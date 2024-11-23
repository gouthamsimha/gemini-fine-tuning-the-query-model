import streamlit as st

# This must be the first Streamlit command
st.set_page_config(page_title="Fine-tuning Progress Dashboard", layout="wide")

from fine_tuning.train import GeminiFineTuner
import time
from datetime import datetime

def main():
    st.title("Gemini Fine-Tuning Dashboard")
    
    # Training parameters in sidebar
    with st.sidebar:
        st.header("Training Parameters")
        epoch_count = st.slider("Number of Epochs", 10, 200, 100)
        batch_size = st.slider("Batch Size", 2, 16, 4)
        learning_rate = st.number_input("Learning Rate", 0.0001, 0.01, 0.001, format="%.4f")

    # Initialize progress containers
    progress_bar = st.empty()
    status_text = st.empty()
    metrics_container = st.empty()

    tuner = GeminiFineTuner()

    if st.button("Start Training"):
        try:
            with st.spinner("Training in progress..."):
                operation, model_name = tuner.train(
                    epoch_count=epoch_count,
                    batch_size=batch_size,
                    learning_rate=learning_rate
                )
                
                # Monitor progress
                for status in operation.wait_bar():
                    progress = getattr(status, 'progress', 0) / 100
                    progress_bar.progress(progress)
                    status_text.text(f"Status: {status}")
                    time.sleep(1)
                
                st.success(f"Training completed! Model: {model_name}")
                
        except Exception as e:
            st.error(f"Training failed: {str(e)}")

if __name__ == "__main__":
    main()