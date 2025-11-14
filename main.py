import pandas as pd
import random
from matplotlib import pyplot as plt
import calendar

def daily_entries_2_to_monthly():
    """Take daily entries 2 and convert to monthly entry"""
    daily_to_monthly("daily_entries_2.csv", "monthly_balances.csv")
    daily1 = pd.read_csv("daily_entries_1.csv")
    daily2 = pd.read_csv("daily_entries_2.csv")
    pd.merge()
    pass

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
    Balance = round(random.uniform(-15, 15), 2)
    records.append([name, cust_id, day, month, Balance])
    # Create DataFrame
    df = pd.DataFrame(records, columns=["CustomerName", "CustomerID", "Day", "Month", "Balance"])
    # Save CSV
    #df.to_csv("daily_entries.csv", index=False)
    #print(df.head())

dataset_crafting()

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

daily_to_monthly()


def load_csv(filepath="daily_entries_total.csv"):
    """ Function to load the "daily_entries_total.csv" CSV file and return  """
    try:
        df = pd.read_csv(filepath, parse_Days=["Day"])
        return df
    except FileNotFoundError:
        print("Error: CSV file not found.")
        return None



def plot_all_customer_entries(df, customer):
    """ Function to plots all the entries of the customer given customer name or ID"""

    sub = df[(df["CustomerID"] == customer) | (df["CustomerName"] == customer)]
    if sub.empty:
        print("No entries found for customer:", customer)
        return
    plt.figure(figsize=(10,5))
    sub2 = [sub["Month"]*30+sub["Day"]]
    #plt.scatter(sub["Day"], sub["Balance"], marker="o")
    plt.scatter(sub2, sub2, marker="o")
    plt.title(f"All Entries for Customer: {customer}")
    plt.xlabel("Day")
    plt.ylabel("Balance")
    plt.grid(True)
    plt.show()

plot_all_customer_entries(pd.read_csv("daily_entries.csv"),"Customer_12")

def plot_entries_on_day(df, month, day):
    """ Function to plot all entries on the day when given a day of the year"""
    sub = df[(df["Month"]== month) & (df["Day"] == day)]

    if sub.empty:
        raise Exception(f"No entries exist on {month}/{day}")

    plt.figure(figsize=(10,5))
    plt.scatter(sub["CustomerName"], sub["Balance"])
    plt.title(f"Entries on {month}/{day}")
    plt.xlabel("Customer")
    plt.ylabel("Balance")
    plt.xticks(rotation=45)
    plt.show()

plot_entries_on_day(pd.read_csv("daily_entries.csv"),7,21)

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

plot_customer_balance(pd.read_csv("daily_entries.csv"),"Customer_12")

def plot_all_entries(df, start_Day, end_Day):
    """ Function to plot all the entires within a period per customer"""
    sub = df[((df["Month"]*30+df["Day"]) >= pd.to_Daytime(start_Day)) &
             ((df["Month"]*30+df["Day"]) <= pd.to_Daytime(end_Day))]

    if sub.empty:
        print("No entries in this Day range.")
        return

    plt.figure(figsize=(10,5))
    for customer, group in sub.groupby("CustomerName"):
        plt.scatter(group["Day"], group["Balance"], marker="o", label=customer)

    plt.title(f"Entries from {start_Day} to {end_Day}")
    plt.xlabel("Day")
    plt.ylabel("Balance")
    plt.legend()
    plt.grid(True)
    plt.show()

plot_all_entries(pd.read_csv("daily_entries.csv"),0,365)

def plot_negative_transactions(df, start_Day, end_Day):
    """ Function to plot all negative transactions within period"""
    sub = df[(df["Day"] >= pd.to_Daytime(start_Day)) &
             (df["Day"] <= pd.to_Daytime(end_Day)) &
             (df["Balance"] < 0)]

    if sub.empty:
        print("No negative transactions in this period.")
        return

    plt.figure(figsize=(10,5))
    plt.bar(sub["Day"], sub["Balance"])
    plt.title(f"Negative Transactions from {start_Day} to {end_Day}")
    plt.xlabel("Day")
    plt.ylabel("Negative Balances")
    plt.grid(True)
    plt.show()



    df = load_csv()

    plot_all_customer_entries(df, "John Doe")
    plot_entries_on_day(df, month=3, day=15)
    plot_customer_balance(df, 42)
    plot_all_entries(df, "2024-01-01", "2024-02-01")
    plot_negative_transactions(df, "2024-03-01", "2024-03-31")


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
