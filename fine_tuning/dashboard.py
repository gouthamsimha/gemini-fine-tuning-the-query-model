import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List

class TrainingDashboard:
    def __init__(self):
        pass
        
        # Initialize containers
        self.metrics_container = st.container()
        self.progress_container = st.container()
        self.examples_container = st.container()
        
    def update_metrics(self, metrics: Dict[str, float]):
        with self.metrics_container:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("SQL Validity Rate", f"{metrics.get('sql_validity_rate', 0):.2%}")
            with col2:
                st.metric("Success Rate", f"{metrics.get('success_rate', 0):.2%}")
            with col3:
                st.metric("Avg Response Time", f"{metrics.get('average_response_time', 0):.3f}s")
    
    def update_progress(self, progress: float, status: str):
        with self.progress_container:
            st.progress(progress)
            st.text(f"Status: {status}")
    
    def show_examples(self, examples: List[Dict]):
        with self.examples_container:
            st.subheader("Training Examples")
            df = pd.DataFrame(examples)
            st.dataframe(df) 