import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import matplotlib.dates as mdates

from datetime import datetime, timedelta
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

    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(14, 7))

    bar_width = 0.35
    income_bars = ax.bar(
        [datetime.strptime(date, date_filter) for date in dates], 
        income_values, 
        width=bar_width, 
        label="Income", 
        color=sns.color_palette("crest", as_cmap=True)(0.6), 
        edgecolor="black", 
        linewidth=0.6
    )
    expense_bars = ax.bar(
        [datetime.strptime(date, date_filter) + timedelta(days=15) for date in dates],
        expense_values, 
        width=bar_width, 
        label="Expenses", 
        color=sns.color_palette("flare", as_cmap=True)(0.6), 
        edgecolor="black", 
        linewidth=0.6
    )

    for bar in income_bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2, 
            bar.get_height(), 
            f'{bar.get_height():,.0f}', 
            ha='center', 
            va='bottom', 
            fontsize=10
        )

    for bar in expense_bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2, 
            bar.get_height(), 
            f'{bar.get_height():,.0f}', 
            ha='center', 
            va='bottom', 
            fontsize=10
        )

    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Amount", fontsize=12)
    ax.set_title(f"Income vs Expenses ({date_str})", fontsize=16, weight='bold')
    ax.legend(loc="upper left", fontsize=10)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y' if date_type == DateType.MONTHLY else '%d-%m-%y'))
    plt.xticks(rotation=45, ha="right")

    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)

    plt.close(fig)

    return buffer