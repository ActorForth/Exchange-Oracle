import pytest
import json
import unittest
from unittest import mock
from unittest.mock import mock_open



from src.exchange import (
    Rates,
    bitkub_url,
    usd_exchange_rate_url,
    app,
    rates
)

from tests.samples import (
    thb_rate_json,
)



    
class Tests:
    def test_get_rate(self):
        rates = Rates()
        
        thb_rate = {
                    "last": thb_rate_json["THB_BCH"]["last"],
                    "raw": thb_rate_json,
                    "from": bitkub_url
                }
        rates.add_rate("thb", thb_rate)
        
        assert rates.get_rate("thb") == thb_rate


    def test_denomination_not_found(self):
        rates = Rates()
        
        assert rates.get_rate("not_found") == None
    
    
    def test_denomination_not_available(self):
            
        # denomination = "thb"
        url = f"/api/get_rate/THB"
        
        flask_app = app
        with flask_app.test_client(self) as test_client:
            
            response = test_client.get(url, content_type="application/json")
            result = json.loads(response.get_data(as_text=True))
            
            assert response.status_code == 404
            assert result == {'message': 'This denomination is not available'}

    def test_get_thb(self):
            
        # denomination = "thb"
        url = f"/api/get_rate/THB"
        
        thb_rate = {
                    "last": 20000,
                    "multiplier": 100,
                    "timestamp": 2000000
                }
        
        rates.add_rate("THB", thb_rate)
        
        flask_app = app
        with flask_app.test_client(self) as test_client:
            
            response = test_client.get(url, content_type="application/json")
            result = json.loads(response.get_data(as_text=True))
            
            assert response.status_code == 200
            assert result == thb_rate
            