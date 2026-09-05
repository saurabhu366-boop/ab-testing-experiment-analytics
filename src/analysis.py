import numpy as np
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

from src.statistics import benjamini_hochberg


def segment_conversion_analysis(
    df: pd.DataFrame,
    segment_col: str,
    group_col: str = "test group",
    conversion_col: str = "converted",
    treatment: str = "ad",
    control: str = "psa"
) -> pd.DataFrame:
    """
    Compare treatment and control conversion rates across segments.

    This function is intended for exploratory segment analysis.
    Segment variables should not automatically be interpreted as
    pre-treatment causal moderators.
    """

    results = []

    for segment in df[segment_col].dropna().unique():

        segment_df = df[df[segment_col] == segment]

        treatment_data = segment_df[
            segment_df[group_col] == treatment
        ][conversion_col]

        control_data = segment_df[
            segment_df[group_col] == control
        ][conversion_col]

        treatment_n = len(treatment_data)
        control_n = len(control_data)

        treatment_conversions = treatment_data.sum()
        control_conversions = control_data.sum()

        treatment_rate = (
            treatment_conversions / treatment_n
            if treatment_n > 0
            else np.nan
        )

        control_rate = (
            control_conversions / control_n
            if control_n > 0
            else np.nan
        )

        difference = treatment_rate - control_rate

        if treatment_n > 0 and control_n > 0:

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

            standard_error = np.sqrt(
                (
                    treatment_rate
                    * (1 - treatment_rate)
                    / treatment_n
                )
                +
                (
                    control_rate
                    * (1 - control_rate)
                    / control_n
                )
            )

            margin_of_error = 1.96 * standard_error

            ci_lower = difference - margin_of_error
            ci_upper = difference + margin_of_error

            relative_lift = (
                difference / control_rate
                if control_rate > 0
                else np.nan
            )

            cohens_h_value = (
                2 * np.arcsin(np.sqrt(treatment_rate))
                -
                2 * np.arcsin(np.sqrt(control_rate))
            )

        else:
            z_stat = np.nan
            p_value = np.nan
            ci_lower = np.nan
            ci_upper = np.nan
            relative_lift = np.nan
            cohens_h_value = np.nan

        results.append({
            segment_col: segment,
            "treatment_users": treatment_n,
            "control_users": control_n,
            "treatment_conversions": treatment_conversions,
            "control_conversions": control_conversions,
            "treatment_rate": treatment_rate,
            "control_rate": control_rate,
            "absolute_difference": difference,
            "relative_lift": relative_lift,
            "z_statistic": z_stat,
            "p_value": p_value,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "cohens_h": cohens_h_value
        })

    return pd.DataFrame(results)


def add_bh_correction(
    results: pd.DataFrame,
    p_value_col: str = "p_value",
    alpha: float = 0.05
) -> pd.DataFrame:
    """Add Benjamini-Hochberg adjusted p-values to segment results."""

    results = results.copy()
    correction = benjamini_hochberg(results[p_value_col].to_numpy(dtype=float), alpha=alpha)

    results["adjusted_p_value"] = correction["adjusted_p_value"].to_numpy()
    results["significant_after_bh"] = correction["significant"].to_numpy()

    return results


def prepare_day_analysis(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Run day-level exploratory treatment-effect analysis.
    """

    results = segment_conversion_analysis(
        df,
        segment_col="most ads day"
    )

    results = add_bh_correction(results)

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    results["most ads day"] = pd.Categorical(
        results["most ads day"],
        categories=day_order,
        ordered=True
    )

    return results.sort_values("most ads day").reset_index(drop=True)


def prepare_hour_analysis(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Run hour-level exploratory treatment-effect analysis.
    """

    results = segment_conversion_analysis(
        df,
        segment_col="most ads hour"
    )

    results = add_bh_correction(results)

    return (
        results
        .sort_values("most ads hour")
        .reset_index(drop=True)
    )