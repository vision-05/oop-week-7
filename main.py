import pandas as pd
import random

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
    "Insert random NaN values at random positions"
    df2 = daily_to_monthly(filename = "dataflow.csv")
    num_noisy_cells = int(df2.shape[0]*df2.shape[1] * 0.1)
    
    # Generate random indices for cells to replace
    for _ in range(num_noisy_cells):
        random_row = random.randint(0, df2.shape[0])
        random_col = random.randint(0, df2.shape[1])
        df2.iloc[random_row, random_col] = float("nan")
    
    df2.to_csv("daily_entries_2.csv")
    return df2