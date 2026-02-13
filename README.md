# Wind Turbine Anomaly Detection System

## Table of Contents
1. [Context](https://github.com/LuisBarbosa02/Wind-Turbine-Anomaly-Detection?tab=readme-ov-file#context)
2. [Installation](https://github.com/LuisBarbosa02/Wind-Turbine-Anomaly-Detection?tab=readme-ov-file#installation)
3. [Starting Server](https://github.com/LuisBarbosa02/Wind-Turbine-Anomaly-Detection?tab=readme-ov-file#starting-server)
4. [Model Predictions](https://github.com/LuisBarbosa02/Wind-Turbine-Anomaly-Detection?tab=readme-ov-file#model-predictions)

## Context
This project implements a real-time anomaly detection system for a wind turbine factory by using simulated sensor data.

## Installation
This repository requires Python 3.12.12

Clone and change to the repository:
```bash
git clone https://github.com/LuisBarbosa02/Wind-Turbine-Anomaly-Detection.git
cd Wind-Turbine-Anomaly-Detection
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

## Create Database
To store the raw and predicted sensor values, a PostgreSQL database is created through Docker container:
```bash
docker pull postgres:18
docker network create app_network
docker run -d --name wind_turbine_db -e POSTGRES_USER=luis -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=wind_db -p 5432:5432 -v wind-vol:/var/lib/postgresql --network app_network postgres:18
```

Then the tables are added by running inside the *Wind-Turbine-Anomaly-Detection* folder:
```bash
python -m src.data.create_db_tables
```

The following steps must be taken inside the PostgreSQL database to configure it.
With the database container running, run the commands:
```bash
docker exec -it wind_turbine_db bash
psql -U luis -d wind_db
```

Inside PostgreSQL, create the function:
```bash
CREATE OR REPLACE FUNCTION enforce_sensor_data_limit()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM sensor_data
    WHERE id IN (
        SELECT id
        FROM sensor_data
        ORDER BY timestamp DESC
        OFFSET 50000
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

And its trigger:
```bash
CREATE TRIGGER sensor_data_limit_trigger
AFTER INSERT ON sensor_data
FOR EACH ROW
EXECUTE FUNCTION enforce_sensor_data_limit();
```

## Starting Server
The server where the model will be run must be started. This can be done locally or through Docker.
### Locally
Inside the *Wind-Turbine-Anomaly-Detection* folder:
```bash
uvicorn app.api:app --reload
```

### Through Docker
Within the *Wind-Turbine-Anomaly-Detection* folder, use Dockerfile to create a docker image:
```bash
docker pull luisbarbosa25/wind-turbine-anomaly-detection:latest
```

With the image built, create and run the Docker container:
```bash
docker run --name wind-model -d -v wind-vol:/app -p 8000:8000 luisbarbosa25/wind-turbine-anomaly-detection:latest
```

## Model Predictions
With the server running, start the model predictions by running the command inside *Wind-Turbine-Anomaly-Detection*:
```bash
python sensor.py
```
