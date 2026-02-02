# Import libraries
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
import mlflow

# Setting experiment
mlflow.set_experiment('Anomaly Detection')

# Loading data
path = Path(__file__).parent.parent / "data/main_data.csv"
main_data = pd.read_csv(path)

dataframe = main_data.copy()
dataframe = dataframe.drop('timestamp', axis=1)
label = dataframe.pop('anomaly')

# Separating test data
X_train, X_test, y_train, y_test = train_test_split(
    dataframe, label, test_size=0.25, random_state=42, stratify=label
)

# Params
params = {
    "n_estimators": 100,
    "contamination": 0.07,
    "random_state": 42
}

# Preprocessor
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), X_train.columns)
], remainder='drop')

# Pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", IsolationForest(**params))
])
pipeline.fit(X_train)

# Logging entire experiment to MLFlow
if input("Save into MLFlow? (True/False)") == "True":
    with mlflow.start_run():
        # Logging params
        mlflow.log_params(params)

        # Logging model
        mlflow.sklearn.log_model(
            pipeline, name="anomaly_model", registered_model_name="sklearn-isolation-forest-anomaly-clas-model"
        )

        # Logging metrics
        y_pred = pipeline.predict(X_test)
        report_dict = classification_report(y_test, y_pred, output_dict=True)
        metrics = {}
        for k_1, v_1 in report_dict.items():
            try:
                for k_2, v_2 in v_1.items():
                    metrics[f"{k_1}_{k_2}"] = v_2
            except:
                metrics[k_1] = v_1
        mlflow.log_metrics(metrics)