#!/usr/bin/env python
# coding: utf-8

# In[1]:


import setup
setup.init_django()


# In[2]:


import helpers.clients as helper_clients
from market.models import *

# companies = Company.objects.all()

# stocks = StockQuote.objects.all()
# stocks.count()


# start_from_strach = True
# if start_from_strach:
#     companies.delete()
#     stocks.delete()


# In[10]:


import yfinance as yf
import pandas as pd

def fetch_top_500_companies():
    """
    Fetch the top 500 companies by market capitalization using Yahoo Finance.
    """
    # S&P 500 ticker list from Wikipedia
    sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    # Fetch the S&P 500 companies from Wikipedia
    sp500_table = pd.read_html(sp500_url)
    sp500_companies = sp500_table[0]

    # Extract the tickers and company names
    tickers = sp500_companies[['Symbol', 'Security']].sort_values(by='Symbol').values.tolist()

    return tickers

if __name__ == "__main__":
    print("Fetching the top 500 companies by market capitalization...")
    top_500_companies = fetch_top_500_companies()
    for company in top_500_companies:
        print (company[1])


# In[ ]:


from datetime import datetime, timedelta

import bs4 as bs
import pickle 
import requests 


# Configuration
def fetch_top_companies():
    """
    Fetch the top 500 companies by market capitalization using Yahoo Finance.
    """
    # S&P 500 ticker list from Wikipedia
    sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    # Fetch the S&P 500 companies from Wikipedia
    sp500_table = pd.read_html(sp500_url)
    sp500_companies = sp500_table[0]

    # Extract the tickers and company names
    tickers = sp500_companies[['Symbol', 'Security']].sort_values(by='Symbol').values.tolist()

    return tickers
# Fetch top companies
try:
    top_companies = fetch_top_companies()
except ValueError as e:
    print(e)
    top_companies = []  # Default to empty list if fetching fails

# company_names = [company[1] for company in top_companies]
# company_tickers = [company[0] for company in top_companies]
multiplier = 1
from_date = "2025-01-01"
to_date = "2025-01-20"
batch_size = 1000  # Batch size for database inserts
date_format = "%Y-%m-%d"

for company in top_companies:

    company_obj, created = Company.objects.get_or_create(name=company[1], ticker=company[0])

    # Initialize API client
    client = helper_clients.PolygonAPIClient(
        ticker=company[0],
        multiplier=multiplier,
        from_date=from_date,
        to_date=to_date
    )


    # Fetch datasets in batches
    print("Fetching datasets in batches...")
    stock_data = client.fetch_stock_data_in_batches(from_date, to_date)
    sma_data = client.fetch_sma_data_in_batches(from_date, to_date)
    ema_data = client.fetch_ema_data_in_batches(from_date, to_date)
    macd_data = client.fetch_macd_data_in_batches(from_date, to_date)
    rsi_data = client.fetch_rsi_data_in_batches(from_date, to_date)

    print(f"Stock Data Length: {len(stock_data)}")
    print(f"SMA Data Length: {len(sma_data)}")
    print(f"EMA Data Length: {len(ema_data)}")
    print(f"MACD Data Length: {len(macd_data)}")
    print(f"RSI Data Length: {len(rsi_data)}")


    print(f"Stock Data Length: {len(stock_data)}")
    print(f"SMA Data Length: {len(sma_data)}")
    print(f"EMA Data Length: {len(ema_data)}")
    print(f"MACD Data Length: {len(macd_data)}")
    print(f"RSI Data Length: {len(rsi_data)}")

    print(sma_data[0])

# Keys available for parsing: dict_keys(['longBusinessSummary', 'maxAge', 'priceHint', 'previousClose', 'open', 'dayLow', 'dayHigh', 'regularMarketPreviousClose', 'regularMarketOpen', 'regularMarketDayLow', 'regularMarketDayHigh', 'trailingPE', 'volume', 'regularMarketVolume', 'averageVolume', 'averageVolume10days', 'averageDailyVolume10Day', 'bid', 'ask', 'bidSize', 'askSize', 'yield', 'totalAssets', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'fiftyDayAverage', 'twoHundredDayAverage', 'trailingAnnualDividendRate', 'trailingAnnualDividendYield', 'navPrice', 'currency', 'category', 'ytdReturn', 'beta3Year', 'fundFamily', 'fundInceptionDate', 'legalType', 'threeYearAverageReturn', 'fiveYearAverageReturn', 'exchange', 'quoteType', 'symbol', 'underlyingSymbol', 'shortName', 'longName', 'firstTradeDateEpochUtc', 'timeZoneFullName', 'timeZoneShortName', 'uuid', 'messageBoardId', 'gmtOffSetMilliseconds', 'trailingPegRatio'])
        


# In[8]:


# Merge additional datasets into the original dataset by matching raw_timestamp
for item in stock_data:
    matching_sma = next((c for c in sma_data if c['raw_timestamp'] == item['raw_timestamp']), None)
    matching_ema = next((e for e in ema_data if e['raw_timestamp'] == item['raw_timestamp']), None)
    matching_macd = next((m for m in macd_data if m['raw_timestamp'] == item['raw_timestamp']), None)
    matching_rsi = next((r for r in rsi_data if r['raw_timestamp'] == item['raw_timestamp']), None)

    # Add the values to the original dataset
    item['sma_value'] = matching_sma['value'] if matching_sma else None
    item['ema_value'] = matching_ema['value'] if matching_ema else None
    if matching_macd:
        item['macd_histogram'] = matching_macd.get('histogram')
        item['macd_signal'] = matching_macd.get('signal')
        item['macd_value'] = matching_macd.get('value')
    item['rsi_value'] = matching_rsi['value'] if matching_rsi else None

# Print the updated dataset for verification
for item in stock_data:
    print(item)
    break  # Remove this break to print all items


# In[ ]:


from market.models import Company, StockQuote


# In[ ]:


# company_obj, created = Company.objects.get_or_create(name=company_name, ticker=company_ticker)
# company_obj, created = Company.objects.create(name=company_name, ticker=company_ticker)
# company_obj, created = Company.objects.get(name=company_name, ticker=company_ticker)


print("Saving data in batches...")
company_obj, _ = Company.objects.get_or_create(name=company_name, ticker=company_ticker)

for i in range(0, len(stock_data), batch_size):
    batch_chunk = stock_data[i:i + batch_size]
    chunked_quotes = []
    for data in batch_chunk:
        chunked_quotes.append(StockQuote(company=company_obj, **data))
    StockQuote.objects.bulk_create(chunked_quotes, ignore_conflicts=True)

print(f"Total Stock Quotes in Database: {StockQuote.objects.all().count()}")


# In[ ]:


company_obj


# In[ ]:


StockQuote.objects.all()


# In[ ]:


StockQuote.objects.all().count()
print(StockQuote.objects.first())
print(StockQuote.objects.first().__dict__)

