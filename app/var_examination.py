import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats

def var_examination(dataset: pd.DataFrame, target: str, figsize: tuple=(20, 2)):
    """
    Perform variable examination on a dataset.

    Parameters:
    dataset (pd.DataFrame): The dataset to be examined.
    target (str): The target variable to be analyzed.
    figsize (tuple): The size of the figure (width, height).

    Returns:
    None
    """

    # Histogram
    sns.histplot(dataset[target], bins=30, kde=True)
    plt.title('Distribution of LSTAT Values')
    plt.xlabel(target)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

    # Box plot 
    sns.boxplot(x=dataset[target])
    plt.title('Box Plot of LSTAT Values')
    plt.xlabel(target)
    plt.grid(True)
    plt.show()

    # Distribution of log-transformed target variable
    # This was suggested, I should maybe figure out why is it relevant?
    sns.histplot(np.log(dataset[target]), bins=30, kde=True)
    plt.title('Distribution of Log-Transformed ' + target + ' Values')
    plt.xlabel('Log of ' + target)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

    # QQ plot to check for normality
    # What does this acutually show?
    stats.probplot(dataset[target], dist="norm", plot=plt)
    plt.title('QQ Plot of LSTAT Values')
    plt.grid(True)
    plt.show()

    correlation_matrix = dataset.corr()

    # Correlation heatmap
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', annot_kws={"size": 8})
    plt.tight_layout()
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

    print(findings)
