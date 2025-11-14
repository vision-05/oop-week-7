import pandas as pd

def daily_entries_2_to_monthly():
    """Take daily entries 2 and convert to monthly entry"""
    daily_to_monthly("daily_entries_2.csv", "monthly_balances.csv")
    daily1 = pd.read_csv("daily_entries_1.csv")
    daily2 = pd.read_csv("daily_entries_2.csv")
    pd.merge()
