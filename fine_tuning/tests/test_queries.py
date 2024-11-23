import json
import sys
import os
from datetime import datetime

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from database import DatabaseConnector
from typing import List, Dict

class QueryTester:
    def __init__(self):
        self.db = DatabaseConnector()
        self.results: Dict[str, List] = {
            "successful": [],
            "failed": [],
            "syntax_error": []
        }
        # Create test_results directory if it doesn't exist
        self.results_dir = 'fine_tuning/test_results'
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Update output files to use new directory
        self.success_file = os.path.join(self.results_dir, 'database_tested.md')
        self.error_file = os.path.join(self.results_dir, 'database_errors.md')
        
    def write_to_file(self, content: str, is_error: bool = False):
        file_path = self.error_file if is_error else self.success_file
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content + '\n')

    def test_query(self, example: Dict, query_num: int) -> bool:
        try:
            query = example['sql']
            text_input = example['user_query']
            explanation = example.get('explanation', '')
            
            result = self.db.execute_query(query)
            
            # Check if result is empty/None - treat as error
            if not result:
                self.write_to_file(f"""## Question {query_num}
### User Query
{text_input}

### Explanation
{explanation}

### SQL Query
```sql
{query}
```

### Error
Query returned no results - possible incorrect query

---
""", is_error=True)
                return False
            
            # Format result to show only first 5 entries
            formatted_result = result
            if isinstance(result, list) and len(result) > 5:
                formatted_result = result[:5]
                formatted_result.append({"note": f"... and {len(result) - 5} more rows"})
            
            # Check for errors in result
            if result is not None and isinstance(result, dict) and 'error' in result:
                # Write to error file
                self.write_to_file(f"""## Question {query_num}
### User Query
{text_input}

### Explanation
{explanation}

### SQL Query
```sql
{query}
```

### Error
```json
{json.dumps(result, indent=2)}
```

---
""", is_error=True)
                return False
            
            # Write successful queries to main file
            self.write_to_file(f"""## Question {query_num}
### User Query
{text_input}

### Explanation
{explanation}

### SQL Query
```sql
{query}
```

### Result
```json
{json.dumps(formatted_result, indent=2) if result else 'No results'}
```

---
""")
            
            return result is not None
            
        except Exception as e:
            self.write_to_file(f"""## Question {query_num}
### User Query
{text_input}

### Explanation
{explanation}

### SQL Query
```sql
{query}
```

### Error
```
{str(e)}
```

---
""", is_error=True)
            return False

    def load_and_test_queries(self):
        try:
            with open('fine_tuning/training_data/validation_queries.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("❌ Training data file not found")
            return
        except json.JSONDecodeError:
            print("❌ Invalid JSON format in training data")
            return

        # Clear existing files and write headers
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for file_path in [self.success_file, self.error_file]:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"""# Database Testing Results
Generated on: {timestamp}

Schema Version: {data.get('metadata', {}).get('version', 'Unknown')}
Category: {data.get('metadata', {}).get('category', 'Unknown')}
Description: {data.get('metadata', {}).get('description', 'Unknown')}

---
""")

        total_queries = len(data['examples'])
        print(f"\nTesting {total_queries} queries...")

        for idx, example in enumerate(data['examples'], 1):
            print(f"Testing query {idx}/{total_queries}: {example['user_query'][:50]}...")
            
            is_successful = self.test_query(example, idx)
            
            if is_successful:
                self.results["successful"].append(example)
            else:
                self.results["failed"].append(example)

def main():
    tester = QueryTester()
    tester.load_and_test_queries()
    print(f"\nSuccessful queries saved to: {tester.success_file}")
    print(f"Failed queries saved to: {tester.error_file}")

if __name__ == "__main__":
    main() 