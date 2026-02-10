# Python image
FROM python:3.12.12-slim

# Working directory
WORKDIR /app

# Copy necessary files
COPY requirements.txt .
COPY app/ ./app
COPY artifacts/pipeline.pkl ./artifacts/pipeline.pkl
COPY .env ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Port where API will be executed
EXPOSE 8000

# Execute command
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]