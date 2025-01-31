#!/usr/bin/env python
# coding: utf-8

# In[6]:


import setup
setup.init_django()


# In[7]:


from market.models import StockQuote


# In[8]:


from django.db.models import Avg, F, RowRange, Window
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


# In[9]:


days_ago = 30
now = timezone.now()
start_date = now - timedelta(days=30)
end_date = now

qs = StockQuote.objects.filter(company__ticker="AAPL", time__range=(start_date, end_date))
qs.count()



# In[12]:


from django.utils.timezone import make_aware
import datetime
import pytz

# for the first object in qs print the available static variable names to parse
first_object = qs[7110]
print(first_object.__dict__.keys())
print(first_object.company)
print(first_object.company.ticker)
print(first_object.close_price)

# turn UTC TIME Jan. 10, 2025, 9 p.m. into Jan 10, 2025, 04:00 PM (EST)
print("current object time: ", first_object.time)  # this gets you utc time
eastern = pytz.timezone('US/Eastern')

# Convert the date to 4 PM EST
localized_time = first_object.time.astimezone(eastern)
print(localized_time)
print(localized_time.hour)
if localized_time.hour >= 16:
    target_est = (localized_time + timedelta(days=1)).replace(hour=16, minute=0, second=0, microsecond=0)
else:
    target_est = localized_time.replace(hour=16, minute=0, second=0, microsecond=0)

target_utc = target_est.astimezone(datetime.timezone.utc)
print("converted time to 4 PM EST: ", target_est)

# Query for the same date but at 4 PM
end_of_trading_day_closing_value = StockQuote.objects.filter(company__ticker="AAPL", time=target_utc).first()
print(end_of_trading_day_closing_value.close_price if end_of_trading_day_closing_value else "No data available")
print("Time for the object: ", end_of_trading_day_closing_value.time if end_of_trading_day_closing_value else "No data available")


