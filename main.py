"""
Created by Zypp, 12-09-2023
"""

import numpy as np
from scipy.stats import expon, kstest
import seaborn as sns
import matplotlib.pyplot as plt


def plot_results(spacings: np.array, params: tuple, p_value: float):
    sns.histplot(spacings, kde=True, stat='density', bins=30, label='Empirical Distribution')
    x = np.linspace(min(spacings), max(spacings), 100)
    pdf = expon.pdf(x, *params)
    plt.plot(x, pdf, label='Theoretical Exponential Distribution', color='red')
    plt.title(f'Distribution of Spacings (p-value: {p_value:.4f})')
    plt.xlabel('Spacing')
    plt.ylabel('Density')
    plt.legend()
    plt.show()


def birthday_spacing_test(n_numbers: int, range_interval: float):
    
    # Generate random uniform point
    random_points = np.random.uniform(low=0.0, high=range_interval, size=n_numbers)

    # Calculate the spacings between the random points
    random_points = np.sort(random_points)
    spacings = np.diff(random_points)

    # Conduct Goodness-of-Fit Test (Kolmogorov-Smirnov Test in this case)
    # Fit the spacings to an exponential distribution to get the parameters
    params = expon.fit(spacings)

    # Conduct the Kolmogorov-Smirnov test to compare the empirical and theoretical distributions
    ks_statistic, p_value = kstest(spacings, 'expon', args=params)

    plot_results(spacings, params, p_value)

    print("KS Statistic:", ks_statistic)
    print("P-value:", p_value)

    if p_value > 0.05:
        print("We fail to reject the null hypothesis, this means that the random generator produces uniformly distributed spacings")
    else:
        print("The random generator is not random")


if __name__ == "__main__":
    birthday_spacing_test(n_numbers=1_000_000, range_interval=1_000_000)
