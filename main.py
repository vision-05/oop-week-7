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


def _compute_day_of_year(df, year=2025):
    """Return a Series with the day-of-year for each row using Month and Day columns.

    - If Month/Day cannot be converted to a valid date, the result will be NaN for that row.
    - Uses the provided `year` (default 2025) because the CSV doesn't include a year column.
    """
    if not set(["Month", "Day"]).issubset(df.columns):
        return pd.Series([pd.NA] * len(df), index=df.index)

    months = pd.to_numeric(df["Month"], errors="coerce")
    days = pd.to_numeric(df["Day"], errors="coerce")
    try:
        dates = pd.to_datetime({"year": year, "month": months, "day": days}, errors="coerce")
        return dates.dt.dayofyear
    except Exception:
        # Fallback: approximate but keep NaN semantics
        return pd.Series([pd.NA] * len(df), index=df.index)



def plot_all_customer_entries(df, customer):
    """ Function to plots all the entries of the customer given customer name or ID"""

    sub = df[(df["CustomerID"] == customer) | (df.get("CustomerName") == customer)]
    if sub.empty:
        print("No entries found for customer:", customer)
        return

    # compute accurate day-of-year using helper
    day_of_year = _compute_day_of_year(sub).fillna(0).astype(int)
    y = pd.to_numeric(sub.get("Balance", pd.Series([0]*len(sub))), errors="coerce").fillna(0)

    plt.figure(figsize=(10,5))
    plt.scatter(day_of_year, y, marker="o")
    plt.title(f"All Entries for Customer: {customer}")
    plt.xlabel("Day of Year")
    plt.ylabel("Balance")
    plt.grid(True)
    plt.show()


def plot_entries_on_day(df, month, day):
    """ Function to plot all entries on the day when given a day of the year"""
    sub = df[(df["Month"]== month) & (df["Day"] == day)]

    plt.figure(figsize=(10,5))
    plt.scatter(sub["CustomerName"], sub["Balance"])
    plt.title(f"Entries on {month}/{day}")
    plt.xlabel("Customer")
    plt.ylabel("Balance")
    plt.xticks(rotation=45)
    plt.show()

def plot_customer_balance(df, customer):
    """ Function to plot balance of the customer per month (in grouped column bars)"""
    sub = df[(df["CustomerID"] == customer) | (df["CustomerName"] == customer)]

    if sub.empty:
        print("No entries found for customer:", customer)
        return

    #sub["month"] = sub["Day"].dt.to_period("M")
    monthly_balance = sub.groupby("Month")["Balance"].sum()

    plt.figure(figsize=(10,5))
    monthly_balance.plot(kind="bar")
    plt.title(f"Monthly Balance for Customer: {customer}")
    plt.xlabel("Month")
    plt.ylabel("Balance")
    plt.grid(True)
    plt.show()



def plot_all_entries(df, start_Day, end_Day):
    """ Function to plot all the entires within a period per customer"""

    # compute day-of-year for entire df and filter by provided start/end (assumed in 1..366)
    doy = _compute_day_of_year(df)
    mask = doy.notna() & (doy >= start_Day) & (doy <= end_Day)
    sub = df[mask].copy()
    if sub.empty:
        print("No entries in this Day range.")
        return

    sub["_day_of_year"] = _compute_day_of_year(sub).astype(int)

    plt.figure(figsize=(10,5))
    for customer, group in sub.groupby("CustomerName"):
        plt.scatter(group["_day_of_year"], group["Balance"], marker="o", label=customer)

    plt.title(f"Entries from {start_Day} to {end_Day}")
    plt.xlabel("Day of Year")
    plt.ylabel("Balance")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_negative_transactions(df, start_Day, end_Day):
    """ Function to plot all negative transactions within period"""

    doy = _compute_day_of_year(df)
    mask = doy.notna() & (doy >= start_Day) & (doy <= end_Day) & (df["Balance"] < 0)
    sub = df[mask].copy()

    if sub.empty:
        print("No negative transactions in this period.")
        return

    sub["_day_of_year"] = _compute_day_of_year(sub).astype(int)

    plt.figure(figsize=(10,5))
    plt.bar(sub["_day_of_year"], sub["Balance"])
    plt.title(f"Negative Transactions from {start_Day} to {end_Day}")
    plt.xlabel("Day of Year")
    plt.ylabel("Negative Balances")
    plt.grid(True)
    plt.show()


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

initial = dataset_crafting()
d2m = daily_to_monthly()
noisy = insert_noise()
d2mnoise = daily_entries_2_to_monthly()

print(initial)
print(d2m)
print(noisy)
print(d2mnoise)
dataset_crafting()
daily_to_monthly()
insert_noise()
daily_entries_2_to_monthly()

# Load the generated CSV once and pick values from the file instead of hard-coding
df = pd.read_csv("daily_entries.csv", skipinitialspace=True)

# choose a customer from the file (prefer CustomerName, fall back to CustomerID)
if "CustomerName" in df.columns and not df["CustomerName"].dropna().empty:
    customer_choice = df["CustomerName"].dropna().unique()[0]
else:
    customer_choice = df["CustomerID"].dropna().unique()[0]

# choose a sample month/day from the file for plotting entries-on-day
if set(["Month", "Day"]).issubset(df.columns) and not df.dropna(subset=["Month", "Day"]).empty:
    sample = df.dropna(subset=["Month", "Day"]).iloc[0]
    sample_month = int(sample["Month"])
    sample_day = int(sample["Day"])
else:
    sample_month, sample_day = 1, 1

plot_all_customer_entries(df, customer_choice)
plot_entries_on_day(df, sample_month, sample_day)
plot_customer_balance(df, customer_choice)
plot_all_entries(df, 0, 365)
plot_negative_transactions(df, 0, 365)
