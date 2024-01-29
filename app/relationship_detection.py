import pandas as pd
import numpy as np
from scipy.stats import pearsonr, chi2_contingency
from itertools import combinations
from sklearn.preprocessing import LabelEncoder

def calculate_correlation(col1, col2):
    # Pearson's r for continuous-continuous
    return pearsonr(col1, col2)[0]

def cramers_v(col1, col2):
    # Cramer's V for categorical-categorical
    confusion_matrix = pd.crosstab(col1, col2)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    return np.sqrt(phi2 / min((k-1), (r-1)))

def detect_column_type(column):
    # Heuristic to detect column type
    if pd.api.types.is_numeric_dtype(column):
        return 'numerical'
    elif pd.api.types.is_categorical_dtype(column) or pd.api.types.is_object_dtype(column):
        return 'categorical'
    return 'unknown'

def analyze_relationships(df):
    columns = df.columns
    relationships = {}

    for col1, col2 in combinations(columns, 2):
        type1, type2 = detect_column_type(df[col1]), detect_column_type(df[col2])
        
        if type1 == 'numerical' and type2 == 'numerical':
            corr = calculate_correlation(df[col1], df[col2])
            relationships[(col1, col2)] = ('numerical-numerical', corr)

        elif type1 == 'categorical' and type2 == 'categorical':
            le = LabelEncoder()
            encoded_col1, encoded_col2 = le.fit_transform(df[col1]), le.fit_transform(df[col2])
            cv = cramers_v(encoded_col1, encoded_col2)
            relationships[(col1, col2)] = ('categorical-categorical', cv)

        # Add more cases as needed (e.g., numerical-categorical, etc.)

    return relationships

# Example Usage
# df = pd.read_csv("your_data.csv")
# relationship_summary = analyze_relationships(df)
# for pair, (type_pair, value) in relationship_summary.items():
#     print(f"Relationship between {pair[0]} and {pair[1]} ({type_pair}): {value}")
