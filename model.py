import pandas as pd
import random
from matplotlib import pyplot as plt
import calendar
import numpy as np

def dataset_crafting():
    n_customers = 15
    n_rows = 50
    customer_names = [f"Customer_{i+1}" for i in range(n_customers)]
    customer_ids = random.sample(range(1000, 9999), n_customers)
    customers = list(zip(customer_names, customer_ids))
    if n_rows > n_customers:
        # sample with replacement to allow more rows than unique customers
        idx = random.choices(range(n_customers), k=n_rows)
    else:
        # sample without replacement when possible
        idx = random.sample(range(n_customers), n_rows)
    # Build dataset
    records = []
    for i in idx:
        name, cust_id = customers[i]
        # Pick a random year-month pair
        year = 2025
        month = random.randint(1, 12)
        # Random valid day in that month
        day = random.randint(1, calendar.monthrange(year, month)[1])
        # Random value between -15.00 and 15.00
        amount = round(random.uniform(-15, 15), 2)
        records.append([name, cust_id, day, month, amount])
    # Create DataFrame
    df = pd.DataFrame(records, columns=["CustomerName", "CustomerID", "Day", "Month", "Balance"])
    # Save CSV
    df.to_csv("daily_entries.csv", index=False)
    return df

def daily_to_monthly (filename = "daily_entries.csv" , outfile = "monthly_balances.csv"):
    # load the daily entries csv file 
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return

    # Ensure required columns exist
    required = {"CustomerID", "Month", "Balance"}
    if not required.issubset(set(df.columns)):
        print("Input file is missing required columns. Found:", df.columns.tolist())
        return

    # Convert Balance to numeric (coerce errors -> NaN) and drop invalid rows
    df["Balance"] = pd.to_numeric(df["Balance"], errors="coerce")
    df = df.dropna(subset=["Balance"])

    # If CustomerName exists, keep it using first() when grouping
    if "CustomerName" in df.columns:
        grouped = df.groupby(["CustomerID", "Month"], as_index=False).agg({
            "CustomerName": "first",
            "Balance": "sum",
        })
        # Reorder columns for readability
        grouped = grouped[["CustomerName", "CustomerID", "Month", "Balance"]]
    else:
        grouped = df.groupby(["CustomerID", "Month"], as_index=False)["Balance"].sum().reset_index()

    # Save aggregated monthly balances
    grouped.to_csv(outfile, index=False)
    print(f"Wrote {len(grouped)} rows to {outfile}")
    print(grouped)
    return grouped

def daily_entries_2_to_monthly():
    """Take daily entries 2 and convert to monthly entry"""
    daily_to_monthly("daily_entries_2.csv", "monthly_balances.csv")
    daily1 = pd.read_csv("daily_entries_2.csv", skipinitialspace=True)
    daily2 = pd.read_csv("daily_entries.csv", skipinitialspace=True)
    daily1.merge(daily2, on="CustomerName", how="outer")
    
    daily_tot = pd.concat([daily1,daily2]).groupby(["CustomerID","CustomerName","Month","Day"]).sum()
    daily_tot.to_csv("daily_total.csv")
    return daily_tot


def load_csv(filepath="daily_entries_total.csv"):
    """ Function to load the "daily_entries_total.csv" CSV file and return  """
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print("Error: CSV file not found.")
        return None




def insert_noise(noise_frac=0.1):
    "Insert random NaN values at random positions"
    df2 = load_csv("daily_entries.csv")
    
    num_noisy_cells = int(df2.shape[0]*df2.shape[1] * noise_frac)
    
    # Generate random indices for cells to replace
    for _ in range(num_noisy_cells):
        random_row = random.randint(0, df2.shape[0]-1)
        random_col = random.randint(0, df2.shape[1]-1)
        df2.iloc[random_row, random_col] = np.nan
    df2.to_csv("daily_entries_2.csv", index=False)
    return df2