import time
import os
import requests
from dotenv import load_dotenv
from loguru import logger
from twilio.rest import Client

load_dotenv()

TRIGGER_PRICE = int(os.environ['TRIGGER_PRICE'])
CURRENCY = os.environ['CURRENCY']
ACCOUNT_SID = os.environ['ACCOUNT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
PHONE_FROM = os.environ['PHONE_FROM']
PHONE_TO = os.environ['PHONE_TO']


def call(phone_from, phone_to):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    _call = client.calls.create(
        url='http://demo.twilio.com/docs/voice.xml',
        to=phone_to,
        from_=phone_from,
    )

    return _call.sid


def get_price(symbol: str):
    json_data = requests.get(f'https://www.binance.com/api/v3/ticker/price?symbol={symbol.upper()}USDT').json()
    return float(json_data['price'])


def main():
    call_was_made = False
    while True:
        try:
            price = get_price(CURRENCY)
            logger.info(f'{CURRENCY} price is {price}')
            if price < TRIGGER_PRICE:
                if not call_was_made:
                    logger.error('CALLING TO BOSS!!!!11')
                    call(PHONE_FROM, PHONE_TO)
                    call_was_made = True
            else:
                if call_was_made and price > TRIGGER_PRICE * 1.025:
                    call_was_made = False
        except Exception as e:
            logger.error(e)
        time.sleep(30)


if __name__ == '__main__':
    main()
