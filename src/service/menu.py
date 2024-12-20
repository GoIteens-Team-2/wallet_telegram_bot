from aiogram.types import BotCommand

menu = [
    BotCommand(command='help', description="Коротенько по командам"),
    BotCommand(command='income', description="прибуток"),
    BotCommand(command='expense', description="витрата"),
    BotCommand(command='history_incomes', description="історія прибутків"),
    BotCommand(command='history_expenses', description="історія витрат"),
    BotCommand(command='history_from_to', description="історія з-до"),
    BotCommand(command='history_from_date', description="історія транзакцій які були виконані у певну дату"),
    BotCommand(command='history_plot_monthly', description="графік транзакцій(помісячно)"),
    BotCommand(command='history_plot_day', description="графік транзакцій(поденно)"),
    BotCommand(command='exchange', description="обміняти свої кошти або введені"),
    BotCommand(command='currency_chart', description="подивитись курс валют"),
    BotCommand(command='balance', description="подивитись свій баланс"),
]   