import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

st.title("Bipul/Aaku Mortgage Payments Calculator")

st.write("### Enter your home details here...")
col1, col2 = st.columns(2)
home_value = col1.number_input("Purchase Price", min_value=0, value=350000)
down_pay = col1.number_input("Down Payments", min_value=0, value=30000)
interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.1, value=6.7)
loan_term = col2.number_input("Loan Term (in years)", min_value=1, value=30)

# Loan Calculations
loan_amount = home_value - down_pay
mth_int_rate = (interest_rate / 100) / 12
mth_payments = loan_term * 12

# Monthly Payment Formula
monthly_payment = (
    loan_amount
    * (mth_int_rate * (1 + mth_int_rate) ** mth_payments)
    / ((1 + mth_int_rate) ** mth_payments - 1)
)

# Display Metrics
total_payments = mth_payments * monthly_payment
total_interest = total_payments - loan_amount

st.write("### Payments")
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Payments", value=f"${monthly_payment:,.2f}")
col2.metric(label="Total Paid in Full", value=f"${total_payments:,.0f}")
col3.metric(label="Total Interest Paid", value=f"${total_interest:,.0f}")

# Create Amortization Schedule
schedule = []
rem_balance = loan_amount

for i in range(1, mth_payments + 1):
    interest_payment = rem_balance * mth_int_rate
    principal_payment = monthly_payment - interest_payment
    rem_balance -= principal_payment
    year = math.ceil(i / 12)
    schedule.append([i, monthly_payment, principal_payment, interest_payment, rem_balance, year])

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"]
)

# 📊 Improved Visualization: Dual-Axis Plot
st.write("### Mortgage Amortization Schedule")

fig, ax1 = plt.subplots(figsize=(10, 5))

# Left Y-Axis (Remaining Balance)
ax1.plot(df["Month"], df["Remaining Balance"], label="Remaining Balance", color="blue", linestyle="dashed", linewidth=2, zorder=3)
ax1.set_xlabel("Months")
ax1.set_ylabel("Remaining Balance ($)", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

# Right Y-Axis (Principal & Interest Payments)
ax2 = ax1.twinx()
ax2.fill_between(df["Month"], df["Principal"], color="green", alpha=0.5, label="Principal Payment")
ax2.fill_between(df["Month"], df["Interest"] + df["Principal"], df["Principal"], color="red", alpha=0.5, label="Interest Payment")
ax2.set_ylabel("Principal & Interest Payments ($)", color="black")

# Labels and Legends
ax1.set_title("Mortgage Amortization Schedule", fontsize=14)
fig.legend(loc="upper right")

st.pyplot(fig)
