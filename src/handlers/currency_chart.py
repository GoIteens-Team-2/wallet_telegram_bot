import matplotlib.pyplot as plt
import requests
import io
from aiogram import Router, F
import numpy as np
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
from aiogram.types import Message

currency_chart_router = Router()

def get_currency_rates():
    response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    data = response.json()
    return data['rates']

def create_chart(rates):
    currencies = list(rates.keys())
    values = list(rates.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(currencies, values)
    plt.xticks(rotation=45)
    plt.title('Курси валют по відношенню до USD')
    plt.xlabel('Валюти')
    plt.ylabel('Курс')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf




@currency_chart_router.message(F.text == "/currencyChart")
async def show_balance(message, update):
    def currency(update):
        rates = get_currency_rates()
        chart_buf = create_chart(rates)
        update.message.reply_photo(photo=chart_buf)
    await message.answer(currency())

