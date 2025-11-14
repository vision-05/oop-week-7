import pandas as pd

def daily_entries_2_to_monthly(filename):
    """Take daily entries 2 and convert to monthly entry"""
    pass

def daily_to_monthly (filename = "dataflow.csv" , outfile = "monthly_balances.csv"):
    # load the daily entries csv file 
    df = pd.read_csv(filename)
    df.groupby("Month")["Balance"].sum()
    print(df.head())