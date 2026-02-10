# Import libraries
import pandas as pd
from ..config import DATA_PATH
from sklearn.model_selection import train_test_split

# Load data
def load_data():
    """
    Function to load data.
    """
    # Load dataset
    df = pd.read_csv(DATA_PATH)

    # Adjust table
    df = df.drop('timestamp', axis=1)
    label = df.pop('anomaly')

    # Splitting data
    X_train, X_test, y_train, y_test = train_test_split(
        df, label, test_size=0.25, random_state=42, stratify=label
    )

    return (X_train, X_test, y_train, y_test)

# TEST
if __name__ == '__main__':
    print(load_data())