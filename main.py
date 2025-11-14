import pandas as pd
import random
from matplotlib import pyplot as plt
import calendar
import numpy as np
import model
import view
import controller

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

controller.control("Bank manager", view.plot_all_customer_entries, customer=customer_choice)

controller.control("Customer", view.plot_all_customer_entries, customer=customer_choice)
controller.control("Customer", view.plot_all_customer_entries, customer=1)

controller.control("Data analyst", view.plot_all_customer_entries, customer=customer_choice)
