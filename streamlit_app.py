import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

from IPython.core.pylabtools import figsize

st.title("Bipul/Aaku, Mortgage Payments Calculator")

st.write("### Enter your home details here...")
col1, col2 = st.columns(2)
home_value = col1.number_input("Purchase Price", min_value=0, value= 350000)
down_pay = col1.number_input("Down Payments", min_value=0, value= 30000)
interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.1, value=6.7)
loan_term = col2.number_input("Loan Term (in years)", min_value=1, value=30)

# calculate the payments formula

loan_amount = home_value - down_pay
mth_int_rate = ( interest_rate / 100 ) / 12
mth_payments = loan_term * 12

monthly_payment = (
    loan_amount
    * (mth_int_rate * (1 + mth_int_rate) ** mth_payments)
    / ((1 + mth_int_rate) ** mth_payments - 1)
)

# display the repayments

total_payments = mth_payments * monthly_payment
total_interest = total_payments - loan_amount

st.write("### Payments")
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Payments", value=f"${monthly_payment:,.2f}")
col2.metric(label="Total Paid in Full", value=f"${total_payments:,.2f}")
col3.metric(label="Total Interest Paid", value=f"${total_interest:,.2f}")

# create a data frame with the payment schedule

schedule = []

rem_balance = loan_amount

for i in range(1, mth_payments +1):
    interest_payment = rem_balance * mth_int_rate
    principal_payment = monthly_payment - interest_payment
    rem_balance -= principal_payment
    year = math.ceil(i / 12) # this calculates the year into the loan.
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            rem_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"]
)

# display the data-frame as a chart

st.write("### Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payments_df)


fig, ax = plt.subplots(figsize=(10,5))

ax.plot(df['Month'], df['Remaining Balance'], label= 'Remaining Balance', color= 'blue')

ax.plot(df['Month'], df['Principal'], label= 'Principal Payment', color= 'green')
ax.plot(df['Month'], df['Interest'], label= 'Interest Payment', color= 'red')

ax.set_xlabel("Months")
ax.set_ylabel("Amount ($)")
ax.set_title("Mortgage Amortization Schedule")
ax.legend()

st.pyplot(fig)


