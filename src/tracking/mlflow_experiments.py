# Import libraries
import mlflow
import pickle
from ..data.load_data import load_data
from ..config import PREPROCESSOR_PATH, MODEL_PATH
from ..model.train_model import model_parameters
from sklearn.metrics import classification_report

# MLflow experiment
def run_experiment():
    # Set experiment
    mlflow.set_experiment('wind turbine anomaly')

    # Load data
    (_, X_test, _, y_test) = load_data()

    # Load preprocessor
    with open(PREPROCESSOR_PATH, 'rb') as file:
        preprocessor = pickle.load(file)

    # Load model
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)

    # Run experiment
    with mlflow.start_run() as run:
        # Log parameters
        mlflow.log_params(model_parameters)

        # Log metrics
        y_pred = model.predict(preprocessor.transform(X_test))
        report_dict = classification_report(y_test, y_pred, output_dict=True)
        metrics = {}
        for k_1, v_1 in report_dict.items():
            try:
                for k_2, v_2 in v_1.items():
                    metrics[f"{k_1}_{k_2}"] = v_2
            except:
                metrics[k_1] = v_1
        mlflow.log_metrics(metrics)

        # Log model
        mlflow.sklearn.log_model(
            model,
            input_example=X_test,
            name="iso_for",
        )

# Run experiment
if __name__ == '__main__':
    run_experiment()