import seaborn as sns
import matplotlib.pyplot as plt


class Visualization:
    def __init__(self, df, variables, target):
        self.df = df
        self.variables = variables
        self.target = target

        if not self.target:
            self.target = self.df.columns.tolist()[-1]
        if not self.variables:
            self.variables = self.df.columns.tolist()
            self.variables.remove(self.target)

    def plot_all(self):
        self.plot_correlation()
        self.plot_scatter()
        self.plot_box()
        self.plot_histogram()
        self.plot_regression()
        self.plot_kde()

    def plot_correlation(self):
        plt.title("Correlation Heatmap")
        corr = self.df[[self.target] + self.variables].corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        plt.show()

    def plot_scatter(self, x_var=None, y_var=None):
        if not y_var:   
            y_var = self.target

        if x_var:
            plt.title(f"Scatter Plot of {x_var} vs. {y_var}")
            sns.scatterplot(x=x_var, y=y_var, data=self.df)
            plt.show()
        else:
            sns.pairplot(self.df[self.variables + [self.target]])
            plt.show()

    def plot_box(self, variable=None):
        if not variable:
            variable = self.target

        plt.title(f"Box Plot of {variable}")
        sns.boxplot(x=variable, data=self.df)
        plt.show()

    def plot_histogram(self):
        plt.title(f"Histogram of {self.target}")
        sns.histplot(self.df[self.target], kde=True)
        plt.show()

        for var in self.variables:
            plt.title(f"Histogram of {var}")
            sns.histplot(self.df[var], kde=True)
            plt.show()

    def plot_regression(self):
        for var in self.variables:
            plt.title(f"Regression Plot of {var} vs. {self.target}")
            sns.regplot(x=var, y=self.target, data=self.df)
            plt.show()

    def plot_kde(self):
        for var in self.variables:
            plt.title(f"KDE Plot of {var}")
            sns.kdeplot(data=self.df, x=var)
            plt.show()
