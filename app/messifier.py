import pandas as pd
import numpy as np

################################################
####### A helper file test data cleaner ########
################################################

def add_missing_values(df, missing_ratio=0.2):
    num_missing_per_column = int(np.ceil(missing_ratio * len(df)))

    # for each col, randomly sample indices to replace with NaN
    for col in df.columns:
        indices = np.random.choice(df.index, num_missing_per_column, replace=False)
        df.loc[indices, col] = np.nan

    return df

def add_duplicates(df, duplicate_ratio=0.1):
    num_duplicates = int(df.shape[0] * duplicate_ratio)
    
    duplicates = df.sample(num_duplicates, replace=True)
    
    df = pd.concat([df, duplicates], ignore_index=True)

    return df

def shuffle_rows(df):
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df
