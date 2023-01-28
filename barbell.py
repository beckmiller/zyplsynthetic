"""Barbell distribution module"""
import pandas as pd
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt


class Barbell:
    """A class for generating barbell-shaped data."""

    def __init__(
        self,
        min_value,
        max_value,
        std,
        upsample_number,
        bin_size=int(180 / 5),
    ):
        """Initialize the class with the specified parameters.

        :param left_side_min: float, the minimum value of the left side of the barbell
        :param left_side_max: float, the maximum value of the left side of the barbell
        :param right_side_min: float, the minimum value of the right side of the barbell
        :param right_side_max: float, the maximum value of the right side of the barbell
        :param std: float, the standard deviation of the data
        :param upsample_number: int, the number of points to generate
        :param bin_size: int, the number of bins to use for the histogram
        """
        self.left_side_min  = min_value
        self.left_side_max = (max_value + min_value) / 2
        self.right_side_min = (max_value + min_value) / 2
        self.right_side_max = max_value
        self.std = std
        self.upsample_number = upsample_number
        self.bin_size = bin_size
        self.data = pd.DataFrame()

    def generate_left_side(self):
        """Generate the left side of the barbell."""
        mu, sigma = self.left_side_min, self.std
        dist_left = stats.truncnorm(
            (self.left_side_min - mu) / sigma,
            (self.left_side_max - mu) / sigma,
            loc=mu,
            scale=sigma,
        )
        left_side = dist_left.rvs(self.upsample_number)
        return left_side

    def generate_right_side(self):
        """Generate the right side of the barbell."""
        mu, sigma = self.right_side_max, self.std
        dist_right = stats.truncnorm(
            (self.right_side_min - mu) / sigma,
            (self.right_side_max - mu) / sigma,
            loc=mu,
            scale=sigma,
        )
        right_side = dist_right.rvs(self.upsample_number)
        return right_side

    def run_simulation(self):
        """Generate the barbell data and store it in the dataframe."""
        left_side = self.generate_left_side()
        right_side = self.generate_right_side()
        self.data = pd.concat(
            [pd.DataFrame(left_side), pd.DataFrame(right_side)])

    def get_data(self):
        """Return the generated data."""
        return self.data

    def plot_data(self):
        """Plot the generated data using a histogram and density plot."""
        sns.distplot(
            self.data,
            hist=True,
            kde=True,
            bins=self.bin_size,
            color="darkblue",
            hist_kws={"edgecolor": "black"},
            kde_kws={"linewidth": 4},
        )
        plt.show()


if __name__ == "__main__":
    b = Barbell(0.21, 0.57, 0.0185, 3000)
    b.run_simulation()
    b.plot_data()
