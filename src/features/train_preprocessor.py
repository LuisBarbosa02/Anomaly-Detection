# Import libraries
from ..data.load_data import load_data
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
import pickle
from ..config import PREPROCESSOR_PATH

# Train preprocessor
def train_preprocessor():
    """
    Function to train preprocessor.
    :return: preprocessor
    """
    # Load data
    X_train = load_data()[0]

    # Train preprocessor
    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), X_train.columns)
    ], remainder='drop').fit(X_train)

    # Save preprocessor
    with open(PREPROCESSOR_PATH, 'wb') as file:
        pickle.dump(preprocessor, file)

    return preprocessor

# RUN
if __name__ == '__main__':
    train_preprocessor()