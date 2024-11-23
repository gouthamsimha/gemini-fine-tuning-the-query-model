## Features
- Text-to-SQL conversion using fine-tuned Gemini model
- Custom training examples for various cricket queries:
  - Player comparisons
  - Venue-specific analysis  
  - Basic and advanced statistics
  - Career stats
  - Match analysis

## Implementation
This fine tuned model takes natural language queries, converts them to SQL using the fine-tuned Gemini model, executes them against the database, and displays results in the frontend interface.

The model is trained on custom examples from our Postgres database to handle cricket-specific queries and terminology.

