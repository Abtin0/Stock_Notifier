# Stock News Alert

This Python script fetches stock data for a specific company (Tesla Inc. by default) and sends an SMS alert if there is a significant change in the stock price (greater than 5%). The alert includes a summary of the latest news articles about the company.

## Requirements

- Python 3.x
- Twilio account for SMS notifications
- Alpha Vantage API key for stock data
- News API key for fetching news articles

## Setup

1. **Install required libraries**:
   Install the required Python libraries using `pip`:

   ```bash
   pip install requests twilio
   
2. **Environment variables**: 
    Create a `.env` file in the project directory and add the following environment variables with your credentials:

    ```env
    STOCKS_API_KEY=your_alpha_vantage_api_key
    NEWS_API_KEY=your_news_api_key
    TWILIO_ACCOUNT_SID=your_twilio_account_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    TWILIO_PHONE_NUMBER=your_twilio_phone_number
    USER_PHONE_NUMBER=your_phone_number
    ```

3. **Run the script**: 
The script will fetch the daily stock data for the given stock symbol (TSLA by default) and check if the percentage change in the stock price exceeds 5%. If it does, the script will fetch the latest news articles and send an SMS with the stock change and news summary.

## Run 

1. To run the script, simply execute the following command:
    ```python
    main.py

## How it works

**Fetch stock data**:\
The script uses the Alpha Vantage API to get the daily stock prices for a given stock symbol (e.g., TSLA).

**Check for significant change**:\
It compares the opening price of the stock for the last two days. If the price change exceeds 5%, it proceeds to the next step.

**Fetch news articles**:\
The script uses the News API to fetch the latest news articles related to the company (e.g., Tesla Inc.).

**Send SMS**:\
If the stock change is significant, the script sends an SMS to the user with the percentage change and the latest news articles using the Twilio API.

**Example Message**:\
If the stock price change is greater than 5%, the message will look like this:
```
    TSLA: 🔺 6%

    Bloomberg
    Tesla Stock Soars to New Highs
    Tesla's stock has seen a significant increase after the latest earnings report.

    CNB
    Tesla Announces New Battery Technology
    The new battery technology is expected to reduce costs and improve performance.

    Reuters
    Tesla Faces Supply Chain Issues
    Tesla is struggling to meet production goals due to ongoing supply chain disruptions.
```
## Error Handling
If the stock price change is less than 5%, no SMS will be sent, and the script will print a message indicating this.
In case of data issues or other errors (e.g., network issues), the script will print an error message.
