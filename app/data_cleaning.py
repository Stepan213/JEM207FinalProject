import pandas as pd


def clean(df):
    out = na_handling(df, "remove")

    return out

def na_handling(df, na_strategy):
    if na_strategy == "remove":
        df = df.dropna()
    elif na_strategy == "mean":
        df = df.fillna(df.mean())
    elif na_strategy == "median":
        df = df.fillna(df.median())
    else:
        pass

    return df