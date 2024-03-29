import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import shap

class Visualization:
    def __init__(self, df, variables=None, target=None,model=None, X_test=None,model_type=None):
        self.df = df
        self.target = target if target else self.df.columns.tolist()[-1]
        self.variables = variables if variables else self.df.columns.tolist()

        self.categorical_vars = []
        self.numerical_vars = []
        self.identify_variable_types()

        self.model_type = model_type
        self.model = model
        self.X_test = X_test
        self.shap_values = None
        self.explainer = None
        self.masker = None

        if self.target in self.variables:
            self.variables.remove(self.target)

    def identify_variable_types(self):
        for var in self.variables:
            if pd.api.types.is_numeric_dtype(self.df[var]):
                self.numerical_vars.append(var)
            else:
                self.categorical_vars.append(var)

    def plot_all(self):
        self.plot_correlation()
        self.plot_categorical()
        for var in self.numerical_vars:
            self.plot_scatter(x_var=var)
            self.plot_box(variable=var)
            self.plot_histogram(variable=var)
            self.plot_regression(variable=var)
            self.plot_kde(variable=var)

    def plot_correlation(self):
        plt.title("Correlation Heatmap")

        # Filter only numeric columns for correlation
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()

        # Check if the target variable is numeric and include it if so
        if pd.api.types.is_numeric_dtype(self.df[self.target]):
            selected_cols = [self.target] + [col for col in numeric_cols if col != self.target]
        else:
            selected_cols = numeric_cols

        corr = self.df[selected_cols].corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        plt.show()

    def plot_categorical(self):
        for var in self.categorical_vars:
            unique_values = self.df[var].nunique()
            threshold = 10 # This is an arbitrary value, adjust as necessary   
            if unique_values > threshold:
                print(f"Too many unique values for {var}: {unique_values}. Skipping the count plot.")
                continue
            
            plt.figure(figsize=(10, 5)) # Adjust figure size to fit all labels
            plt.title(f"Count Plot of {var}")
            plt.xticks(rotation=45)
            sns.countplot(x=var, data=self.df)
            plt.tight_layout() # Adjust layout to make room for label rotation
            plt.show()

    def plot_scatter(self, x_var=None, y_var=None):
        if not y_var:
            y_var = self.target

        if x_var:
            plt.title(f"Scatter Plot of {x_var} vs. {y_var}")

            if x_var in self.categorical_vars:
                sns.swarmplot(x=x_var, y=y_var, data=self.df)
            else:
                sns.scatterplot(x=x_var, y=y_var, data=self.df)

            plt.show()
        else:
            sns.pairplot(self.df[self.variables + [self.target]])
            plt.show()

    def plot_box(self, variable=None):
        if variable and variable in self.categorical_vars:
            plt.title(f"Box Plot of {variable} by {self.target}")
            sns.boxplot(x=variable, y=self.target, data=self.df)
        elif variable and variable in self.numerical_vars:
            plt.title(f"Box Plot of {variable}")
            sns.boxplot(y=variable, data=self.df)
        else:
            plt.title(f"Box Plot of {self.target}")
            sns.boxplot(y=self.target, data=self.df)
        plt.show()

    def plot_histogram(self, variable=None):
        if not variable:
            variable = self.target

        plt.title(f"Histogram of {variable}")
        sns.histplot(self.df[variable], kde=True)
        plt.show()

    def plot_regression(self, variable=None):
        if not self.target in self.numerical_vars:
            pass
        elif variable and variable in self.numerical_vars:
            plt.title(f"Regression Plot of {variable} vs. {self.target}")
            sns.regplot(x=variable, y=self.target, data=self.df)
            plt.show()

    def plot_kde(self, variable=None):
        if variable and variable in self.numerical_vars:
            plt.title(f"KDE Plot of {variable}")
            sns.kdeplot(data=self.df, x=variable)
            plt.show()

    def generate_shap_values(self):
        if self.model is None or self.model.model is None:
            raise ValueError("Model has not been trained yet. Call the 'train' method first.")
        if self.model_type == 'linear_regression':
            self.explainer = shap.Explainer(self.model.model, self.X_test)
        elif self.model_type == 'random_forest':
            self.explainer = shap.TreeExplainer(self.model.model, self.X_test)
        elif self.model_type == 'lasso':
            self.explainer = shap.LinearExplainer(self.model.model, self.X_test)
        elif self.model_type == 'ridge':
            self.explainer = shap.LinearExplainer(self.model.model, self.X_test)
        else:
            raise ValueError(f"Unsupported model_type: {self.model_type}")
        
        self.shap_values = self.explainer.shap_values(self.X_test)

    def plot_shap_summary(self):
        if self.shap_values is None:
            raise ValueError("SHAP values have not been generated. Call the 'generate_shap_values' method first.")
        shap.summary_plot(self.shap_values, self.X_test, show=False)
        plt.show()

    def plot_shap_force(self, index):
        if self.shap_values is None:
            raise ValueError("SHAP values have not been generated. Call the 'generate_shap_values' method first.")
        shap.force_plot(self.explainer.expected_value, self.shap_values[index, :], self.X_test.iloc[index, :], show=False,matplotlib=True)
        plt.show()

# ### Example usage 2--------------#
#visualization = Visualization(model=model, X_test=model.X_test)
#visualization.generate_shap_values()
#visualization.plot_shap_summary()
#visualization.plot_shap_force(index=0)