import pandas as pd

def daily_entries_2_to_monthly():
    """Take daily entries 2 and convert to monthly entry"""
    daily_to_monthly("daily_entries_2.csv", "monthly_balances.csv")
    daily1 = pd.read_csv("daily_entries_1.csv")
    daily2 = pd.read_csv("daily_entries_2.csv")
    pd.merge()
    pass

def daily_to_monthly (filename = "dataflow.csv" , outfile = "monthly_balances.csv"):
    # load the daily entries csv file 
    df = pd.read_csv(filename)
    print(df)
    df.groupby("Month")["Balance"].sum()
    print(df.head())
    return df

def insert_noise():
    df2 = daily_to_monthly(filename = "dataflow.csv")


    df2.to_csv("daily_entries_2.csv")