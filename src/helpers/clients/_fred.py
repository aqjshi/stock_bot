import pytz
import requests
import math
from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlencode
from datetime import datetime
from decouple import config

# ------------------------------------------------------------------------------
# SAMPLE FRED API REQUEST URL
# ------------------------------------------------------------------------------
# For series_id = "GNPCA", realtime_start = "2024-07-04", realtime_end = "2024-08-28"
# and a placeholder API key, the request could look like:
#
# https://api.stlouisfed.org/fred/series/observations
# ?series_id=GNPCA
# &realtime_start=2024-07-04
# &realtime_end=2024-08-28
# &api_key=6799bbe3b5be9dc92751b055763e402b
# &file_type=json
#
# ------------------------------------------------------------------------------
# SAMPLE OUTPUT (TRUNCATED)
# ------------------------------------------------------------------------------
"""
{
  "realtime_start":"2024-07-04",
  "realtime_end":"2024-07-05",
  "observation_start":"1600-01-01",
  "observation_end":"9999-12-31",
  "units":"lin",
  "output_type":1,
  "file_type":"json",
  "order_by":"observation_date",
  "sort_order":"asc",
  "count":1337,
  "offset":0,
  "limit":100000,
  "observations":[
     {
       "realtime_start":"2024-07-04",
       "realtime_end":"2024-07-05",
       "date":"1913-01-01",
       "value":"12.1"
     },
     {
       "realtime_start":"2024-07-04",
       "realtime_end":"2024-07-05",
       "date":"1913-02-01",
       "value":"12.0"
     },
     ...
  ]
}
"""

# ------------------------------------------------------------------------------

# Fetch FRED API Key from environment (.env) or fallback
FRED_API_KEY = config("FRED_API_KEY", default=None, cast=str)

def fetch_fred_data(series_id: str, fred_api_key: str, 
                    realtime_start: str = "2024-07-04", 
                    realtime_end: str = "2024-08-28") -> dict:
    """
    Fetches time series data from the FRED API for a given series ID.
    
    :param series_id: The FRED series ID.
    :param fred_api_key: The API key for authentication.
    :param realtime_start: The start date for real-time FRED data.
    :param realtime_end: The end date for real-time FRED data.
    :return: A dictionary mapping date strings to float values (or NaN).
    """
    base_url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "realtime_start": realtime_start,
        "realtime_end": realtime_end,
        "api_key": fred_api_key,
        "file_type": "json"
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()

    observations = response.json().get("observations", [])
    data_dict = {}

    for obs in observations:
        date_str = obs["date"]
        val_str = obs["value"]
        data_dict[date_str] = float(val_str) if val_str != "." else math.nan

    return data_dict

def transform_fred_result(result: dict) -> dict:
    """
    Transforms a single FRED observation into a structured format.
    
    NOTE: This example assumes a structure with 't' (timestamp) 
    and 'value' keys. Adjust to your actual JSON fields if needed.
    
    :param result: A single observation from the FRED API.
    :return: A transformed result with a UTC timestamp and 'value'.
    """
    # Example: if result has a field 't' that is a Unix timestamp in milliseconds
    # you can convert it to a Python datetime object.
    # This is just an illustrative example; real FRED data does not usually return 't'.
    unix_timestamp = result.get('t', 0) / 1000.0  # default to 0 if not found
    utc_timestamp = datetime.fromtimestamp(unix_timestamp, tz=pytz.UTC)

    return {
        "timestamp": utc_timestamp,
        "value": result.get('value')
    }

@dataclass
class FREDAPIClient:
    """
    A dataclass-based client for fetching data from the FRED API.
    """
    series_id: str = "GNPCA"
    realtime_start: str = "2024-07-04"
    realtime_end: str = "2024-08-28"
    api_key: str = FRED_API_KEY

    def get_api_key(self) -> str:
        """Returns the API key, prioritizing the field over the environment variable."""
        return self.api_key or FRED_API_KEY

    def get_params(self) -> dict:
        """Generates request parameters for the FRED API call."""
        return {
            "series_id": self.series_id,
            "realtime_start": self.realtime_start,
            "realtime_end": self.realtime_end,
            "file_type": "json",
            "api_key": self.get_api_key()
        }

    def generate_url(self) -> str:
        """Constructs the complete FRED API URL for this client's configuration."""
        base_url = "https://api.stlouisfed.org/fred/series/observations"
        params = self.get_params()
        return f"{base_url}?{urlencode(params)}"

    def fetch_data(self) -> dict:
        """
        Fetches raw data from the FRED API, returning the parsed JSON.
        """
        url = self.generate_url()
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_series_data(self) -> list:
        """
        Fetches and transforms the series data from the FRED API.
        
        :return: A list of transformed observation data.
        """
        data = self.fetch_data()
        observations = data.get("observations")
        if not observations:
            raise ValueError(f"No data found for series ID: {self.series_id}")

        # Example transformation; adjust fields as needed for real FRED data.
        return [transform_fred_result(obs) for obs in observations]

# ------------------------------------------------------------------------------

def get_macro_data(fred_api_key: str = FRED_API_KEY) -> dict:
    """
    Fetches key macroeconomic indicators from FRED using their series IDs.
    
    :param fred_api_key: The API key for the FRED API.
    :return: A dictionary of macroeconomic indicators, each as a dict of date-value pairs.
    """
    return {
        "treasury_10y_yield": fetch_fred_data("DGS10", fred_api_key),
        "fed_funds_rate": fetch_fred_data("FEDFUNDS", fred_api_key),
        "cpi": fetch_fred_data("CPIAUCSL", fred_api_key),
        "ppi": fetch_fred_data("PPIACO", fred_api_key),
        "u3": fetch_fred_data("UNRATE", fred_api_key),
        "u6": fetch_fred_data("U6RATE", fred_api_key),
        "gdp": fetch_fred_data("GDP", fred_api_key),
        "cci": fetch_fred_data("CSCICP03USM665S", fred_api_key),
        "retail_sales": fetch_fred_data("RSAFS", fred_api_key),
        "m2": fetch_fred_data("M2SL", fred_api_key),
    }

# ------------------------------------------------------------------------------
# EXAMPLE USAGE
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Provide your actual FRED API key here or set it in your .env file
    example_api_key = "YOUR_FRED_API_KEY"
    
    # Fetch a single series (e.g., GNPCA) for a given date range
    # using the FREDAPIClient dataclass
    client = FREDAPIClient(
        series_id="GNPCA",
        realtime_start="2024-07-04",
        realtime_end="2024-08-28",
        api_key=example_api_key
    )
    gnpca_data = client.get_series_data()
    print("GNPCA Data (Transformed):", gnpca_data)

    # Fetch multiple macroeconomic indicators
    macro_indicators = get_macro_data(example_api_key)
    print("Macro Indicators:", macro_indicators)

