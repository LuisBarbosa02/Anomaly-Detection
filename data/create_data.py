# Import libraries
from . import data_generator
import pandas as pd

# Create data
if __name__ == '__main__':
    gen = data_generator.SensorDataGenerator()
    df = pd.DataFrame(
        columns=['timestamp', 'temperature', 'humidity', 'sound', 'anomaly']
    )

    n_samples = int(input('Insert number of samples: '))
    for _ in range(n_samples):
        data = gen.step()
        df.loc[len(df)] = data

    print(df)
    df.to_csv('model2production/data/testing.csv', index=False)