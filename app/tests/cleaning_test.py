import unittest
import pandas as pd
import numpy as np
from app.data_cleaning import DataCleaner

class TestDataCleaner(unittest.TestCase):

    def setUp(self):
        self.data = {
            "A": [1, np.nan, 3, 4, 5, 5],
            "B": ["a", "b", "b", np.nan, "e", "e"],
            "C": [1, 2, 3, 4, np.nan, np.nan]
        }
        self.df = pd.DataFrame(self.data)
        self.cleaner = DataCleaner(self.df)

    def test_remove_duplicates(self):
        cleaned_df = self.cleaner.remove_duplicates()
        self.assertEqual(cleaned_df.shape[0], self.df.drop_duplicates().shape[0])

    def test_na_handling_remove(self):
        cleaned_df = self.cleaner.na_handling("remove")
        self.assertTrue(cleaned_df.isna().sum().sum() == 0)

    def test_clean(self):
        cleaned_df = self.cleaner.clean()
        self.assertTrue(cleaned_df.isna().sum().sum() == 0)
        self.assertEqual(cleaned_df.shape[0], self.df.dropna().drop_duplicates().shape[0])

    def test_apply_strategy_mean(self):
        self.cleaner.apply_strategy("A", "mean")
        self.assertFalse(self.cleaner.df["A"].isna().any())

if __name__ == '__main__':
    unittest.main()
