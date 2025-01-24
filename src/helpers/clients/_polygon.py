import pytz
import requests

from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlencode
from datetime import datetime
from decouple import config
from datetime import datetime, timedelta

POLOGYON_API_KEY = config("POLOGYON_API_KEY", default=None, cast=str)

print(POLOGYON_API_KEY)
def transform_polygon_stock_result(result):
    unix_timestamp = result.get('t') / 1000.0
    utc_timestamp = datetime.fromtimestamp(unix_timestamp, tz=pytz.timezone('UTC'))
    return {
        'open_price': result['o'],
        'close_price': result['c'],
        'high_price': result['h'],
        'low_price': result['l'],
        'number_of_trades': result['n'],
        'volume': result['v'],
        'volume_weighted_average': result['vw'],
        'raw_timestamp': result.get('t'),
        'time': utc_timestamp,
    }

def transform_polygon_sma_result(result):
    """
    Transforms an SMA result from Polygon into a structured format.
    """
    unix_timestamp = result.get("timestamp") / 1000.0
    utc_timestamp = datetime.fromtimestamp(unix_timestamp, tz=pytz.timezone("UTC"))
    return {
        "value": result.get("value"),  # Use "value" to get the SMA value
        "raw_timestamp": result.get("timestamp"),
        "time": utc_timestamp,
    }

def transform_polygon_ema_result(result):
    unix_timestamp = result.get("timestamp") / 1000.0
    utc_timestamp = datetime.fromtimestamp(unix_timestamp, tz=pytz.timezone("UTC"))
    return {
        "value": result.get("value"),  # Use "value" to get the SMA value
        "raw_timestamp": result.get("timestamp"),
        "time": utc_timestamp,
    }
def transform_polygon_macd_result(result):
    unix_timestamp = result.get("timestamp") / 1000.0
    utc_timestamp = datetime.fromtimestamp(unix_timestamp, tz=pytz.timezone("UTC"))
    return {
        "histogram": result["histogram"],
        "signal": result["signal"],
        "value": result["value"],
        'raw_timestamp': result["timestamp"],
        'time': utc_timestamp,
    }


def transform_polygon_rsi_result(result):
    unix_timestamp = result.get("timestamp") / 1000.0
    utc_timestamp = datetime.fromtimestamp(unix_timestamp, tz=pytz.timezone("UTC"))
    return {
        'value': result['value'],
        'raw_timestamp': result.get('timestamp'),
        'time': utc_timestamp,
    }




@dataclass
class PolygonAPIClient:
    ticker: str = "AAPL"
    multiplier: int = 5
    timespan:str = "minute"
    from_date:str = "2025-01-01"
    to_date:str = "2025-01-21"
    api_key:str = ""
    adjusted: bool = True 
    sort: Literal["asc", "desc"] = "desc"

    #sma 
    window: int = 50

    short_window: int = 12
    long_window: int = 26
    signal_window: int = 9

    rsi_window: int = 14
    series_type: Literal["open", "high", "low", "close"] = "close"
    order: Literal["asc", "desc"] = "desc"
    limit = 5000

    date_format = "%Y-%m-%d"

    def get_api_key(self):
        return self.api_key or POLOGYON_API_KEY

    def get_headers(self):
        api_key = self.get_api_key()
        return {
            "Authorization": f"Bearer {api_key}"
        }

    def get_stock_params(self):
        return {
            "adjusted": self.adjusted,
            "sort": self.sort,
            "limit": 5000,
        }
    def get_sma_params(self):
        return {
            "timestamp.gte": self.from_date,
            "timestamp.lte": self.to_date,
            "timespan": self.timespan,
            "adjusted": self.adjusted,
            "window": self.window,
            "series_type": self.series_type,
            "order": self.sort,
            "limit": 5000,
        }
    def get_ema_params(self):
        return {
            "timestamp.gte": self.from_date,
            "timestamp.lte": self.to_date,
            "timespan": self.timespan,
            "adjusted": self.adjusted,
            "window": self.window,
            "series_type": self.series_type,
            "order": self.sort,
            "limit": 5000,
        }
    def get_macd_params(self):
        return {
            "timestamp.gte": self.from_date,
            "timestamp.lte": self.to_date,
            "timespan": self.timespan,
            "adjusted": self.adjusted,
            "short_window": self.short_window,
            "long_window": self.long_window,
            "signal_window": self.signal_window,
            "series_type": self.series_type,
            "order": self.sort,
            "limit": 5000,
        }
    def get_rsi_params(self):
        return {
            "timestamp.gte": self.from_date,
            "timestamp.lte": self.to_date,
            "timespan": self.timespan,
            "adjusted": self.adjusted,
            "rsi_window": self.rsi_window,
            "series_type": self.series_type,
            "order": self.sort,
            "limit": 5000,
        }
    
    def generate_stock_url(self, pass_auth=True):
        ticker = f"{self.ticker}".upper()
        path = f"/v2/aggs/ticker/{ticker}/range/{self.multiplier}/{self.timespan}/{self.from_date}/{self.to_date}"
        url = f"https://api.polygon.io{path}"
        params = self.get_stock_params()
        encoded_params = urlencode(params)
        url = f"{url}?{encoded_params}"
        if pass_auth:
            api_key = self.get_api_key()
            url += f"&apiKey={api_key}"
        return url

    def generate_sma_url(self, pass_auth=True):
        ticker = f"{self.ticker}".upper()
        path = f"/v1/indicators/sma/{ticker}/"
        url = f"https://api.polygon.io{path}"
        params = self.get_sma_params()
        encoded_params = urlencode(params)
        url = f"{url}?{encoded_params}"
        if pass_auth:
            api_key = self.get_api_key()
            url += f"&apiKey={api_key}"
        print(url)
        return url
    
    def generate_ema_url(self, pass_auth=True):
        ticker = f"{self.ticker}".upper()
        path = f"/v1/indicators/ema/{ticker}/"
        url = f"https://api.polygon.io{path}"
        params = self.get_ema_params()
        encoded_params = urlencode(params)
        url = f"{url}?{encoded_params}"
        if pass_auth:
            api_key = self.get_api_key()
            url += f"&apiKey={api_key}"
        return url
        
    def generate_macd_url(self, pass_auth=True):
        ticker = f"{self.ticker}".upper()
        path = f"/v1/indicators/macd/{ticker}/"
        url = f"https://api.polygon.io{path}"
        params = self.get_macd_params()
        encoded_params = urlencode(params)
        url = f"{url}?{encoded_params}"
        if pass_auth:
            api_key = self.get_api_key()
            url += f"&apiKey={api_key}"
        return url
    
    def generate_rsi_url(self, pass_auth=True):
        ticker = f"{self.ticker}".upper()
        path = f"/v1/indicators/rsi/{ticker}/"
        url = f"https://api.polygon.io{path}"
        params = self.get_rsi_params()
        encoded_params = urlencode(params)
        url = f"{url}?{encoded_params}"
        if pass_auth:
            api_key = self.get_api_key()
            url += f"&apiKey={api_key}"
        return url
    
    def fetch_stock_data(self):
        headers = self.get_headers()
        url = self.generate_stock_url()
        response = requests.get(url, headers=headers)
        response.raise_for_status() # not 200/201
        return response.json()
    
    def fetch_sma_data(self):
        headers = self.get_headers()
        url = self.generate_sma_url()
        response = requests.get(url, headers=headers)
        response.raise_for_status() # not 200/201

        return response.json()
    def fetch_ema_data(self):
        headers = self.get_headers()
        url = self.generate_ema_url()
        response = requests.get(url, headers=headers)
        response.raise_for_status() # not 200/201
        return response.json()
    
    def fetch_macd_data(self):
        headers = self.get_headers()
        url = self.generate_macd_url()
        response = requests.get(url, headers=headers)
        response.raise_for_status() # not 200/201
        return response.json()
    
    def fetch_rsi_data(self):
        headers = self.get_headers()
        url = self.generate_rsi_url()
        response = requests.get(url, headers=headers)
        response.raise_for_status() # not 200/201
        return response.json()

    def get_stock_data(self):
        data = self.fetch_stock_data()
        results = data.get('results') or None
        if results is None:
            raise Exception(f"Ticker {self.ticker} has no results")
        dataset = []
        for result in results:
            dataset.append(
                transform_polygon_stock_result(result)
            )
        return dataset
    
    def get_sma_data(self):
        """
        Fetches SMA data, transforms it, and returns a dataset.
        """
        data = self.fetch_sma_data()
        results = data.get("results")  # Use "values" directly if SMA data is in this key
        results = results['values']
        # Transform each SMA result
        dataset = [transform_polygon_sma_result(result) for result in results]
        return dataset

    def get_ema_data(self):
        data = self.fetch_ema_data()
        results = data.get('results') or None
        results = results['values']
        if results is None:
            raise Exception(f"Ticker {self.ticker} has no results")
        dataset = []
        for result in results:
            dataset.append(
                transform_polygon_ema_result(result)
            )
        return dataset
    def get_macd_data(self):
        data = self.fetch_macd_data()
        results = data.get('results')
        results = results['values']
        if results is None:
            raise Exception(f"Ticker {self.ticker} has no results")
        dataset = []
        for result in results:
            dataset.append(
                transform_polygon_macd_result(result)
            )
        return dataset
    def get_rsi_data(self):
        data = self.fetch_rsi_data()
        results = data.get('results') 
        results = results['values']
        if results is None:
            raise Exception(f"Ticker {self.ticker} has no results")
        dataset = []
        for result in results:
            dataset.append(
                transform_polygon_rsi_result(result)
            )
        return dataset
    

        # Helper function to fetch data in date-range batches
    def fetch_stock_data_in_batches(self, from_date, to_date, step_days=5):
        """
        Fetches data in batches based on date ranges.

        :param self: Initialized API client
        :param from_date: Start date (string in 'YYYY-MM-DD')
        :param to_date: End date (string in 'YYYY-MM-DD')
        :param step_days: Number of days per batch
        :return: Consolidated dataset
        """
        consolidated_data = []
        current_date = datetime.strptime(from_date, self.date_format)
        end_date = datetime.strptime(to_date, self.date_format)

        while current_date < end_date:
            batch_start = current_date.strftime(self.date_format)
            batch_end = (current_date + timedelta(days=step_days - 1)).strftime(self.date_format)

            if datetime.strptime(batch_end, self.date_format) > end_date:
                batch_end = to_date

            print(f"Fetching data from {batch_start} to {batch_end}...")
            self.from_date = batch_start
            self.to_date = batch_end

            batch_data = self.get_stock_data()
            consolidated_data.extend(batch_data)

            current_date += timedelta(days=step_days)

        return consolidated_data

    def fetch_sma_data_in_batches(self, from_date, to_date, step_days=5):
        """
        Fetches data in batches based on date ranges.

        :param self: Initialized API client
        :param from_date: Start date (string in 'YYYY-MM-DD')
        :param to_date: End date (string in 'YYYY-MM-DD')
        :param step_days: Number of days per batch
        :return: Consolidated dataset
        """
        consolidated_data = []
        current_date = datetime.strptime(from_date, self.date_format)
        end_date = datetime.strptime(to_date, self.date_format)

        while current_date < end_date:
            batch_start = current_date.strftime(self.date_format)
            batch_end = (current_date + timedelta(days=step_days - 1)).strftime(self.date_format)

            if datetime.strptime(batch_end, self.date_format) > end_date:
                batch_end = to_date

            print(f"Fetching data from {batch_start} to {batch_end}...")
            self.from_date = batch_start
            self.to_date = batch_end

            batch_data = self.get_sma_data()
            consolidated_data.extend(batch_data)

            current_date += timedelta(days=step_days)

        return consolidated_data

    def fetch_ema_data_in_batches(self, from_date, to_date, step_days=5):
        """
        Fetches data in batches based on date ranges.

        :param self: Initialized API client
        :param from_date: Start date (string in 'YYYY-MM-DD')
        :param to_date: End date (string in 'YYYY-MM-DD')
        :param step_days: Number of days per batch
        :return: Consolidated dataset
        """
        consolidated_data = []
        current_date = datetime.strptime(from_date, self.date_format)
        end_date = datetime.strptime(to_date, self.date_format)

        while current_date < end_date:
            batch_start = current_date.strftime(self.date_format)
            batch_end = (current_date + timedelta(days=step_days - 1)).strftime(self.date_format)

            if datetime.strptime(batch_end, self.date_format) > end_date:
                batch_end = to_date

            print(f"Fetching data from {batch_start} to {batch_end}...")
            self.from_date = batch_start
            self.to_date = batch_end

            batch_data = self.get_ema_data()
            consolidated_data.extend(batch_data)

            current_date += timedelta(days=step_days)

        return consolidated_data
    def fetch_macd_data_in_batches(self, from_date, to_date, step_days=5):
        """
        Fetches data in batches based on date ranges.

        :param self: Initialized API client
        :param from_date: Start date (string in 'YYYY-MM-DD')
        :param to_date: End date (string in 'YYYY-MM-DD')
        :param step_days: Number of days per batch
        :return: Consolidated dataset
        """
        consolidated_data = []
        current_date = datetime.strptime(from_date, self.date_format)
        end_date = datetime.strptime(to_date, self.date_format)

        while current_date < end_date:
            batch_start = current_date.strftime(self.date_format)
            batch_end = (current_date + timedelta(days=step_days - 1)).strftime(self.date_format)

            if datetime.strptime(batch_end, self.date_format) > end_date:
                batch_end = to_date

            print(f"Fetching data from {batch_start} to {batch_end}...")
            self.from_date = batch_start
            self.to_date = batch_end

            batch_data = self.get_macd_data()
            consolidated_data.extend(batch_data)

            current_date += timedelta(days=step_days)

        return consolidated_data

    def fetch_rsi_data_in_batches(self, from_date, to_date, step_days=5):
        """
        Fetches data in batches based on date ranges.

        :param self: Initialized API client
        :param from_date: Start date (string in 'YYYY-MM-DD')
        :param to_date: End date (string in 'YYYY-MM-DD')
        :param step_days: Number of days per batch
        :return: Consolidated dataset
        """
        consolidated_data = []
        current_date = datetime.strptime(from_date, self.date_format)
        end_date = datetime.strptime(to_date, self.date_format)

        while current_date < end_date:
            batch_start = current_date.strftime(self.date_format)
            batch_end = (current_date + timedelta(days=step_days - 1)).strftime(self.date_format)

            if datetime.strptime(batch_end, self.date_format) > end_date:
                batch_end = to_date

            print(f"Fetching data from {batch_start} to {batch_end}...")
            self.from_date = batch_start
            self.to_date = batch_end

            batch_data = self.get_rsi_data()
            consolidated_data.extend(batch_data)

            current_date += timedelta(days=step_days)

        return consolidated_data

    def fetch_indicator_data(self, endpoint: str, params: dict):
        """
        Generalized method to fetch data for indicators like SMA, EMA, MACD, and RSI.
        """
        url = f"https://api.polygon.io{endpoint}?{urlencode(params)}&apiKey={self.get_api_key()}"
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensure 2xx status
        return response.json()
    def get_indicator_data(self, endpoint: str, params: dict, transform_function):
        """
        Generalized method to get data for SMA, EMA, MACD, or RSI.
        """
        data = self.fetch_indicator_data(endpoint, params)
        results = data.get("values")  # Assuming the indicator results are under "values"
        if not results:
            raise Exception(f"Ticker {self.ticker} has no results for endpoint {endpoint}")
        
        return [transform_function(result) for result in results]
