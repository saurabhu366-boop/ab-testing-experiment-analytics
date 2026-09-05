import pandas as pd
from scipy import stats


def check_group_integrity(
    df: pd.DataFrame,
    group_col: str = "test group",
    expected_groups: tuple = ("ad", "psa")
) -> dict:
    """
    Check whether the dataset contains the expected experiment groups.
    """
    groups = sorted(df[group_col].dropna().unique())

    return {
        "valid": tuple(groups) == tuple(sorted(expected_groups)),
        "groups_found": groups,
        "number_of_groups": len(groups)
    }


def check_user_uniqueness(
    df: pd.DataFrame,
    user_col: str = "user id"
) -> dict:
    """
    Check whether each user appears only once.
    """
    total_rows = len(df)
    unique_users = df[user_col].nunique()
    duplicate_rows = total_rows - unique_users

    return {
        "total_rows": total_rows,
        "unique_users": unique_users,
        "duplicate_rows": duplicate_rows,
        "valid": duplicate_rows == 0
    }


def check_conversion_integrity(
    df: pd.DataFrame,
    conversion_col: str = "converted"
) -> dict:
    """
    Check conversion values for missing or unexpected observations.
    """
    missing = df[conversion_col].isna().sum()
    unique_values = df[conversion_col].dropna().unique().tolist()

    valid_values = set(unique_values).issubset({True, False})

    return {
        "missing_values": int(missing),
        "unique_values": unique_values,
        "valid": missing == 0 and valid_values
    }


def calculate_srm(
    df: pd.DataFrame,
    group_col: str = "test group",
    assumed_allocation: dict = None
) -> dict:
    """
    Test for Sample Ratio Mismatch (SRM) against an assumed allocation.

    Important:
    The assumed allocation must come from the experimental design.
    Passing this test does not prove that randomization was correctly
    implemented.
    """
    if assumed_allocation is None:
        assumed_allocation = {
            "ad": 0.96,
            "psa": 0.04
        }

    observed_counts = df[group_col].value_counts()

    groups = list(assumed_allocation.keys())

    observed = [
        observed_counts.get(group, 0)
        for group in groups
    ]

    total = sum(observed)

    expected = [
        total * assumed_allocation[group]
        for group in groups
    ]

    chi_square, p_value = stats.chisquare(
        f_obs=observed,
        f_exp=expected
    )

    observed_allocation = {
        group: observed[i] / total
        for i, group in enumerate(groups)
    }

    return {
        "observed_counts": dict(zip(groups, observed)),
        "expected_counts": dict(zip(groups, expected)),
        "observed_allocation": observed_allocation,
        "chi_square": chi_square,
        "p_value": p_value,
        "significant_srm": p_value < 0.05
    }


def summarize_exposure(
    df: pd.DataFrame,
    group_col: str = "test group",
    exposure_col: str = "total ads"
) -> pd.DataFrame:
    """
    Summarize exposure distribution by experiment group.
    """
    summary = (
        df.groupby(group_col)[exposure_col]
        .agg(
            users="count",
            mean="mean",
            median="median",
            q1=lambda x: x.quantile(0.25),
            q3=lambda x: x.quantile(0.75),
            max="max"
        )
        .reset_index()
    )

    summary["iqr"] = summary["q3"] - summary["q1"]

    return summary