import smtplib
import requests
from datetime import date, timedelta

stock = "TSLA"
company = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API_STOCK = "4ZF58316XF8U38KO"
API_NEWS = "e7e14c8af3d442b0a1a3ea9a963207f0"

SENDER_EMAIL = "email to send from"
PASSWORD = "password to ^ email"


def getPrice(stock):
    stock_parameters = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": stock,
        "apikey": API_STOCK,
    }

    stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
    stock_response.raise_for_status()
    stock_data = stock_response.json()

    # 1 day ago stock price
    one_day_ago = date.today() - timedelta(days=1)
    price_one_day = stock_data["Time Series (Daily)"][str(one_day_ago)]["4. close"]

    # 2 days ago stock price
    two_day_ago = date.today() - timedelta(days=2)
    price_two_day = stock_data["Time Series (Daily)"][str(two_day_ago)]["4. close"]

    price_change = abs(float(price_one_day) - float(price_two_day))

    change_percent = (price_change / float(price_one_day)) * 100
    if change_percent > 4:
        return True


def getNews(company):
    news_parameters = {
        "apikey": API_NEWS,
        "qInTitle": company,
        "language": "en",
        "sortBy": "publishedAt",
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    three_newest_articles = news_data[:3]
    print(three_newest_articles)

    formatted_email = [f"Headline: {article['title']}. \n"
                       f" Brief: {article['description']} "
                       for article in three_newest_articles]

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=SENDER_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=SENDER_EMAIL,
                            to_addrs="email to send message to",
                            msg=f"Subject:STOCK INFORMATION \n\n"
                                f"{formatted_email[0]}\n"
                                f"{formatted_email[1]}\n"
                                f"{formatted_email[2]}")
        connection.close()


if getPrice(stock):
    getNews(company)
else:
    print("No change")

