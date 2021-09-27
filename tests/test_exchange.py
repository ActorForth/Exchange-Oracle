import pytest
import json

from src.exchange import (
    Rates,
    bitkub_url,
    usd_exchange_rate_url,
)

from tests.samples import (
    thb_rate_json,
)




def test_get_rate():
    rates = Rates()
    
    thb_rate = {
                "last": thb_rate_json["THB_BCH"]["last"],
                "raw": thb_rate_json,
                "from": bitkub_url
            }
    
    rates.add_rate("thb", thb_rate)
    
    assert rates.get_rate("thb") == thb_rate

def test_denomination_not_found():
    rates = Rates()
    
    assert rates.get_rate("not_found") == None