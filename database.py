from supabase import create_client
from typing import Dict, Optional
from fine_tuning.config import SUPABASE_URL, SUPABASE_KEY

class DatabaseConnector:
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    def execute_query(self, sql: str) -> Optional[Dict]:
        try:
            # Remove trailing semicolon if present
            sql = sql.rstrip(';')
            result = self.supabase.rpc('execute_query', {'query': sql}).execute()
            return result.data
        except Exception as e:
            print(f"Database error: {str(e)}")
            return None

    def test_connection(self) -> bool:
        try:
            # Remove async/await - use synchronous call
            test_query = "SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'ipl';"
            result = self.supabase.rpc('execute_query', {'query': test_query}).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False 