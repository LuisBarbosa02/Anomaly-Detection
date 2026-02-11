
# Wind Turbine Anomaly Detection System

## Table of Contents
1. [Context](https://github.com/LuisBarbosa02/Anomaly-Detection?tab=readme-ov-file#context)
2. [Installation](https://github.com/LuisBarbosa02/Anomaly-Detection?tab=readme-ov-file#installation)
3. [Starting Server](https://github.com/LuisBarbosa02/Anomaly-Detection?tab=readme-ov-file#starting-server)
4. [Model Predictions](https://github.com/LuisBarbosa02/Anomaly-Detection?tab=readme-ov-file#model-predictions)

## Context
This project implements a real-time anomaly detection system for a wind turbine factory by using simulated sensor data.

## Installation
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

## Starting Server
The server where the model will be run must be started. This can be done locally or through Docker.
### Locally
Inside the *Anomaly-Detection* folder:
```bash
uvicorn app.api:app --reload
```

### Through Docker
Within the *Anomaly-Detection* folder, use Dockerfile to create a docker image:
```bash
docker build -t wind-anomaly-detection .
```

With the image built, create and run the docker container:
```bash
docker run --name wind-anomaly-detection -d -v wind-vol:/app -p 8000:8000 wind-anomaly-detection:latest
```

## Model Predictions
With the server running, start the model predictions by running the command inside *Anomaly-Detection*:
```bash
python sensor.py
```
