import pandas as pd
import numpy as np
from scipy import stats

class DataCleaner:
    def __init__(self, df):
        self.df = df
        self.log = []

    def clean(self):
        self.df = self.na_handling("remove")
        self.df = self.remove_duplicates()

        return self.df

    def na_handling(self, na_strategy="remove", specific_columns=None):
        """
        Handle missing values in the DataFrame based on the specified strategy.
        """
        initial_shape = self.df.shape
        initial_na_count = self.df.isna().sum().sum()
        self.log.append(f"na_handling: There are {initial_na_count} missing values in the DataFrame.")

        if specific_columns:
            for col in specific_columns:
                strategy = na_strategy[col]
                self.apply_strategy(col, strategy)
        else:
            if na_strategy == "remove":
                removed_rows = self.df.isna().any(axis=1).sum()
                self.df = self.df.dropna()
                self.log.append(f"na_handling: Removed {removed_rows} rows with missing values.")
            else:
                self.apply_strategy_to_all(na_strategy)

        final_shape = self.df.shape
        final_na_count = self.df.isna().sum().sum()
        replaced_count = initial_na_count - final_na_count

        self.log.append(f"na_handling: Changed from {initial_shape} to {final_shape}. "
                        f"Replaced {replaced_count} missing values using strategy '{na_strategy}'.")

        if initial_na_count > 0:
            percentage_replaced = (replaced_count / initial_na_count) * 100
            self.log.append(f"na_handling: Replaced {percentage_replaced:.2f}% of the total missing values.")

        return self.df

    def apply_strategy(self, col, strategy):
        initial_na_count = self.df[col].isna().sum()

        if strategy == "remove":
            removed_rows = self.df[col].isna().sum()
            self.df = self.df[self.df[col].notna()]
            self.log.append(f"Column '{col}': Removed {removed_rows} rows with missing values.")
        elif strategy in ["mean", "median", "mode"]:
            self.df[col] = self.df[col].fillna(self.get_replacement_value(col, strategy))
            self.log.append(f"Column '{col}': Replaced {initial_na_count} missing values with {strategy}.")
        elif strategy == "constant":
            self.df[col] = self.df[col].fillna("Unknown")
            self.log.append(f"Column '{col}': Replaced {initial_na_count} missing values with 'Unknown'.")

    def apply_strategy_to_all(self, strategy):
        for col in self.df.columns:
            if self.df[col].isna().any():
                self.apply_strategy(col, strategy)

    def get_replacement_value(self, col, strategy):
        if strategy == "mean":
            return self.df[col].mean()
        elif strategy == "median":
            return self.df[col].median()
        elif strategy == "mode":
            return self.df[col].mode()[0]
        
    def remove_duplicates(self):
        initial_shape = self.df.shape

        self.df = self.df.drop_duplicates()

        final_shape = self.df.shape
        removed_duplicates = initial_shape[0] - final_shape[0]

        self.log.append(f"remove_duplicates: Changed from {initial_shape} to {final_shape}. "
                        f"Removed {removed_duplicates} duplicate rows.")

        return self.df

    def get_log(self):
        return "\n".join(self.log)
