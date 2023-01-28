import pandas as pd
from barbell import Barbell


def generate_barbell_distribution(dataframe, columns, upsample_number):
    """Generates a barbell distribution for the specified columns in the dataframe."""
    dataframe = dataframe.drop_duplicates().reset_index(drop=True)
    upsample_number = int(upsample_number / 2)
    barbell_data = pd.DataFrame()
    for column in columns:
        min_value = dataframe[column].min()
        max_value = dataframe[column].max()
        std = dataframe[column].std()*0.25
        barbell = Barbell(min_value, max_value, std, upsample_number)
        barbell.run_simulation()
        barbell_data[column] = barbell.get_data()
    dataframe[columns] = barbell_data[columns].reset_index(drop=True)
    return dataframe