import pandas as pd
import numpy as np
import random
from typing import List


class SyntheticDataGenerator:
    """
    A class for generating synthetic dataset based on given dataset
    """

    def __init__(self, dataset, target):
        """
        Initializes the synthetic dataset generator
        Parameters:
            dataset (pandas.DataFrame): The dataset to use for generating synthetic data
        """
        self.dataset = dataset
        self.target = target
        self.np_random = np.random.RandomState(0)

    def generate_target(self, iterations: int) -> List[int]:
        """
        Generates a list of binary values (1s and 0s) based on the proportion of the target variable in the dataset.
        The number of 1s in the list is equal to the proportion of 1s in the target variable, and the number of 0s is
        equal to the proportion of 0s. The list is then shuffled to generate a random sequence of 1s and 0s.
        Parameters:
        - self (object): the instance of the class
        - iterations (int): the number of binary values to be generated
        Returns:
        - List[int]: a list of binary values (1s and 0s)
        """
        proportion = self.dataset[self.target].value_counts(normalize=True)[1]
        ones = int(proportion * iterations)
        zeros = iterations - ones
        target_list = [1] * ones + [0] * zeros
           
        random.shuffle(target_list)

        return target_list

    def generate_data(self, iterations: int) -> pd.DataFrame:
        """
        Generates new synthetic data
        Parameters:
            iterations (int): The number of iterations to generate synthetic data for
        Returns:
            synthetic_data (pandas.DataFrame): The synthetic data generated
        """
        generated_target = self.generate_target(iterations)
        self.dataset.drop(columns=self.target, axis=1, inplace=True)

        synthetic_data = pd.DataFrame(
            columns=self.dataset.columns, index=range(iterations)
        )
        for i in range(iterations):
            for col in self.dataset.columns:
                if self.dataset[col].dtype in ["float"]:
                    synthetic_data.loc[i, col] = self.np_random.uniform(
                        self.dataset[col].min(), self.dataset[col].max()
                    )
                if self.dataset[col].dtype in ["int"]:
                    if len(self.dataset[col].unique()) == 2:
                        synthetic_data.loc[i, col] = self.np_random.choice(
                            range(self.dataset[col].min(), self.dataset[col].max() + 1)
                        )
                    else:
                        synthetic_data.loc[i, col] = self.np_random.randint(
                            self.dataset[col].min(), self.dataset[col].max()
                        )
                else:
                    synthetic_data.loc[i, col] = self.np_random.choice(
                        self.dataset[col].unique()
                    )

        synthetic_data[self.target] = generated_target

        return synthetic_data


1

