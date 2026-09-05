import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest


def conversion_summary(
    df: pd.DataFrame,
    group_col: str = "test group",
    conversion_col: str = "converted"
) -> pd.DataFrame:
    """
    Calculate users, conversions, and conversion rates by experiment group.
    """
    summary = (
        df.groupby(group_col)[conversion_col]
        .agg(
            users="count",
            conversions="sum"
        )
        .reset_index()
    )

    summary["conversion_rate"] = (
        summary["conversions"] / summary["users"]
    )

    return summary


def two_proportion_test(
    df: pd.DataFrame,
    group_col: str = "test group",
    conversion_col: str = "converted",
    treatment: str = "ad",
    control: str = "psa"
) -> dict:
    """
    Perform a two-proportion z-test comparing treatment and control
    conversion rates.

    Returns the z-statistic, p-value, conversion rates, absolute
    difference, and 95% confidence interval.
    """

    treatment_data = df[df[group_col] == treatment][conversion_col]
    control_data = df[df[group_col] == control][conversion_col]

    treatment_conversions = treatment_data.sum()
    control_conversions = control_data.sum()

    treatment_n = len(treatment_data)
    control_n = len(control_data)

    treatment_rate = treatment_conversions / treatment_n
    control_rate = control_conversions / control_n

    counts = np.array([
        treatment_conversions,
        control_conversions
    ])

    sample_sizes = np.array([
        treatment_n,
        control_n
    ])

    z_stat, p_value = proportions_ztest(
        counts,
        sample_sizes
    )

    difference = treatment_rate - control_rate

    # Unpooled Wald confidence interval
    standard_error = np.sqrt(
        (treatment_rate * (1 - treatment_rate) / treatment_n)
        +
        (control_rate * (1 - control_rate) / control_n)
    )

    margin_of_error = 1.96 * standard_error

    ci_lower = difference - margin_of_error
    ci_upper = difference + margin_of_error

    relative_lift = (
        difference / control_rate
        if control_rate != 0
        else np.nan
    )

    return {
        "treatment_rate": treatment_rate,
        "control_rate": control_rate,
        "absolute_difference": difference,
        "relative_lift": relative_lift,
        "z_statistic": z_stat,
        "p_value": p_value,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper
    }


def cohens_h(
    treatment_rate: float,
    control_rate: float
) -> float:
    """
    Calculate Cohen's h for two proportions.
    """

    transformed_treatment = (
        2 * np.arcsin(np.sqrt(treatment_rate))
    )

    transformed_control = (
        2 * np.arcsin(np.sqrt(control_rate))
    )

    return transformed_treatment - transformed_control


def mann_whitney_analysis(
    df: pd.DataFrame,
    group_col: str = "test group",
    value_col: str = "total ads",
    treatment: str = "ad",
    control: str = "psa"
) -> dict:
    """
    Perform a Mann-Whitney U test and calculate rank-biserial correlation
    for a continuous/skewed variable.
    """

    treatment_values = df.loc[
        df[group_col] == treatment,
        value_col
    ]

    control_values = df.loc[
        df[group_col] == control,
        value_col
    ]

    u_statistic, p_value = stats.mannwhitneyu(
        treatment_values,
        control_values,
        alternative="two-sided"
    )

    n_treatment = len(treatment_values)
    n_control = len(control_values)

    rank_biserial = (
        (2 * u_statistic)
        / (n_treatment * n_control)
    ) - 1

    return {
        "u_statistic": u_statistic,
        "p_value": p_value,
        "rank_biserial": rank_biserial
    }


def benjamini_hochberg(
    p_values,
    alpha: float = 0.05
) -> pd.DataFrame:
    """
    Apply Benjamini-Hochberg false discovery rate correction.

    Parameters
    ----------
    p_values : array-like
        Collection of raw p-values.
    alpha : float
        Desired false discovery rate.

    Returns
    -------
    pd.DataFrame
        Raw p-values, adjusted p-values, and significance flags.
    """

    p_values = np.asarray(p_values, dtype=float)

    n = len(p_values)

    order = np.argsort(p_values)

    sorted_p = p_values[order]

    adjusted = np.empty(n)

    cumulative_min = 1.0

    for i in range(n - 1, -1, -1):
        rank = i + 1

        adjusted_value = (
            sorted_p[i] * n / rank
        )

        cumulative_min = min(
            cumulative_min,
            adjusted_value
        )

        adjusted[i] = cumulative_min

    adjusted = np.minimum(adjusted, 1.0)

    adjusted_original_order = np.empty(n)

    adjusted_original_order[order] = adjusted

    return pd.DataFrame({
        "raw_p_value": p_values,
        "adjusted_p_value": adjusted_original_order,
        "significant": adjusted_original_order < alpha
    })