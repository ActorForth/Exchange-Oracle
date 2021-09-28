import requests
import logging
import sys
import time
import threading
import json
import os

from flask import Flask
from flask_restful import Resource, Api

from decimal import Decimal

logging.basicConfig(filename='history.log', filemode='w', level=logging.DEBUG)

PORT = os.environ.get("PORT", "2222")
HOST = os.environ.get("HOST", "0.0.0.0")
DEBUG_MODE = os.environ.get("DEBUG", True)

last_rate = {}
# mutex = threading.Lock()
bitkub_url = "https://api.bitkub.com/api/market/ticker?sym=THB_BCH"
usd_exchange_rate_url = "https://cex.io/api/ticker/BCH/USD"

NEW_RESULT_INTERVAL = 10 # Seconds

class Rates:
    # Stores current rates out of global scope
    def __init__(self):
        self.rates = {}

    def get_rate(self, denomination):
        return self.rates.get(denomination, None)

    def add_rate(self, denomination, info):
            self.rates[denomination] = info


# rates class gets passed so thread has access
def start_rate_thread(rates): # pragma: no cover
    logging.debug("starting")
    rate_thread = threading.Thread(target=rate_fetcher, args=(rates,))
    rate_thread.daemon = True
    rate_thread.start()
    return

# rates class gets passed so thread has access
def rate_fetcher(rates): # pragma: no cover
    while True:
        rates = rates
        try:
            # get current exchange rate from bitkub
            thb_result = requests.get(bitkub_url)
            usd_result = requests.get(usd_exchange_rate_url)
            logging.debug("grabbing new rate:")
            logging.debug(f"result: {thb_result.json()}")
            logging.debug(f"result: {usd_result.json()}")
            
            thb_json = thb_result.json()
            usd_json = usd_result.json()
            
            thb_rate = {
                "last": int(Decimal(str(thb_json["THB_BCH"]["last"])) * 100),
                "multiplier": 100,
                "raw": thb_json,
                "from": bitkub_url,
                "timestamp": int(time.time())
            }
            
            usd_rate = {
                "last": int(Decimal(str(usd_json["last"])) * 100),
                "multiplier": 100,
                "raw": usd_json,
                "from": usd_exchange_rate_url,
                "timestamp": int(usd_json["timestamp"])
            }
            
            rates.add_rate("THB", thb_rate)
            rates.add_rate("USD", usd_rate)
        except Exception as err:
            logging.debug(f"An error occurred: {err}")
            pass
        finally:
            time.sleep(NEW_RESULT_INTERVAL)

    

class GetRate(Resource):
    def __init__(self, **kwargs):
        self.rates = kwargs["rates"]

    def get(self, denomination):
        # Format in docs
        rate = self.rates.get_rate(denomination)
        if not rate:
            return {"message": "This denomination is not available"}, 404
        
        result = {
            "last": rate["last"],
            "multiplier": rate["multiplier"],
            "timestamp": rate["timestamp"]
        }
        
        return result, 200


class Exchange(Flask):  # pragma: no cover
    def run(
        self,
        host=None,
        port=None,
        debug=None,
        load_dotenv=True,
        ev_list=None,
        **options,
    ):
        if not self.debug or os.getenv("WERKZEUG_RUN_MAIN") == "true":
            with self.app_context():
                pass

            super(Exchange, self).run(
                host=host,
                port=port,
                debug=debug,
                load_dotenv=load_dotenv,
                **options
            )


rates = Rates()
start_rate_thread(rates)

app = Exchange(__name__)
api = Api(app)

api.add_resource(GetRate, '/api/get_rate/<denomination>', resource_class_kwargs={
        "rates": rates})

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE,
        host=HOST,
        port=PORT) 