#!/usr/bin/env python
# coding: utf-8

# In[7]:


import setup
setup.init_django()


# In[8]:


from market.models import StockQuote


# In[9]:


from django.db.models import Avg, F, RowRange, Window
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


# In[10]:


days_ago = 30
now = timezone.now()
start_date = now - timedelta(days=30)
end_date = now

qs = StockQuote.objects.filter(company__ticker="AAPL", time__range=(start_date, end_date))
qs.count()



# In[11]:


from django.utils.timezone import make_aware
import datetime
import pytz

# Define the parameter k
k = 30  # for example, 30 minutes after the current time

# for the first object in qs print the available static variable names to parse
first_object = qs[7110]
print(first_object.__dict__.keys())
print(first_object.company)
print(first_object.company.ticker)
print(first_object.close_price)

# turn UTC TIME Jan. 10, 2025, 9 p.m. into Jan 10, 2025, 04:00 PM (EST)
print("current object time: ", first_object.time)  # this gets you utc time
eastern = pytz.timezone('US/Eastern')

# Convert the date to k minutes after the current time
localized_time = first_object.time.astimezone(eastern)
print(localized_time)
print(localized_time.hour)

# Add k minutes to the current time
target_est = localized_time + timedelta(minutes=k)
target_utc = target_est.astimezone(datetime.timezone.utc)
print(f"converted time to {k} minutes after current time: ", target_est)

# Query for the same date but k minutes after the current time
value_after_k_minutes = StockQuote.objects.filter(company__ticker="AAPL", time=target_utc).first()
print(value_after_k_minutes.close_price if value_after_k_minutes else "No data available")
print("Time for the object: ", value_after_k_minutes.time if value_after_k_minutes else "No data available")




# In[12]:


# Initialize the queryset
qs = None
qs = StockQuote.objects.filter(company__ticker="AAPL")

# Initialize a list to store the results
close_price_after_k_window_dataset = []

# Iterate over each object in the queryset
for obj in qs:
    # Localize the time to Eastern timezone
    localized_time = obj.time.astimezone(eastern)
    
    # Add k minutes to the localized time
    target_est = localized_time + timedelta(minutes=k)
    target_utc = target_est.astimezone(datetime.timezone.utc)
    
    # Query for the same date but k minutes after the current time
    value_after_k_minutes = StockQuote.objects.filter(company__ticker="AAPL", time=target_utc).first()
    
    # Append the result to the dataset
    close_price_after_k_window_dataset.append({
        'original_time': obj.time,
        'close_price': obj.close_price,
        'time_after_k_minutes': target_utc,
        'close_price_after_k_minutes': value_after_k_minutes.close_price if value_after_k_minutes else None
    })

# Print the number of items with a valid close_price_after_k_window_value
valid_close_price_after_k_window_value = sum(1 for item in close_price_after_k_window_dataset if item['close_price_after_k_minutes'] is not None)
print(f"Number of items with a valid close_price_after_k_window_value: {valid_close_price_after_k_window_value}")
# Print the first 10 items in the dataset
for item in close_price_after_k_window_dataset[:1000]:
    print(item)


# In[ ]:


# Let A be Predicted Price Change: Literal["1", "-1"] for 1 being greater than current price
# Let B be Given time series past data
# we want to solve for P (A | B) 
import setup
setup.init_django()
import helpers.clients as helper_clients
from datetime import datetime, timedelta

# class TimeSeriesBlock(int: lookback_depth, int: k_projection)
from django.db import models
from dataclasses import dataclass
from market.models import Company, StockQuote


@dataclass
class TimeSeriesBlock:
    ticker: str = "AAPL"
    timestamp = models.DateTimeField(auto_now_add=True)
    step_size: str = "minute"
    # number of the most recent time series objects we store given that the objects are sorted ascending, and less than current time
    l_lookback_depth: int = 15 

    # number of the most recent time series objects we store given that the objects are sorted ascending, and greater than current time
    k_projection_depth: int = 15
    k_projection_steps: int = 15


