import pandas as pd
import numpy as np
from scipy import stats

def clean(df):
    out = na_handling(df, "remove")

    return out

def na_handling(df, na_strategy="remove", specific_columns=None):
    """
    Handle missing values in a DataFrame based on the specified strategy.

    Parameters:
    df (DataFrame): The input DataFrame.
    na_strategy (str or dict): The strategy to handle missing values. If a string is provided, it will be applied to all columns. If a dictionary is provided, it should contain column names as keys and corresponding strategies as values.
        - "remove": Remove rows with missing values.
        - "mean": Fill missing values with the mean of the column.
        - "median": Fill missing values with the median of the column.
        - "mode": Fill missing values with the mode of the column.
        - "constant": Fill missing values with a constant value ("Unknown").
    specific_columns (list): A list of column names to apply the specified strategy. If None, the strategy will be applied to all columns.

    Returns:
    DataFrame: The DataFrame with missing values handled according to the specified strategy.
    """

    if specific_columns:
        for col in specific_columns:
            strategy = na_strategy[col]
            if strategy == "remove":
                df = df[df[col].notna()]
            elif strategy == "mean":
                df[col] = df[col].fillna(df[col].mean())
            elif strategy == "median":
                df[col] = df[col].fillna(df[col].median())
            elif strategy == "mode":
                df[col] = df[col].fillna(df[col].mode()[0])
            elif strategy == "constant":
                df[col] = df[col].fillna("Unknown")
    else:
        if na_strategy == "remove":
            df = df.dropna()
        elif na_strategy == "mean":
            df = df.fillna(df.mean())
        elif na_strategy == "median":
            df = df.fillna(df.median())
        elif na_strategy == "mode":
            df = df.apply(lambda x: x.fillna(x.mode()[0]) if x.dtype == 'O' else x.fillna(x.median()))
        elif na_strategy == "constant":
            df = df.fillna("Unknown")
    return df




