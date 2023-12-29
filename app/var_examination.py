import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats

def var_examination(dataset: pd.DataFrame, target: str):

    # TODO correlation heatmap "unviversalisation"

    # Distribution plot using histplot
    plt.figure(figsize=(8, 2))
    sns.histplot(dataset[target], bins=30, kde=True)
    plt.title('Distribution of LSTAT Values')
    plt.xlabel(target)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

    # Box plot to identify outliers
    plt.figure(figsize=(10, 2))
    sns.boxplot(x=dataset[target])
    plt.title('Box Plot of LSTAT Values')
    plt.xlabel(target)
    plt.grid(True)
    plt.show()

    dataset['LOG_LSTAT'] = np.log(dataset[target])

    # Distribution of log-transformed LSTAT
    plt.figure(figsize=(10, 2))
    sns.histplot(dataset['LOG_LSTAT'], bins=30, kde=True)
    plt.title('Distribution of Log-Transformed LSTAT Values')
    plt.xlabel('Log of LSTAT')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

    # QQ plot to check for normality
    plt.figure(figsize=(10, 2))
    stats.probplot(dataset[target], dist="norm", plot=plt)
    plt.title('QQ Plot of LSTAT Values')
    plt.grid(True)
    plt.show()

    correlation_matrix = dataset[[target, 'LOG_LSTAT', 'RM', 'AGE']].corr()

    # Correlation heatmap
    plt.figure(figsize=(4, 4))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.show()

    skewness = dataset[target].skew()
    kurtosis = dataset[target].kurt()

    basic_stats = dataset[target].describe()
    findings = {
        'Basic Statistics': basic_stats.round(2),
        'Skewness': skewness.round(2),
        'Kurtosis': kurtosis.round(2),
        'Correlation with RM': correlation_matrix.loc[target, 'RM'].round(2),
        'Correlation with AGE': correlation_matrix.loc[target, 'AGE'].round(2)
    }

    findings
