
# Anomaly Detection System

## Table of Contents
1. [Context](https://github.com/LuisBarbosa02/Anomaly-Detection?tab=readme-ov-file#context)
2. [How to Use](https://github.com/LuisBarbosa02/Anomaly-Detection?tab=readme-ov-file#how-to-use)

## Context
This project implements a real-time anomaly detection system for a wind turbine factory by using simulated sensor data.

## How to Use
### Installation
This repository requires Python 3.12.12

Clone and change to the repository:
```bash
git clone https://github.com/LuisBarbosa02/Anomaly-Detection.git
cd Anomaly-Detection
```

[Optional] Create and activate a virtual environment:
```bash
python3.12 -m venv venv
source venv/bin/activate
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

### Running Project
Inside the *Anomaly-Detection* folder, start MLflow to log model and metrics:
```bash
mlflow ui
```

Open another terminal and load the venv, then the model can be trained by running the **train_model.py** script on the *model* folder. This can be done by running the following command inside the *Anomaly-Detection* folder:
```bash
python -m model.train_model
```

Inside MLflow, add the alias "champion" to the main model version.

To run the simulated sensor data on the main model, close the current MLFlow server and serve the registered model locally by running the following command inside the *Anomaly-Detection* folder:
```bash
mlflow models serve \
-m models:/sklearn-isolation-forest-anomaly-clas-model@champion \
-p 5000 \
--env-manager local
```
Then, run outside the *Anomaly-Detection* folder:
```bash
python -m Anomaly-Detection.sensor
```
