import os
import json
from datetime import datetime
import matplotlib.pyplot as plt
from aiogram import Router
from io import BytesIO

history_router = Router()

def load_user_transactions(user_id):
    file_path = f'users_transactions/user_{user_id}_data.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

def group_transactions_by_month(transactions):
    monthly_income = {}
    monthly_expenses = {}

    print(transactions)
    for transaction in transactions:
        print(transaction)
        date = datetime.strptime(transaction['date'], "%d-%m-%y")
        month_year = date.strftime("%B %Y")

        if transaction['type'] == 'income':
            monthly_income[month_year] = monthly_income.get(month_year, 0) + transaction['amount']
        else:
            monthly_expenses[month_year] = monthly_expenses.get(month_year, 0) + transaction['amount']

    return monthly_income, monthly_expenses

def generate_monthly_transaction_graph(monthly_income, monthly_expenses):
    months = sorted(set(list(monthly_income.keys()) + list(monthly_expenses.keys())), key=lambda x: datetime.strptime(x, "%B %Y"))

    income_values = [monthly_income.get(month, 0) for month in months]
    expense_values = [monthly_expenses.get(month, 0) for month in months]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(months, income_values, width=0.4, label='Income', color='green', align='center')
    ax.bar(months, expense_values, width=0.4, label='Expenses', color='red', align='edge')

    ax.set_xlabel('Month')
    ax.set_ylabel('Amount')
    ax.set_title('Income vs Expenses by Month')
    ax.legend()
    plt.xticks(rotation=45, ha='right')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    plt.close(fig)

    return buffer


def filter_transactions_by_date(transactions, start_date, end_date):
    filtered_transactions = []
    for transaction in transactions:
        transaction_date = datetime.strptime(transaction['date'], '%d-%m').date()
        if start_date <= transaction_date <= end_date:
            filtered_transactions.append(transaction)
    return filtered_transactions




def group_transactions_by_day(transactions):
    daily_income = {}
    daily_expenses = {}

    for transaction in transactions:
        date = datetime.strptime(transaction["date"], "%d-%m-%y")
        day = date.strftime("%d-%m-%y")

        if transaction['type'] == 'income':
            daily_income[day] = daily_income.get(day, 0) + transaction['amount']
        else:
            daily_expenses[day] = daily_expenses.get(day, 0) + transaction['amount']

    return daily_income, daily_expenses

def generate_daily_transaction_graph(daily_income, daily_expenses):
    days = sorted(set(list(daily_income.keys()) + list(daily_expenses.keys())), key=lambda x: datetime.strptime(x, "%d-%m-%y"))

    income_values = [daily_income.get(day, 0) for day in days]
    expense_values = [daily_expenses.get(day, 0) for day in days]

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(days, income_values, width=0.4, label='Income', color='green', align='center')
    ax.bar(days, expense_values, width=0.4, label='Expenses', color='red', align='edge')

    ax.set_xlabel('Date')
    ax.set_ylabel('Amount')
    ax.set_title('Income vs Expenses by Day')
    ax.legend()
    plt.xticks(rotation=45, ha='right')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    plt.close(fig)

    return buffer