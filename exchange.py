import requests
import logging
import sys
import time
import threading
import json
import os

from flask import Flask
from flask_restful import Resource, Api


logging.basicConfig(filename='history.log', filemode='w', level=logging.DEBUG)

PORT = os.environ.get("PORT", "2222")
HOST = os.environ.get("HOST", "0.0.0.0")
DEBUG_MODE = os.environ.get("DEBUG", True)

last_rate = {}
# mutex = threading.Lock()
bitkub_url = "https://api.bitkub.com/api/market/ticker?sym=THB_BCH"

NEW_RESULT_INTERVAL = 10 # Seconds

class Rates:
    # Stores current rates out of global scope
    def __init__(self):
        self.bitkub_rates = {}

    def get_rate(self):
        return self.bitkub_rates

    def add_rate(self, info):
            self.bitkub_rates = info


# rates class gets passed so thread has access
def start_rate_thread(rates):
    logging.debug("starting")
    rate_thread = threading.Thread(target=rate_fetcher, args=(rates,))
    rate_thread.daemon = True
    rate_thread.start()
    return

# rates class gets passed so thread has access
def rate_fetcher(rates):
    while True:
        rates = rates
        try:
            # get current exchange rate from bitkub
            result = requests.get(bitkub_url)
            logging.debug("grabbing new rate:")
            logging.debug(f"result: {result.json()}")
            rates.add_rate(result.json())
        except Exception as err:
            logging.debug(f"An error occurred: {err}")
            pass
        finally:
            time.sleep(NEW_RESULT_INTERVAL)

    

class GetRate(Resource):
    def __init__(self, **kwargs):
        self.rates = kwargs["rates"]

    def get(self, amount, denomination):
        # Format in docs
        return {"thb-bch": self.rates.get_rate()}
    


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

api.add_resource(GetRate, '/api/get_rate/<amount>/<denomination>', resource_class_kwargs={
        "rates": rates})

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE,
        host=HOST,
        port=PORT) 