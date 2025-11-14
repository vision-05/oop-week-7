import pandas as pd
import random
from matplotlib import pyplot as plt
import calendar
import numpy as np



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

def plot_all_customer_entries(df, **kwargs):
    """ Function to plots all the entries of the customer given customer name or ID"""
    customer = kwargs.get("customer", None)

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


def plot_entries_on_day(df, **kwargs):
    """ Function to plot all entries on the day when given a day of the year"""
    month = kwargs.get("month", None)
    day = kwargs.get("day", None)

    sub = df[(df["Month"]== month) & (df["Day"] == day)]

    plt.figure(figsize=(10,5))
    plt.scatter(sub["CustomerName"], sub["Balance"])
    plt.title(f"Entries on {month}/{day}")
    plt.xlabel("Customer")
    plt.ylabel("Balance")
    plt.xticks(rotation=45)
    plt.show()

def plot_customer_balance(df, **kwargs):
    """ Function to plot balance of the customer per month (in grouped column bars)"""
    customer = kwargs.get("customer", None)
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



def plot_all_entries(df, **kwargs):
    """ Function to plot all the entires within a period per customer"""
    start_day = kwargs.get("start_day", None)
    end_day = kwargs.get("end_day", None)

    # compute day-of-year for entire df and filter by provided start/end (assumed in 1..366)
    doy = _compute_day_of_year(df)
    mask = doy.notna() & (doy >= start_day) & (doy <= end_day)
    sub = df[mask].copy()
    if sub.empty:
        print("No entries in this Day range.")
        return

    sub["_day_of_year"] = _compute_day_of_year(sub).astype(int)

    plt.figure(figsize=(10,5))
    for customer, group in sub.groupby("CustomerName"):
        plt.scatter(group["_day_of_year"], group["Balance"], marker="o", label=customer)

    plt.title(f"Entries from {start_day} to {end_day}")
    plt.xlabel("Day of Year")
    plt.ylabel("Balance")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_negative_transactions(df, **kwargs):
    """ Function to plot all negative transactions within period"""
    start_day = kwargs.get("start_day", None)
    end_day = kwargs.get("end_day", None)

    doy = _compute_day_of_year(df)
    mask = doy.notna() & (doy >= start_day) & (doy <= end_day) & (df["Balance"] < 0)
    sub = df[mask].copy()

    if sub.empty:
        print("No negative transactions in this period.")
        return

    sub["_day_of_year"] = _compute_day_of_year(sub).astype(int)

    plt.figure(figsize=(10,5))
    plt.bar(sub["_day_of_year"], sub["Balance"])
    plt.title(f"Negative Transactions from {start_day} to {end_day}")
    plt.xlabel("Day of Year")
    plt.ylabel("Negative Balances")
    plt.grid(True)
    plt.show()

def get_data(df, perm, **kwargs):
    name = kwargs.get("name", None)
    print(f"perm {perm} name {name}")
    if perm == 0:
        return df
    elif perm == 1:
        return df.loc[df["CustomerName"] == name]
    elif perm == 2:
        return df.drop(columns=["CustomerName"])
