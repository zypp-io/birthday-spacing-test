"""
Created by Zypp, 12-09-2023
"""

import numpy as np
from scipy.stats import expon, kstest
import seaborn as sns
import matplotlib.pyplot as plt
from time import time
import pandas as pd


def plot_results_ks_test(spacings: np.array, params: tuple, p_value: float) -> None:
    sns.histplot(spacings, kde=True, stat='density', bins=30, label='Empirical Distribution')
    x = np.linspace(min(spacings), max(spacings), 100)
    pdf = expon.pdf(x, *params)
    plt.plot(x, pdf, label='Theoretical Exponential Distribution', color='red')
    plt.title(f'Distribution of Spacings (p-value: {p_value:.4f})')
    plt.xlabel('Spacing')
    plt.ylabel('Density')
    plt.legend()
    plt.show()


def test_randomness_with_ks_test(n_numbers: int, range_interval: float) -> None:
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

    plot_results_ks_test(spacings, params, p_value)

    print("KS Statistic:", ks_statistic)
    print("P-value:", p_value)

    if p_value > 0.05:
        print(
            "PASS: We fail to reject the null hypothesis, "
            "this means that the random generator produces uniformly distributed spacings")
    else:
        print("FAIL: The random generator is not random")


def plot_results_birthday_spacing_test(df):
    """
    Plot die de resultaten van de test tonen.
    """
    plt.figure(figsize=(12, 6))

    sns.lineplot(x="Number of People", y="Expected Percentage", data=df, marker="o", linestyle="--",
                 label="Verwachte distributie", color='blue')
    sns.lineplot(x="Number of People", y="Calculated Percentage", data=df, marker="x", linestyle="-",
                 label="Berekende Distributie", color='red')
    plt.fill_between(df["Number of People"], df["Expected Percentage"], df["Calculated Percentage"], color='grey',
                     alpha=0.1)

    plt.title("Verwachte vs. berekende kans op overlap in verjaardagen")
    plt.ylabel("Kans op overlap in verjaardag")
    plt.xlabel("Aantal personen in een kamer")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()

    plt.show()


def check_overlapping_birthdays(birthday_list: list) -> bool:
    """
    Neemt birthday_list als input en geeft terug of er overlap is in de lijst.
    Parameters
    ----------
    birthday_list: list
        lijst met gegenereerde verjaardagen.

    Returns
    -------
    resultaat van de check: bool
        geeft het resultaat terug of er wel of niet overlap is.
    """

    # controleer of er overlap is.
    overlapping_birthdays = [birthday for birthday in set(birthday_list) if birthday_list.count(birthday) > 1]

    if overlapping_birthdays:
        return True
    else:
        return False


def generate_birthdays(counter: int, n_numbers:int) -> list:
    """
    Neemt counter en n_numbers als input en geeft een lijst terug met willekeurige nummers (verjaardagen). We gebruiken
    geen datumvelden, maar getallen van 1 tot 365.

    Parameters
    ----------
    counter: int
        teller die wordt toegevoegd aan de seed om randomness te garanderen.
    n_numbers: int
        Aantal nummers die je wil genereren.

    Returns
    -------
    birthdays : list
        lijst met nummers die gezien worden als willekeurige verjaardagen.
    """
    # pas de random seed aan omdat de test vaak wordt uitgevoerd binnen dezelfde seconde.
    random_seed = int(time()) + counter
    rnd = np.random.RandomState(random_seed)
    birthdays = list(rnd.randint(low=1, high=365, size=n_numbers))

    return birthdays


def birthday_spacing_expectation() -> dict:
    """
    Geeft de kans terug dat er overlap is in verjaardagen, op basis van het aantal personen in een kamer.
    Returns
    -------
    birthday_dict: dict
        de key's zijn aantal personen en de values zijn de kans dat er overlap is op de verjaardag.
    """

    birthday_dict = {
        1: 0.0,
        5: 2.7,
        10: 11.7,
        20: 41.1,
        23: 50.7,
        30: 70.6,
        40: 89.1,
        50: 97.0,
        60: 99.4,
        70: 99.9,
        75: 99.97,
        100: 99.99997
    }

    return birthday_dict


def perform_birthday_spacing_test(n_numbers: int, n_perform_test: int = 10_000) -> float:
    """
    neemt n_numbers en n_perform_tests aan als variabelen en voert de birthday spacing test uit. Het doel van deze test
    is om aan te tonen dat de volgende verdeling opgaat.
    Parameters
    ----------
    n_numbers
    n_perform_test

    Returns
    -------
    percentage: int
        berekend percentage van overlap.
    """
    result_list = list()

    for counter in range(n_perform_test):
        # genereer n_numbers aan verjaardagen.
        birthday_list = generate_birthdays(n_numbers=n_numbers, counter=counter)
        check_overlap = check_overlapping_birthdays(birthday_list)
        result_list.append(check_overlap)
    passes = len([x for x in result_list if x])
    percentage = round(((passes / n_perform_test) * 100), 2)

    return percentage


def test_randomness_with_birthday_spacing_test() -> None:
    """
    Voert de birthday spacing test uit en bepaald of de verwachte kans overeenkomt met de werkelijke kans.
        1. De dictionary met expected outcome wordt getoetst door 100.000 keer de generator uit te laten voeren.
        2. De resultaten worden geplot in een frame, om aan te tonen dat de berekende kans overeenkomt met de verwachte kans.
    """
    expected_outcome_dict = birthday_spacing_expectation()

    results_data = {"Number of People": [], "Expected Percentage": [], "Calculated Percentage": []}

    for number_of_people, expected_percentage in expected_outcome_dict.items():
        calculated_percentage = perform_birthday_spacing_test(n_numbers=number_of_people, n_perform_test=100_000)

        results_data["Number of People"].append(number_of_people)
        results_data["Expected Percentage"].append(expected_percentage)
        results_data["Calculated Percentage"].append(calculated_percentage)

        diff = calculated_percentage - expected_percentage
        if abs(diff) < 1:
            print(
                f"PASS: test geslaagd voor {number_of_people} persoon. \nverwachte kans: {expected_percentage}\nberekende kans: {calculated_percentage}")
        else:
            print(
                f"FAIL: test NIET geslaagd voor {number_of_people} persoon. \nverwachte kans: {expected_percentage}\nberekende kans: {calculated_percentage}")

    # Plot the results
    df = pd.DataFrame(results_data)
    plot_results_birthday_spacing_test(df)


if __name__ == "__main__":
    test_randomness_with_ks_test(n_numbers=1_000_000, range_interval=1_000_000)
    test_randomness_with_birthday_spacing_test()
