import pandas as pd
import matplotlib.pyplot as plt

PAGE_FAULT_MAX = 20000

# load csv data from a local file or an url
def  load_data(csv_file):
    df = pd.read_csv(csv_file, sep=";").dropna()
    return df

# get max value from latest 10 data points
def get_max10(df):
    return df["Value"].tail(10).max()

# generate box plot for analysis
def create_boxplot(df, output, format="png"):
    fig = plt.figure()
    bp = df.boxplot(column=["Value"])
    fig.savefig(output, format=format)

# generate notification based thresholds
def notification(csv_file):
    df = load_data(csv_file)
    max_value = get_max10(df)
    if not max_value:
        return "Not enough data!\n"
    if ("page_fault" in csv_file) and (max_value > float(PAGE_FAULT_MAX)):
        return "Too many page faults, consider reducing memory use\n"
    # add more rules for other SGX metrics here
    
# Test
df = load_data("page_faults.csv").tail(10)
#print(df.head(10))
#print(df.dtypes)
#print(df.info())
#print(max(df["Value"].astype("int")))
#print(df["Value"].max())
#print(get_max10(df))
#print(notification("page_faults.csv"))
create_boxplot(df, "page_faults.png")