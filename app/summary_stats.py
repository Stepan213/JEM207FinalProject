import pandas as pd

def summary_statistics(df, description_interval="all", decimal_places=2):

    def get_stats(data):
        stats = pd.DataFrame()

        desc_stats = data.describe().round(decimal_places)
        stats = pd.concat([stats, desc_stats.T], axis=1)

        mode_stats = data.mode().iloc[0].round(decimal_places)
        mode_stats.name = 'mode'
        stats = pd.concat([stats, mode_stats], axis=1)

        var_stats = data.var().round(decimal_places)
        var_stats.name = 'variance'
        stats = pd.concat([stats, var_stats], axis=1)

        skew_stats = data.skew().round(decimal_places)
        skew_stats.name = 'skewness'
        stats = pd.concat([stats, skew_stats], axis=1)

        kurtosis_stats = data.kurtosis().round(decimal_places)
        kurtosis_stats.name = 'kurtosis'
        stats = pd.concat([stats, kurtosis_stats], axis=1)

        missing_values_stats = data.isnull().sum()
        missing_values_stats.name = 'missing_values'
        stats = pd.concat([stats, missing_values_stats], axis=1)

        return stats

    # Handling different description intervals
    if description_interval == "all":
        return get_stats(df)
    elif description_interval == "none":
        return pd.DataFrame()
    else:
        all_stats = {}
        for interval in description_interval:
            resampled_data = df.resample(interval).apply(lambda x: x.round(decimal_places))
            all_stats[interval] = get_stats(resampled_data)
        return all_stats