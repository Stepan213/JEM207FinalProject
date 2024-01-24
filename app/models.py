from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso, Ridge
from sklearn.metrics import mean_squared_error
from skopt import BayesSearchCV
import numpy as np


class RegressionModel:
    def __init__(self, model_type='random_forest', hyperpar_grid=None, cv=5, n_iter=10, random_state=None):
        self.model_type = model_type
        self.hyperpar_grid = hyperpar_grid
        self.cv = cv
        self.n_iter = n_iter
        self.random_state = random_state
        self.model = None
        self.best_params = None
        self.X_train = None
        self.X_test = None
        self.Y_train = None
        self.Y_test = None

    def split_data(self, df, variables, target, test_size=0.2):
        X = df[variables]
        Y = df[target]
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(X, Y, test_size=test_size, random_state=self.random_state)

    def _random_search(self):
        if self.hyperpar_grid is not None:
            random_search = RandomizedSearchCV(estimator=self.model, param_distributions=self.hyperpar_grid,
                                               n_iter=self.n_iter, cv=self.cv, verbose=2,
                                               random_state=self.random_state, n_jobs=-1, scoring='neg_mean_squared_error')
            random_search.fit(self.X_train, self.Y_train)
            self.best_params = random_search.best_params_
            self.model = random_search.best_estimator_

    def _grid_search(self):
        if self.hyperpar_grid is not None:
            grid_search = GridSearchCV(estimator=self.model, param_grid=self.hyperpar_grid,
                                       cv=self.cv, verbose=2, n_jobs=-1, scoring='neg_mean_squared_error')
            grid_search.fit(self.X_train, self.Y_train)
            self.best_params = grid_search.best_params_
            self.model = grid_search.best_estimator_

    def _bayesian_optimization(self):
        if self.hyperpar_grid is not None:
            bayesian_opt = BayesSearchCV(estimator=self.model, search_spaces=self.hyperpar_grid,
                                         n_iter=self.n_iter, cv=self.cv, verbose=2, n_jobs=-1, scoring='neg_mean_squared_error')
            np.int = int
            bayesian_opt.fit(self.X_train, self.Y_train)
            self.best_params = bayesian_opt.best_params_
            self.model = bayesian_opt.best_estimator_

    def train(self, search_method='random_search'):
        if self.model_type == 'random_forest':
            self.model = RandomForestRegressor(random_state=self.random_state)
        elif self.model_type == 'lasso':
            self.model = Lasso(random_state=self.random_state)
        elif self.model_type == 'ridge':
            self.model = Ridge(random_state=self.random_state)
        else:
            raise ValueError("Invalid model type. Supported types: 'random_forest', 'lasso', 'ridge'.")

        if self.X_train is None or self.Y_train is None or self.X_test is None or self.Y_test is None:
            raise ValueError("Data not split. Call the 'split_data' method first.")

        if search_method == 'random_search':
            self._random_search()
        elif search_method == 'grid_search':
            self._grid_search()
        elif search_method == 'bayesian_optimization':
            self._bayesian_optimization()
        else:
            raise ValueError("Invalid search method. Supported methods: 'random_search', 'grid_search', 'bayesian_optimization'.")

    def predict(self, X_test=None):
        if self.model is None:
            raise ValueError("Model has not been trained yet. Call the 'train' method first.")

        if X_test is None:
            X_test = self.X_test

        return self.model.predict(X_test)

    def evaluate(self, Y_test=None, X_test=None):
        if self.model is None:
            raise ValueError("Model has not been trained yet. Call the 'train' method first.")

        if Y_test is None or X_test is None:
            Y_test = self.Y_test
            X_test = self.X_test

        predictions = self.predict(X_test)
        mse = mean_squared_error(Y_test, predictions)
        return mse
    
    def feature_importance(self, X_test=None):
        if self.model is None:
            raise ValueError("Model has not been trained yet. Call the 'train' method first.")

        if X_test is None:
            X_test = self.X_test

        return self.model.feature_importances_

### Example usage ----------------------------#
X, Y = make_regression(n_samples=100, n_features=2, noise=0.1, random_state=42)
df = pd.DataFrame({'Feature1': X[:, 0], 'Feature2': X[:, 1], 'Target': Y})

model = RegressionModel(model_type='random_forest', hyperpar_grid={'n_estimators': [10,20,30,150], 'max_depth': [None, 10, 20,30]},cv = 10, n_iter=15, random_state=42)
model.split_data(df, variables=['Feature1', 'Feature2'], target='Target', test_size=0.2)
model.train(search_method='bayesian_optimization')

mse = model.evaluate()
print(f"Mean Squared Error: {mse}")
#---------------------------------------------#