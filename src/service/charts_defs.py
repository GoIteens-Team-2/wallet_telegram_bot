import matplotlib.pyplot as plt
import requests
import io

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