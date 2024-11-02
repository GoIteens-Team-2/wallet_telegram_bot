import requests
import io
import matplotlib.pyplot as plt
import seaborn as sns

from ..constants import SELECTED_CURRENCIES


def get_currency_rates(currency_type: str = "UAH"):
    response = requests.get(
        f"https://api.exchangerate-api.com/v4/latest/{currency_type}"
    )
    data = response.json()
    rates = {
        k: v
        for k, v in data["rates"].items()
        if k in SELECTED_CURRENCIES and k != currency_type
    }
    return rates


def create_chart(rates, currency_type: str = "UAH"):
    currencies = list(rates.keys())
    values = list(rates.values())

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 7))
    barplot = sns.barplot(x=currencies, y=values, hue=currencies, palette="viridis")

    barplot.set_title(f"Курси валют по відношенню до {currency_type}", fontsize=16)
    barplot.set_xlabel("Валюти", fontsize=14)
    barplot.set_ylabel("Курс", fontsize=14)

    for index, value in enumerate(values):
        barplot.text(
            index, value + 0.5, f"{value:.2f}", ha="center", color="black", fontsize=10
        )

    plt.xticks(rotation=45)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf
