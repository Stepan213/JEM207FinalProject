
import pandas as pd

def read_file(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.json'):
        df = pd.read_json(file_path)
    else:
        print("Invalid file format. CSV, XLSX and JSON files are supported.")

    return df

def import_from_api(api_url):
    # Add code to import data from API
    pass

def import_data(data_source):
    if data_source == "file":
        file_path = input("Enter the file path: ")
        df = read_file(file_path)
    elif data_source == "api":
        api_url = input("Enter the API URL: ")
        df = import_from_api(api_url)
    else:
        print("Invalid data source. Please choose 'file' or 'api'.")
    if df.empty:
        print("No data was imported.")

    return df
