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

daily_to_monthly()


def load_csv(filepath="daily_entries_total.csv"):
    """ Function to load the "daily_entries_total.csv" CSV file and return  """
    try:
        df = pd.read_csv(filepath, parse_dates=["date"])
        return df
    except FileNotFoundError:
        print("Error: CSV file not found.")
        return None



def plot_all_customer_entries(df, customer):
    """ Function to plots all the entries of the customer given customer name or ID"""

    sub = df[(df["customer_id"] == customer) | (df["customer_name"] == customer)]

    if sub.empty:
        print("No entries found for customer:", customer)
        return

    plt.figure(figsize=(10,5))
    plt.plot(sub["date"], sub["amount"], marker="o")
    plt.title(f"All Entries for Customer: {customer}")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.grid(True)
    plt.show()


def plot_entries_on_day(df, month, day):
    """ Function to plot all entries on the day when given a day of the year"""
    sub = df[(df["date"].dt.month == month) & (df["date"].dt.day == day)]

    if sub.empty:
        raise Exception(f"No entries exist on {month}/{day}")

    plt.figure(figsize=(10,5))
    plt.bar(sub["customer_name"], sub["amount"])
    plt.title(f"Entries on {month}/{day}")
    plt.xlabel("Customer")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.show()


def plot_customer_balance(df, customer):
    """ Function to plot balance of the customer per month (in grouped column bars)"""
    sub = df[(df["customer_id"] == customer) | (df["customer_name"] == customer)]

    if sub.empty:
        print("No entries found for customer:", customer)
        return

    sub["month"] = sub["date"].dt.to_period("M")
    monthly_balance = sub.groupby("month")["amount"].sum()

    plt.figure(figsize=(10,5))
    monthly_balance.plot(kind="bar")
    plt.title(f"Monthly Balance for Customer: {customer}")
    plt.xlabel("Month")
    plt.ylabel("Balance")
    plt.grid(True)
    plt.show()



def plot_all_entries(df, start_date, end_date):
    """ Function to plot all the entires within a period per customer"""
    sub = df[(df["date"] >= pd.to_datetime(start_date)) &
             (df["date"] <= pd.to_datetime(end_date))]

    if sub.empty:
        print("No entries in this date range.")
        return

    plt.figure(figsize=(10,5))
    for customer, group in sub.groupby("customer_name"):
        plt.plot(group["date"], group["amount"], marker="o", label=customer)

    plt.title(f"Entries from {start_date} to {end_date}")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.legend()
    plt.grid(True)
    plt.show()



def plot_negative_transactions(df, start_date, end_date):
    """ Function to plot all negative transactions within period"""
    sub = df[(df["date"] >= pd.to_datetime(start_date)) &
             (df["date"] <= pd.to_datetime(end_date)) &
             (df["amount"] < 0)]

    if sub.empty:
        print("No negative transactions in this period.")
        return

    plt.figure(figsize=(10,5))
    plt.bar(sub["date"], sub["amount"])
    plt.title(f"Negative Transactions from {start_date} to {end_date}")
    plt.xlabel("Date")
    plt.ylabel("Negative Amounts")
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