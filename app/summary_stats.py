
def summary_statistics(df, description_interval = "all"):
    if description_interval == "all":
        print(df.describe())
    elif description_interval == "none":
        pass
    else:
        for i in range(len(description_interval)):
            print(df.resample(description_interval[i]).describe())
