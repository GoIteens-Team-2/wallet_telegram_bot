import requests
import matplotlib.pyplot as plt
import io


def get_currency_rates(currency_type: str = "USD"):
    response = requests.get(
        f"https://api.exchangerate-api.com/v4/latest/{currency_type}"
    )
    data = response.json()
    return data["rates"]


def create_chart(rates):
    currencies = list(rates.keys())
    values = list(rates.values())

    plt.figure(figsize=(10, 6))
    plt.bar(currencies, values)
    plt.xticks(rotation=45)
    plt.title("Курси валют по відношенню до USD")
    plt.xlabel("Валюти")
    plt.ylabel("Курс")
    plt.tight_layout()
    plt.show()
    # plt.close()

    # buf = io.BytesIO()
    # plt.savefig(buf, format="png")
    # plt.close()
    # buf.seek(0)
    # return buf


if __name__ == "__main__":
    rate_data = get_currency_rates("UAH")
    print(rate_data)
    # print(create_chart(rate_data).getvalue())
