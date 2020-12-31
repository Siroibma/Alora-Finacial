#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import plotly.express as px
import pandas as pd
import requests
import sys
from alpha_vantage.timeseries import TimeSeries

key = 'VG7VFW3TBRFINU4E'


def calc_Tbond(amount, years, interest):
    with open('TreasuryBond.csv', 'w', newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['Total', 'Years'])
        total = amount
        semi_annual_amount = years * 2

        for x in range(0, semi_annual_amount):
            thewriter.writerow([total, x])
            total = total * interest
    df = pd.read_csv('TreasuryBond.csv')
    fig = px.bar(df, x='Years', y='Total', title='Loan Duration')
    fig.show()
    return round(total, 2)


def loan_Payment(monthly_payment, amount, interest):
    with open('LoanPayment.csv', 'w', newline='') as f:

        thewriter = csv.writer(f)
        thewriter.writerow(['Total', 'Month Number'])
        total = amount
        month_increments = 0
        while total > 0:
            thewriter.writerow([total, month_increments])
            total = total - monthly_payment
            if total > 0:
                total = total + total * (interest / 100)
            month_increments += 1
    df = pd.read_csv('LoanPayment.csv')
    fig = px.bar(df, x='Month Number', y='Total', title='Loan Duration')
    fig.show()
    return month_increments


def loan_term_payment(term, amount, interest):
    periodic = interest / 12
    term_in_months = term * 12
    monthly_payment = round(10000 / round(((1 + periodic)
                            ** term_in_months - 1) / (periodic * (1
                            + periodic) ** term_in_months), 2), 2)
    loan_term_payment_graph(monthly_payment, term_in_months, amount,
                            periodic)
    return monthly_payment


def loan_term_payment_graph(monthly_payment,term,amount,interest):
    with open('LoanTermPayment.csv', 'w', newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['Amount Remaining', 'Month'])
        month_increments = 0
        total = amount
        for x in range(0, term):
            thewriter.writerow([total, month_increments])
            total = total - monthly_payment
            if total > 0:
                total = total + total * (interest / 100)
            else:
                break
            month_increments += 1
    df = pd.read_csv('LoanTermPayment.csv')
    fig = px.bar(df, x='Month', y='Amount Remaining',
                 title='Loan Duration')
    fig.show()


def stock_handler(symbol):
    base_url = 'https://www.alphavantage.co/query?'

    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'datatype': 'csv',
        'apikey': key,
        }

    response = requests.get(base_url, params=params)

    with open('stock.csv', 'wb') as file:
        file.write(response.content)

    df = pd.read_csv('stock.csv')
    df.set_index('timestamp', inplace=True)
    df = pd.read_csv('stock.csv')

    fig = px.line(df, x='timestamp', y='high')
    fig.show()


def latest_change(filename):
    df = pd.read_csv(filename)
    percent_change = 0

    # print(df.head(3))

    if df.iloc[1, 0] - df.iloc[0, 0] > 0:
        percent_change = round(df.iloc[1, 0] / df.iloc[0, 0] - 1, 4)
        print (percent_change)
        return 'Increasing'
    elif df.iloc[1, 0] - df.iloc[0, 0] == 0:
        percent_change = round(df.iloc[1, 0] / df.iloc[0, 0] - 1, 4)
        print (percent_change)
        return 'No Change'
    elif df.iloc[1, 0] - df.iloc[0, 0] < 0:
        percent_change = round(df.iloc[1, 0] / df.iloc[0, 0] - 1, 4)
        print (percent_change)
        return 'Decreasing'


# Function Name : calc_CollegeLoan
# Parameters: unsub_amount, unsub_time, sub_amount, sub_time, interest
# Purpose: Given two different types of loans "unsub/sub" we calculate the interest accrued and total
# amount of debt we are in

def calc_CollegeLoan(unsub_amount,unsub_time,sub_amount,sub_time,interest):
    unsub_total = unsub_amount
    sub_total = sub_amount
    print (sub_total)
    for x in range(0, sub_time):
        sub_total = sub_total * interest
        print (sub_total)
    for y in range(0, unsub_time):
        unsub_total = unsub_total * interest
    return sub_total + unsub_total


def main():

    # x = calc_Tbond(1000,30, 1.05)
    # x = latest_change('LoanPayment.csv')
    # x = loan_term_payment(7, 10000, .03)
    # print(x)
    # print(sys.path)

    stock_handler('GOOG')


if __name__ == '__main__':
    main()
