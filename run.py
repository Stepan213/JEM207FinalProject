import os
from app import data_imports
from app import data_cleaning
from app import summary_stats

def main():
    
    filepath = input("Enter the filepath: ")

    df = data_imports.read_file(filepath)

    df = data_cleaning.clean(df)

    summary_stats.summary_statistics(df)

    # models TODO

    # visualisations TODO