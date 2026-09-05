import pandas as pd


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the raw marketing A/B testing dataset.

    Parameters
    ----------
    filepath : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.
    """
    return pd.read_csv(filepath)


def remove_exported_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove the sequential exported index column if present.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.

    Returns
    -------
    pd.DataFrame
        Dataset without the exported index.
    """
    df = df.copy()

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the project's approved data-cleaning steps.

    Only the exported index is removed. Other observations,
    including extreme total_ads values, are retained because
    no evidence was found that they were invalid.
    """
    df_clean = remove_exported_index(df)

    return df_clean