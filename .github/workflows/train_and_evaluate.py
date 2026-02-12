name: Train and Evaluate Model

on:
	workflow_dispatch:

jobs:
	train-and-evaluate:
		runs-on: ubuntu-latest

		steps:
		- name: Checkout repository
		  uses: actions/checkout@4

		- name: Set up Python
		  uses: actions/setup-python@5
		  with: 
			python-version: '3.12.12'

		- name: Install dependencies
		  run: |
			python -m pip install --upgrade pip
			pip install -r requirements.txt

		- name: Train and save preprocessor
		  run: python -m src.features.train_preprocessor

		- name: Train and save model
		  run: python -m src.model.train_model

		- name: Log experiment
		  env:
			DATABRICKS_HOST: ${{  secrets.DATABRICKS_HOST  }}
			DATABRICKS_TOKEN: ${{  secrets.DATABRICKS_TOKEN  }}
			MLFLOW_TRACKING_URI: databricks

		  run: python -m src.tracking.mlflow_experiments