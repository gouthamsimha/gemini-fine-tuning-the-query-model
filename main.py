from google.generativeai import GenerativeModel
import google.generativeai as genai
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException
from schemas.database_schema import get_system_prompt
from database import DatabaseConnector
from fine_tuning.config import GEMINI_API_KEY, FINE_TUNED_MODEL_NAME
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = GenerativeModel(FINE_TUNED_MODEL_NAME)

class CricketQueryProcessor:
    def __init__(self):
        self.system_prompt = get_system_prompt()

    async def generate_sql(self, user_query: str) -> Optional[str]:
        try:
            prompt = f"{self.system_prompt}\n{user_query}"
            response = await model.generate_content_async(prompt)
            return self._clean_sql(response.text)
        except Exception as e:
            logger.error(f"Error generating SQL: {str(e)}")
            return None

    def _clean_sql(self, sql: str) -> str:
        sql = sql.replace('```sql', '').replace('```', '')
        return sql.strip()

    def validate_sql(self, sql: str) -> bool:
        if not sql:
            return False
            
        # Only allow SELECT statements
        sql_upper = sql.upper().strip()
        if not sql_upper.startswith('SELECT '):
            return False

        # Additional validation can be added here
        return True

class CricketStatsAPI:
    def __init__(self):
        self.query_processor = CricketQueryProcessor()
        self.db = DatabaseConnector()

    async def process_question(self, user_question: str) -> Dict:
        try:
            # Generate SQL
            sql_query = await self.query_processor.generate_sql(user_question)
            if not sql_query:
                return {"error": "Failed to generate SQL query", "status": "error"}

            # Validate SQL
            if not self.query_processor.validate_sql(sql_query):
                return {"error": "Invalid SQL query generated", "status": "error"}

            # Execute query
            results = await self.db.execute_query(sql_query)
            if results is None:
                return {"error": "Database query failed", "status": "error"}

            # Format response
            return {
                "sql": sql_query,
                "results": results,
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            return {"error": str(e), "status": "error"}

# FastAPI app
app = FastAPI(title="Cricket Stats API")
cricket_stats = CricketStatsAPI()

@app.post("/api/query")
async def query_stats(request: Dict):
    try:
        question = request.get("question")
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")

        result = await cricket_stats.process_question(question)
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except Exception as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    db = DatabaseConnector()
    db_status = await db.test_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)