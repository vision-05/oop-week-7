import pandas as pd
import matplotlib.pyplot as plt


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
    
    sub = daily_df[(daily_df["CustomerId"] == customer) |
                   (daily_df["CustomerName"] == customer)]

    if sub.empty:
        print("No entries found for customer:", customer)
        return

    # Convert to datetime
    sub["date"] = pd.to_datetime(
        {"year": 2024, "month": sub["Month"], "day": sub["Day"]}
    )

    plt.figure(figsize=(10,5))
    plt.plot(sub["date"], sub["Balance"], marker="o")
    plt.title(f"Daily Entries for Customer: {customer}")
    plt.xlabel("Date")
    plt.ylabel("Balance")
    plt.grid(True)
    plt.show()


def plot_entries_on_day():
    """ Function to plot all entries on the day when given a day of the year"""
    pass


def plot_customer_balance():
    """ Function to plot balance of the customer per month (in grouped column bars)"""
    pass



def plot_all_entries():
    """ Function to plot all the entires within a period per customer"""
    pass



def plot_negative_transactions():
    """ Function to plot all negative transactions within period"""
    pass



df = load_csv()

plot_all_customer_entries(df, "John Doe")
plot_entries_on_day(df, month=3, day=15)
plot_customer_balance(df, 42)
plot_all_entries(df, "2024-01-01", "2024-02-01")
plot_negative_transactions(df, "2024-03-01", "2024-03-31")