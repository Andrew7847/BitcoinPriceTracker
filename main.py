
import requests
import time
from datetime import datetime

API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_URL = 'https://maker.ifttt.com/trigger/{}/with/key/rKR1cBiXbAoBwhP8vY_U5'

PRICE_THRESHOLD = 20000


def get_latest_bitcoin_price():
    response = requests.get(API_URL)
    response_json = response.json()
    return float(response_json[0]['price_usd'])


def post_ifttt_webhook(event, value):
    # The payload that will be sent to IFTTT service
    data = {'value1': value}
    # Inserts our desired event
    ifttt_event_url = IFTTT_URL.format(event)
    # Sends a HTTP POST request to the webhook URL
    requests.post(ifttt_event_url, json=data)


def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string: '24.02.2018 15:09'
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    return '<br>'.join(rows)


def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # Send an emergency notification
        if price < PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        # Send a Telegram notification
        # Once we have 5 items in our bitcoin_history send an update
        if len(bitcoin_history) == 5:
            post_ifttt_webhook('bitcoin_price_update',
                               format_bitcoin_history(bitcoin_history))
            # Reset the history
            bitcoin_history = []

        # Sleep for 30 minutes
        time.sleep(1800)


if __name__ == '__main__':
    main()
