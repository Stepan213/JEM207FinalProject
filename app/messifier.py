import pandas as pd
import numpy as np

################################################
####### A helper file test data cleaner ########
################################################

def add_missing_values(df, missing_ratio):
    # Calculate the number of missing values to add
    num_missing = int(df.size * missing_ratio)
    
    # Randomly choose indices to add missing values
    indices = np.random.choice(df.size, num_missing, replace=False)
    
    # Set the chosen indices to NaN
    df.values.flat[indices] = np.nan
    
    return df

def add_duplicates(df, duplicate_ratio):
    # Calculate the number of duplicates to add
    num_duplicates = int(df.shape[0] * duplicate_ratio)
    
    # Sample rows from the dataframe to create duplicates
    duplicates = df.sample(num_duplicates, replace=True)
    
    # Concatenate the duplicates with the original dataframe
    df = pd.concat([df, duplicates], ignore_index=True)
    
    return df

def shuffle_rows(df):
    # Shuffle the rows of the dataframe
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df
