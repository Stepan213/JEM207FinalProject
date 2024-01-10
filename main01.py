from sklearn import datasets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import app.var_examination as ve
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV, train_test_split, GridSearchCV
from skopt import BayesSearchCV
import shap
shap.initjs()


def read_file(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        print("Invalid file format. Only CSV and XLSX files are supported.")

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

#na_strategy = input("Choose NA handling strategy: remove, mean, median, or keep: ")
def na_handling(df, na_strategy):
    if na_strategy == "remove":
        df = df.dropna()
    elif na_strategy == "mean":
        df = df.fillna(df.mean())
    elif na_strategy == "median":
        df = df.fillna(df.median())
    elif na_strategy == "keep":
        pass
    else:
        print("Invalid NA handling strategy. Please choose 'remove', 'mean', 'median', or 'keep'.")

    return df
#description_interval = ["all", "none", variable names]
def summary_statistics(df, description_interval):
    if description_interval == "all":
        print(df.describe())
    elif description_interval == "none":
        pass
    else:
        for i in range(len(description_interval)):
            print(df.resample(description_interval[i]).describe())

#Hyperparameter tuning

def random_search(X_train, Y_train, model, hyperpar_grid, cv, n_iter, random_state):
    random_search = RandomizedSearchCV(estimator=model, param_distributions=hyperpar_grid, n_iter=n_iter, cv=cv,
                                       verbose=2, random_state=random_state, n_jobs=-1,scoring='neg_mean_squared_error')
    random_search.fit(X_train, Y_train)
    best_params = random_search.best_params_
    best_model = random_search.best_estimator_

    return best_params, best_model

def grid_search(X_train, Y_train, model, hyperpar_grid, cv):
    grid_search = GridSearchCV(estimator=model, param_grid=hyperpar_grid,scoring='neg_mean_squared_error' ,cv=cv, verbose=2, n_jobs=-1)
    grid_search.fit(X_train, Y_train)
    best_params = grid_search.best_params_
    best_model = grid_search.best_estimator_

    return best_params, best_model

def bayesian_search(X_train, Y_train, model, hyperpar_grid,n_iter, cv, random_state):
    bayesian_search = BayesSearchCV(estimator=model, search_spaces=hyperpar_grid,scoring='neg_mean_squared_error' ,n_iter=n_iter, cv=cv, verbose=2, random_state=random_state, n_jobs=-1)
    bayesian_search.fit(X_train, Y_train)
    best_params = bayesian_search.best_params_
    best_model = bayesian_search.best_estimator_

    return best_params, best_model


#Model evaluation

def Linear_regression(df, variables,target, test_size, random_state):
    X = df[variables]
    Y = df['target']
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=random_state)
    model = LinearRegression()
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)

    return Y_pred, Y_test

def Random_forest(df, hyperpar_method, variables, target,test_size, random_state):
    pass

def Laso_regression():
    pass

def Ridge_regression():
    pass