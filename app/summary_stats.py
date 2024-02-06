import pandas as pd

def numeric_statistics(df, decimal_places=2):
    data = df.select_dtypes(include='number')

    desc_stats = data.describe().round(decimal_places)
    
    additional_stats = pd.DataFrame(index=desc_stats.columns)
    
    additional_stats['mode'] = data.mode().iloc[0].round(decimal_places)
    additional_stats['variance'] = data.var().round(decimal_places)
    additional_stats['skewness'] = data.skew().round(decimal_places)
    additional_stats['kurtosis'] = data.kurtosis().round(decimal_places)
    additional_stats['missing_values'] = data.isnull().sum()
    
    return pd.concat([desc_stats.T, additional_stats], axis=1)

def categorical_statistics(df):
    data = df.select_dtypes(include='object')

    # Check if data is empty
    if data.empty:
        return pd.DataFrame()

    stats = pd.DataFrame(index=data.columns)

    stats['unique_values'] = data.nunique()

    # Safely get mode
    mode_df = data.mode()
    if mode_df.empty:
        stats['mode'] = None
        stats['frequency_of_mode'] = None
    else:
        stats['mode'] = mode_df.iloc[0]
        stats['frequency_of_mode'] = data.apply(lambda x: x.value_counts().iloc[0] if not x.empty else None)

    stats['missing_values'] = data.isnull().sum()

    return stats
