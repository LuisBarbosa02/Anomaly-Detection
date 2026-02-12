# Import libraries
from ..config import PREPROCESSOR_PATH, PIPELINE_PATH
import mlflow
import pickle
from sklearn.pipeline import Pipeline

# Build pipeline
def build_pipeline():
    """
    Function to build full pipeline.
    :return: pipeline
    """
    # Setting MLflow in Databricks server
    mlflow.set_tracking_uri("databricks")

    # Load preprocessor
    with open(PREPROCESSOR_PATH, 'rb') as file:
        preprocessor = pickle.load(file)

    # Load model
    model_uri = f"models:/workspace.default.sklearn-isolation-forest-anomaly-detection@champion"
    try:
        model = mlflow.sklearn.load_model(model_uri)
    except:
        print("There is no registed model / There is no 'champion' alias on registed model!")

    # Build full pipeline
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    # Save pipeline
    with open(PIPELINE_PATH, 'wb') as file:
        pickle.dump(pipeline, file)

    return pipeline

# RUN
if __name__ == '__main__':
    build_pipeline()