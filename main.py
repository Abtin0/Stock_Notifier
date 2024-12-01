from twilio.rest import Client
import requests
from datetime import datetime, timedelta
import os

# Constants
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCKS_API_URL = "https://www.alphavantage.co/query"
NEWS_API_URL = "https://newsapi.org/v2/everything"

# Environment variables for sensitive data
STOCKS_API_KEY = os.getenv("STOCKS_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
USER_PHONE_NUMBER = os.getenv("USER_PHONE_NUMBER")

# Helper function to calculate percentage change
def change_percentage(yesterday_price, day_before_yesterday_price):
    percentage_change = ((yesterday_price - day_before_yesterday_price) / day_before_yesterday_price) * 100
    emoji = "🔺" if percentage_change > 0 else "🔻"
    return emoji, round(abs(percentage_change))

# Fetch stock data
def fetch_stock_data(stock_symbol):
    params = {
        "apikey": STOCKS_API_KEY,
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_symbol,
    }
    response = requests.get(STOCKS_API_URL, params=params)
    response.raise_for_status()
    return response.json()

# Fetch news articles
def fetch_news_articles(company_name):
    params = {"q": company_name, "apiKey": NEWS_API_KEY}
    response = requests.get(NEWS_API_URL, params=params)
    response.raise_for_status()
    return response.json()

# Main function
def main():
    try:
        # Dates
        yesterday = (datetime.now() - timedelta(days=1)).date()
        before_yesterday = (datetime.now() - timedelta(days=2)).date()

        # Stock data
        stocks_data = fetch_stock_data(STOCK)
        daily_prices = stocks_data["Time Series (Daily)"]
        opening_y = float(daily_prices[str(yesterday)]["1. open"])
        opening_before = float(daily_prices[str(before_yesterday)]["1. open"])

        # Check significant change
        emoji, percentage = change_percentage(opening_y, opening_before)
        if percentage >= 5:
            news_data = fetch_news_articles(COMPANY_NAME)
            articles = news_data["articles"][:3]

            # Prepare news body
            news_body = "\n\n".join(
                f"{article['source']['name']}\n{article['title']}\n{article['description']}"
                for article in articles
            )

            # Message body
            message_body = f"{STOCK}: {emoji} {percentage}%\n\n{news_body}"

            # Send SMS
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                from_=TWILIO_PHONE_NUMBER,
                to=USER_PHONE_NUMBER,
                body=message_body,
            )
            print(f"Message sent: {message.sid}")
        else:
            print("Stock change less than 5%. No message sent.")
    except KeyError as e:
        print(f"Data issue: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
