import requests
import matplotlib.pyplot as plt
import io
import seaborn as sns
from src.handlers.currency_chart import currencys_types



def get_currency_rates(currency_type: str = currencys_types):
    response = requests.get(
        f"https://api.exchangerate-api.com/v4/latest/{currency_type}"
    )
    data = response.json()
    selected_currencies = {
        "UAH",
        "USD",
        "PLN",
        "EUR",
    }

    rates = {
        k: v
        for k, v in data["rates"].items()
        if k in selected_currencies and k != currency_type
    }
    return rates


def create_chart(rates, currency_type: str = currencys_types):
    currencies = list(rates.keys())
    values = list(rates.values())
    
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 7))
    barplot = sns.barplot(x=currencies, y=values, palette="viridis")
    
    barplot.set_title(f"Курси валют по відношенню до {currency_type}", fontsize=16)
    barplot.set_xlabel("Валюти", fontsize=14)
    barplot.set_ylabel("Курс", fontsize=14)
    
    for index, value in enumerate(values):
        barplot.text(index, value + 0.5, f"{value:.2f}", ha='center', color="black", fontsize=10)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf