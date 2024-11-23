from setuptools import setup, find_packages

setup(
    name="fine_tuning",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "google-generativeai",
        "mlflow",
        "wandb",
        "pandas",
        "python-dotenv",
    ],
) 