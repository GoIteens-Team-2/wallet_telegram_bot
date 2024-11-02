import os
import json
import matplotlib.pyplot as plt

from datetime import datetime
from io import BytesIO
from aiogram import Router

from ..enums.DateType import DateType

history_router = Router()


def load_user_transactions(user_id):
    file_path = f"users_transactions/user_{user_id}_data.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []


def filter_transactions_by_date(transactions, start_date, end_date):
    filtered_transactions = []
    for transaction in transactions:
        transaction_date = datetime.strptime(transaction["date"], "%d-%m-%y").date()
        if start_date <= transaction_date <= end_date:
            filtered_transactions.append(transaction)
    return filtered_transactions


def group_transactions(transactions, date_type: DateType):
    if date_type == DateType.DAILY:
        date_filter = "%d-%m-%y"
    elif date_type == DateType.MONTHLY:
        date_filter = "%B %Y"
    else:
        raise TypeError("Incorrect type")
    monthly_income = {}
    monthly_expenses = {}

    for transaction in transactions:
        print(transaction)
        date = datetime.strptime(transaction["date"], "%d-%m-%y")
        month_year = date.strftime(date_filter)

        if transaction["type"] == "income":
            monthly_income[month_year] = (
                monthly_income.get(month_year, 0) + transaction["amount"]
            )
        else:
            monthly_expenses[month_year] = (
                monthly_expenses.get(month_year, 0) + transaction["amount"]
            )

    return monthly_income, monthly_expenses


def generate_transaction_buffer(income, expenses, date_type: DateType):
    if date_type == DateType.DAILY:
        date_filter = "%d-%m-%y"
        date_str = "Daily"
    elif date_type == DateType.MONTHLY:
        date_filter = "%B %Y"
        date_str = "Monthly"
    else:
        raise TypeError("Incorrect type")

    dates = sorted(
        set(list(income.keys()) + list(expenses.keys())),
        key=lambda x: datetime.strptime(x, date_filter),
    )

    income_values = [income.get(date, 0) for date in dates]
    expense_values = [expenses.get(date, 0) for date in dates]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        dates, income_values, width=0.1, label="Income", color="green", align="center"
    )
    ax.bar(
        dates, expense_values, width=0.1, label="Expenses", color="red", align="edge"
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    ax.set_title(f"Income vs Expenses {date_str}")
    ax.legend()
    plt.xticks(rotation=45, ha="right")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    plt.close(fig)

    return buffer
