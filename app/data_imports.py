import pandas as pd

def convert_to_dataframe(file_path, file_format):

    if file_format == 'pandas':
        return pd.read_pickle(file_path)
    elif file_format == 'csv':
        return pd.read_csv(file_path)
    elif file_format == 'txt':
        return pd.read_table(file_path)
    elif file_format == 'excel':
        return pd.read_excel(file_path)
    else:
        raise ValueError('Unsupported file format')

# Example usage
data_frame = convert_to_dataframe('/path/to/file.csv', 'csv')
