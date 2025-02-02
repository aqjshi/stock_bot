import pytz
import requests

from decouple import config
from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlencode
from datetime import datetime
from decimal import Decimal

ALPHA_VANTAGE_API_KEY = config("ALPHA_VANTAGE_API_KEY", default=None, cast=str)

def transform_stock_result(timestamp_str, result):
    # unix_timestamp = result.get('t') / 1000.0
    # utc_timestamp = datetime.fromtimestamp(unix_timestamp, tz=pytz.timezone('UTC'))
    timestamp_format = '%Y-%m-%d %H:%M:%S' 
    eastern = pytz.timezone("US/Eastern")
    utc = pytz.utc
    timestamp = eastern.localize(datetime.strptime(timestamp_str,timestamp_format)).astimezone(utc)
    return {
        'open_price': Decimal(result['1. open']),
        'close_price': Decimal(result['4. close']),
        'high_price': Decimal(result['2. high']),
        'low_price': Decimal(result['3. low']),
        'number_of_trades': None,
        'volume': int(result['5. volume']),
        'volume_weighted_average': None,
        'raw_timestamp': timestamp_str,
        'time': timestamp,
    }

def transform_sma_result(timestamp_str, result):
    # unix_timestamp = result.get('t') / 1000.0
    # utc_timestamp = datetime.fromtimestamp(unix_timestamp, tz=pytz.timezone('UTC'))
    timestamp_format = '%Y-%m-%d %H:%M' 
    eastern = pytz.timezone("US/Eastern")
    utc = pytz.utc
    timestamp = eastern.localize(datetime.strptime(timestamp_str,timestamp_format)).astimezone(utc)
    return {
        'SMA': Decimal(result['SMA']),
        'raw_timestamp': timestamp_str,
        'time': timestamp,
    }




@dataclass
class AlphaVantageAPIClient:
    ticker: str = "AAPL"
    function: str = "TIME_SERIES_INTRADAY"
    interval: Literal["1min", "5min", "15min", "30min", "60min"] = "1min"
    month: str = "2025-01"
    api_key: str = ""
    time_period: int = 60
    series_type: Literal["close", "open", "high", "low"] = "close"




    def get_api_key(self):
        return self.api_key or ALPHA_VANTAGE_API_KEY

    def get_headers(self):
        api_key = self.get_api_key()
        return {}

    def get_stock_params(self):
        return {
            "apikey": self.get_api_key(),
            "symbol": self.ticker,
            "interval": self.interval,
            "function": self.function,
            "month": self.month,
            
        }
    
    
    def generate_stock_url(self, pass_auth=False):
        path = "/query"
        url = f"https://www.alphavantage.co{path}"
        params = self.get_stock_params()
        encoded_params = urlencode(params)
        url = f"{url}?{encoded_params}"
        if pass_auth:
            api_key = self.get_api_key()
            url += f"&api_key={api_key}"
        return url



    def fetch_stock_data(self):
        headers = self.get_headers()
        url = self.generate_stock_url()
        response = requests.get(url, headers=headers)
        response.raise_for_status() # not 200/201
        return response.json()

    def get_stock_data(self):
        data = self.fetch_data()
        dataset_key = [x for x in list(data.keys()) if not x.lower() == "meta data"][0]
        results = data[dataset_key]
        dataset = []
        for timestamp_str in results.keys():
            dataset.append(
                transform_stock_result(timestamp_str, results.get(timestamp_str))
            )
        return dataset
    
    def get_sma_params(self):
        return {
            "apikey": self.get_api_key(),
            "symbol": self.ticker,
            "interval": self.interval,
            "function": "SMA",
            "month": self.month,
            "time_period": self.time_period, 
            "series_type": self.series_type, 
            

        }
    def generate_sma_url(self, pass_auth=False):
        path = "/query"
        url = f"https://www.alphavantage.co{path}"
        params = self.get_sma_params()
        encoded_params = urlencode(params)
        url = f"{url}?{encoded_params}"
        if pass_auth:
            api_key = self.get_api_key()
            url += f"&api_key={api_key}"
        return url
    

    def fetch_sma_data(self):
        headers = self.get_headers()
        url = self.generate_sma_url()
        response = requests.get(url, headers=headers)
        response.raise_for_status() # not 200/201
        return response.json()

    def get_sma_data(self):
        data = self.fetch_sma_data()
        dataset_key = [x for x in list(data.keys()) if not x.lower() == "meta data"][0]
        results = data[dataset_key]
        dataset = []
        for timestamp_str in results.keys():
            dataset.append(
                transform_sma_result(timestamp_str, results.get(timestamp_str))
            )
        return dataset
        

# testing 
if __name__ == "__main__":
    client = AlphaVantageAPIClient(
        ticker="AAPL",
        function="TIME_SERIES_INTRADAY",
        interval="1min",
        month="2024-01",
        api_key=ALPHA_VANTAGE_API_KEY
    )
    stock_data = client.get_sma_data()
    print(stock_data)
        
