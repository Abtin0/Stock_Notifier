from twilio.rest import Client
import requests
from datetime import *

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCKS_API_KEY = "YBFA8NAHGA1DXQCQ"
stocks_endpoint = "https://www.alphavantage.co/query?"
stocks_params = {
    "apikey": STOCKS_API_KEY,
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK
}
news_endpoint = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "d9a9f18e39ff4e50b7368a3cb0e3dc46"
news_params = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
}
account_sid = "AC8d1e6921377ea53ef02cd970c1b0d813"
auth_token = "81427fb98b4fd53272d222300b8016dc"
client = Client(account_sid, auth_token)


def change_percentage(yesterday_price, day_before_yesterday_price):
    percentage_change = ((yesterday_price - day_before_yesterday_price) / day_before_yesterday_price) * 100
    if percentage_change > 0:
        return "🔺", round(abs(percentage_change))
    if percentage_change < 0:
        return "🔻", round(abs(percentage_change))


yesterday = (datetime.now() - timedelta(days=1)).date()
before_yesterday = (datetime.now() - timedelta(days=2)).date()

stocks_r = requests.get(stocks_endpoint, params=stocks_params)
if stocks_r.status_code != 200:
    raise Exception("Failed to fetch stock data")
try:
    stocks_data: dict = stocks_r.json()
    daily_prices = stocks_data["Time Series (Daily)"]
except KeyError:
    raise Exception("Failed to fetch stock data. You have used your free daily 25 requests.")

try:
    opening_y = float(daily_prices[str(yesterday)]["1. open"])
    opening_before = float(daily_prices[str(before_yesterday)]["1. open"])

    if change_percentage(opening_y, opening_before)[1] >= 5:
        news_data: dict = requests.get(news_endpoint, params=news_params).json()
        if news_data.status_code != 200:
            raise Exception("Failed to fetch stock data")
        articles = news_data["articles"]
        news_body = ""
        for i in range(3):
            publisher = articles[i]["source"]["name"]
            title = articles[i]["title"]
            description = articles[i]["description"]
            news_body += f"{publisher}\n{title}\n{description}\n\n"
        emoji, percentage = change_percentage(opening_y, opening_before)
        message_body = f"{STOCK}: {str(emoji)} {str(percentage)}%\n\n" + news_body

except KeyError:
    print("NASDAQ was closed yesterday or the day before")

message = client.messages.create(
    from_="+17753805686",
    to="+16476739180",
    body=message_body
)
