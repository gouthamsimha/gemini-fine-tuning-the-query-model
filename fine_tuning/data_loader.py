import json
import os
from typing import List, Dict
import logging
from sqlparse import parse, format

logger = logging.getLogger(__name__)

class TrainingDataLoader:
    def __init__(self, data_dir: str = "fine_tuning/training_data"):
        self.data_dir = data_dir

    def load_all_examples(self) -> List[Dict[str, str]]:
        """Load all training examples from all JSON files."""
        all_examples = []
        
        try:
            for filename in os.listdir(self.data_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.data_dir, filename)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        validated_examples = self._validate_examples(data, filename)
                        all_examples.extend(validated_examples)
                        
            logger.info(f"Loaded {len(all_examples)} training examples")
            return all_examples
        
        except Exception as e:
            logger.error(f"Error loading training data: {str(e)}")
            raise

    def _validate_examples(self, examples: List[Dict], filename: str) -> List[Dict[str, str]]:
        """Validate and format examples for training."""
        validated = []
        for idx, example in enumerate(examples):
            try:
                if 'text_input' not in example or 'output' not in example:
                    logger.warning(f"Skipping invalid example {idx} in {filename}: missing required fields")
                    continue
                
                # Format for Gemini API requirements
                validated.append({
                    'text_input': example['text_input'],
                    'output': example['output']
                })
            
            except Exception as e:
                logger.warning(f"Error validating example {idx} in {filename}: {str(e)}")
                continue
                
        return validated

    def get_examples_by_category(self, category: str) -> List[Dict[str, str]]:
        """Load training examples from a specific category."""
        file_path = os.path.join(self.data_dir, f"{category}_queries.json")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Category file not found: {file_path}")
            
        with open(file_path, 'r') as f:
            data = json.load(f)
            return self._validate_examples(data.get('examples', []), f"{category}_queries.json") 

    def _validate_sql_syntax(self, sql: str) -> bool:
        try:
            formatted_sql = format(sql, reindent=True)
            parsed = parse(formatted_sql)
            return len(parsed) > 0
        except Exception as e:
            logger.warning(f"Invalid SQL syntax: {str(e)}")
            return False