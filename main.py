import pandas as pd

def daily_entries_2_to_monthly():
    """Take daily entries 2 and convert to monthly entry"""
    #daily_to_monthly("dataflow.csv", "monthly_balances.csv")
    daily1 = pd.read_csv("dataflow.csv")
    daily2 = pd.read_csv("daily_2.csv")
    print(daily1)
    print(daily2)
    daily1.merge(daily2, on="Customer_Name", how="outer")
    daily_tot = daily1.groupby(["Customer_Id","Month", "Day"]).sum()
    print(daily_tot)
    pass

def daily_to_monthly (filename = "dataflow.csv" , outfile = "monthly_balances.csv"):
    # load the daily entries csv file 
    df = pd.read_csv(filename)
    print(df)
    df.groupby(by=["Month"], as_index=False)
    print(df.head())

daily_entries_2_to_monthly()