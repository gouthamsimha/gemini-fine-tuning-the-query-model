# 1. First set the PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd) -- dont need to use this anymore since we installed this "pip install -e ."

This will:
Install your package in "editable" mode
Make it available for importing anywhere
Automatically install required dependencies
After this, you can run Streamlit without setting PYTHONPATH:

# 2. Then run Streamlit
streamlit run fine_tuning/streamlit_app.py


##
Browser Tab 1: Streamlit (http://localhost:8501)
    └── Control training & see progress

Browser Tab 2: MLflow (http://localhost:5000)
    └── Compare runs & analyze metrics locally

Browser Tab 3: W&B (wandb.ai)
    └── Detailed analytics & visualizations in cloud




  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.12.111:8501