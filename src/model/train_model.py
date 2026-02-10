# Import libraries
from ..data.load_data import load_data
from ..config import PREPROCESSOR_PATH, MODEL_PATH
import pickle
from sklearn.ensemble import IsolationForest

# Parameters
model_parameters = {
    "n_estimators": 100,
    "contamination": 0.07,
    "random_state": 42
}

# Train model
def train_model(params: dict):
    """
    Function to train model.
    :return: model
    """
    # Load data
    (X_train, _, y_train, _) = load_data()

    # Load preprocessor
    with open(PREPROCESSOR_PATH, 'rb') as file:
        preprocessor = pickle.load(file)

    # Preprocess data
    X_train = preprocessor.transform(X_train)

    # Train model
    model = IsolationForest(**params).fit(X_train)

    # Save model
    with open(MODEL_PATH, 'wb') as file:
        pickle.dump(model, file)

    return model

# RUN
if __name__ == '__main__':
    train_model(model_parameters)