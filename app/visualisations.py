import seaborn as sns
import matplotlib.pyplot as plt


class Visualization:
    def __init__(self, df, variables, target):
        self.df = df
        self.variables = variables
        self.target = target

    def plot_correlation(self):
        corr = self.df[self.variables + [self.target]].corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        plt.show()

    def plot_scatter(self):
        for var in self.variables:
            sns.scatterplot(x=var, y=self.target, data=self.df)
            plt.show()