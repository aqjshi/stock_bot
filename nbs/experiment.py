#!/usr/bin/env python
# coding: utf-8

# In[13]:


import setup
setup.init_django()


# In[16]:


import helpers.clients as helper_clients
from market.models import *

companies = Company.objects.all()

stocks = StockQuote.objects.all()
stocks.count()


start_from_strach = True
if start_from_strach:
    companies.delete()
    stocks.delete()


# In[ ]:


import bs4 as bs
import pickle
import requests
import pandas as pd
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging
from django.db import transaction

# Set up basic logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
def fetch_top_companies():
    """
    Fetch the top 500 companies by market capitalization using Wikipedia.
    """
    # S&P 500 ticker list from Wikipedia
    sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    # Fetch the S&P 500 companies from Wikipedia
    sp500_table = pd.read_html(sp500_url)
    sp500_companies = sp500_table[0]

    # Extract the tickers and company names
    tickers = sp500_companies[['Symbol', 'Security']].sort_values(by='Symbol').values.tolist()

    return tickers

def fetch_company_data(company, multiplier, from_date, to_date):
    """
    Fetch stock and technical indicator data for a single company.
    """
    ticker = company[0]
    company_name = company[1]
    logging.info(f"Starting data fetch for {ticker}")

    try:
      company_obj, created = Company.objects.get_or_create(name=company_name, ticker=ticker)

      # Initialize API client
      client = helper_clients.PolygonAPIClient(
          ticker=ticker,
          multiplier=multiplier,
          from_date=from_date,
          to_date=to_date
        )

      # Fetch datasets in batches
    #   logging.info(f"Fetching datasets for {ticker}...")
      stock_data = client.fetch_stock_data_in_batches(from_date, to_date)
      sma_data = client.fetch_sma_data_in_batches(from_date, to_date)
      ema_data = client.fetch_ema_data_in_batches(from_date, to_date)
      macd_data = client.fetch_macd_data_in_batches(from_date, to_date)
      rsi_data = client.fetch_rsi_data_in_batches(from_date, to_date)
    #   logging.info(f"Stock Data Length for {ticker}: {len(stock_data)}")
    #   logging.info(f"SMA Data Length for {ticker}: {len(sma_data)}")
    #   logging.info(f"EMA Data Length for {ticker}: {len(ema_data)}")
    #   logging.info(f"MACD Data Length for {ticker}: {len(macd_data)}")
    #   logging.info(f"RSI Data Length for {ticker}: {len(rsi_data)}")

      if not stock_data:
        logging.warning(f"No stock data for {ticker}")
        return None, None

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

      logging.info(f"Data fetch and merge complete for {ticker}")
      return company_obj, stock_data

    except Exception as e:
        logging.error(f"Error processing {ticker}: {e}", exc_info=True)  # Log full traceback
        return None, None

def save_company_data(company_obj, stock_data, batch_size):
    """
    Save the stock data for a company in batches to the database.
    """
    if not stock_data:
      return

    # logging.info(f"Saving data for company: {company_obj.name}...")
    try:
      for i in range(0, len(stock_data), batch_size):
          batch_chunk = stock_data[i:i + batch_size]
          chunked_quotes = []
          for data in batch_chunk:
              chunked_quotes.append(StockQuote(company=company_obj, **data))

          StockQuote.objects.bulk_create(chunked_quotes, ignore_conflicts=True)

      logging.info(f"Saving complete for company: {company_obj.name}...")
    except Exception as e:
      logging.error(f"Error saving data for {company_obj.name}: {e}", exc_info=True)
    
# Fetch top companies
try:
    top_companies = fetch_top_companies()
except ValueError as e:
    print(e)
    top_companies = []  # Default to empty list if fetching fails

multiplier = 1
from_date = "2025-01-01"
to_date = "2025-01-20"
batch_size = 1000  # Batch size for database inserts
date_format = "%Y-%m-%d"

for company in top_companies:
    company_obj, stock_data = fetch_company_data(company, multiplier, from_date, to_date)
    if company_obj and stock_data:
        save_company_data(company_obj, stock_data, batch_size)

print(f"Total Stock Quotes in Database: {StockQuote.objects.all().count()}")


# In[8]:





# In[ ]:


from market.models import Company, StockQuote


# In[ ]:


# company_obj, created = Company.objects.get_or_create(name=company_name, ticker=company_ticker)
# company_obj, created = Company.objects.create(name=company_name, ticker=company_ticker)
# company_obj, created = Company.objects.get(name=company_name, ticker=company_ticker)





# In[ ]:


company_obj


# In[ ]:


StockQuote.objects.all()


# In[ ]:


StockQuote.objects.all().count()
print(StockQuote.objects.first())
print(StockQuote.objects.first().__dict__)

