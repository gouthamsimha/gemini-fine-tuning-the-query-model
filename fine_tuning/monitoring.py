import logging
import mlflow
from datetime import datetime
from typing import Dict, Any
import wandb
from wandb.sdk.data_types import Table
from .config import FINE_TUNED_MODEL_NAME

class FineTuningMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        mlflow.set_experiment("gemini_fine_tuning")
        self.metrics: Dict[str, Any] = {}
        wandb.init(
            project="cricket-sql-generator",
            config={
                "model": FINE_TUNED_MODEL_NAME,
                "architecture": "gemini-pro"
            }
        )
    
    def log_training_start(self, num_examples: int):
        mlflow.start_run()
        mlflow.log_param("num_examples", num_examples)
        mlflow.log_param("model_name", FINE_TUNED_MODEL_NAME)
        mlflow.log_param("start_time", datetime.now().isoformat())
        self.metrics['start_time'] = datetime.now()
        self.metrics['num_examples'] = num_examples
        self.logger.info(f"Starting fine-tuning with {num_examples} examples")
    
    def log_metrics(self, metrics: Dict[str, float]):
        mlflow.log_metrics({
            "sql_validity_rate": metrics["sql_validity_rate"],
            "success_rate": metrics["success_rate"],
            "average_response_time": metrics["average_response_time"]
        })

    def log_training_complete(self, model_name: str, validation_results: Dict):
        duration = datetime.now() - self.metrics['start_time']
        mlflow.log_metric("training_duration_seconds", duration.total_seconds())
        mlflow.log_metrics(validation_results)
        mlflow.end_run()

    def log_example(self, input_text: str, predicted_sql: str, actual_sql: str):
        wandb.log({
            "examples": Table(
                columns=["input", "predicted", "actual"],
                data=[[input_text, predicted_sql, actual_sql]]
            )
        })

    def log_training_metrics(self, metrics: Dict[str, float]):
        wandb.log(metrics)

class WandBMonitor:
    def __init__(self):
        """Initialize WandB monitoring."""
        self.run = None
    
    def log_training_metrics(self, metrics: Dict[str, float]):
        """Log training metrics to WandB."""
        if not self.run:
            self.run = wandb.init(
                project="cricket-sql-generator",
                config={
                    "model": "gemini-pro",
                    "timestamp": datetime.now().isoformat()
                }
            )
        wandb.log(metrics)
    
    def log_validation_results(self, results: Dict[str, Any]):
        """Log validation results to WandB."""
        if self.run:
            wandb.log(results)
    
    def finish(self):
        """End the WandB run."""
        if self.run:
            wandb.finish()