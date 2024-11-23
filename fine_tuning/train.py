import google.generativeai as genai
import os
import random
from fine_tuning.data_loader import TrainingDataLoader
import logging
from datetime import datetime
from typing import List, Dict
import time
from fine_tuning.monitoring import FineTuningMonitor, WandBMonitor
from fine_tuning.dashboard import TrainingDashboard
from fine_tuning import config
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiFineTuner:
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        logger.info(f"API Key found: {'Yes' if self.api_key else 'No'}")
        logger.info(f"Current working directory: {os.getcwd()}")
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables or .env file")
        
        genai.configure(api_key=self.api_key)
        self.data_loader = TrainingDataLoader()
        self.mlflow_monitor = FineTuningMonitor()
        self.wandb_monitor = WandBMonitor()
        self.dashboard = TrainingDashboard()

    def get_base_model(self):
        """Get the appropriate base model for fine-tuning."""
        base_models = [
            m for m in genai.list_models()
            if "createTunedModel" in m.supported_generation_methods and
            "flash" in m.name
        ]
        
        if not base_models:
            raise ValueError("No suitable base model found for fine-tuning")
        
        return base_models[0]

    def train(self, 
              epoch_count: int = 100,
              batch_size: int = 4,
              learning_rate: float = 0.001):
        """Start the fine-tuning process."""
        try:
            # Load training data and format it correctly
            raw_data = self.data_loader.load_all_examples()
            training_data = [
                {
                    'text_input': example['text_input'],
                    'output': example['output']
                }
                for example in raw_data
            ]
            logger.info(f"Loaded {len(training_data)} training examples")

            # Generate unique model name
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            model_name = f'cricket-sql-{timestamp}'.lower()
            
            if len(model_name) > 40:
                model_name = f'cricket-{timestamp}'.lower()

            # Get base model
            base_model = self.get_base_model()
            logger.info(f"Using base model: {base_model.name}")

            # Start fine-tuning
            operation = genai.create_tuned_model(
                source_model=base_model.name,
                training_data=training_data,
                id=model_name,
                epoch_count=epoch_count,
                batch_size=batch_size,
                learning_rate=learning_rate
            )

            logger.info(f"Started fine-tuning model: {model_name}")

            # Monitor training progress
            start_time = time.time()
            for status in operation.wait_bar():
                current_time = time.time()
                elapsed_time = current_time - start_time
                
                # Extract serializable information from status
                status_info = {
                    'status': str(status),
                    'timestamp': datetime.now().isoformat(),
                    'progress': getattr(status, 'progress', 0),
                    'state': getattr(status, 'state', 'unknown'),
                    'elapsed_minutes': round(elapsed_time / 60, 2)
                }
                
                if self.wandb_monitor:
                    self.wandb_monitor.log_training_metrics(status_info)
                
                # Print detailed progress information
                logger.info(f"""
Training Progress:
Status: {status_info['status']}
Progress: {status_info['progress']}%
State: {status_info['state']}
Elapsed Time: {status_info['elapsed_minutes']} minutes
                """)
                
                time.sleep(30)  # Check status every 30 seconds

            # Get the final model
            model = operation.result()

            # Log final metrics if available
            if hasattr(model, 'tuning_task') and hasattr(model.tuning_task, 'snapshots'):
                snapshots = pd.DataFrame(model.tuning_task.snapshots)
                for _, snapshot in snapshots.iterrows():
                    metrics = {
                        'epoch': int(snapshot.get('epoch', 0)),
                        'mean_loss': float(snapshot.get('mean_loss', 0.0))
                    }
                    self.wandb_monitor.log_training_metrics(metrics)

            return operation, model_name

        except Exception as e:
            logger.error(f"Error during training setup: {str(e)}")
            raise

    def monitor_training(self, operation):
        """Monitor the training progress."""
        try:
            # Get initial status
            status = operation.metadata()
            logger.info(f"Initial Queue Status:")
            logger.info(f"Operation ID: {operation.operation.name}")
            logger.info(f"Queue State: {getattr(status, 'queueState', 'unknown')}")
            logger.info(f"Current Status: {status}")

            while not operation.done():
                # Get current status
                status = operation.metadata()
                
                # Debug logging
                logger.info("Detailed Operation Status:")
                logger.info(f"Operation Done: {operation.done()}")
                logger.info(f"Operation Name: {operation.operation.name}")
                logger.info(f"Full Metadata: {status}")
                
                # Check for errors
                if operation.exception():
                    logger.error(f"Training Error: {operation.exception()}")
                    raise operation.exception()
                
                # Extract progress information
                progress_info = {
                    'status': str(status),
                    'timestamp': datetime.now().isoformat(),
                    'progress': getattr(status, 'progress', 0),
                    'state': getattr(status, 'state', 'unknown'),
                }
                
                # Log to monitoring systems
                if self.wandb_monitor:
                    self.wandb_monitor.log_training_metrics(progress_info)
                
                # Print progress
                logger.info(f"""
Training Progress Update:
Status: {progress_info['status']}
Progress: {progress_info['progress']}%
State: {progress_info['state']}
                """)
                
                time.sleep(30)  # Wait before next check
            
            # Get final model once training is complete
            final_model = operation.result()
            logger.info("Training completed successfully")
            return final_model

        except Exception as e:
            logger.error(f"Error during training monitoring: {str(e)}")
            raise

    def validate_model_output(self, model, test_cases: List[Dict[str, str]]) -> Dict[str, float]:
        results = {
            'success_rate': 0,
            'sql_validity_rate': 0,
            'average_response_time': 0
        }
        
        total = len(test_cases)
        successful = 0
        valid_sql = 0
        total_time = 0
        
        for test in test_cases:
            start_time = time.time()
            try:
                response = model.generate_content(test['text_input'])
                duration = time.time() - start_time
                total_time += duration
                
                if response.text.strip():
                    successful += 1
                    if self.data_loader._validate_sql_syntax(response.text):
                        valid_sql += 1
                        
            except Exception as e:
                logger.error(f"Validation error: {str(e)}")
                
        results['success_rate'] = successful / total
        results['sql_validity_rate'] = valid_sql / total
        results['average_response_time'] = total_time / total
        
        return results

if __name__ == "__main__":
    tuner = GeminiFineTuner()
    operation, model_name = tuner.train()
    model = tuner.monitor_training(operation)
    
    # Load validation set
    validation_data = tuner.data_loader.get_examples_by_category('validation')
    
    # Test the model
    tuned_model = genai.GenerativeModel(model_name=f'tunedModels/{model_name}')
    validation_results = tuner.validate_model_output(tuned_model, validation_data)
    
    print("\nValidation Results:")
    print(f"Success Rate: {validation_results['success_rate']:.2%}")
    print(f"SQL Validity Rate: {validation_results['sql_validity_rate']:.2%}")
    print(f"Average Response Time: {validation_results['average_response_time']:.3f}s") 