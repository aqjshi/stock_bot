from django.db import models

from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager

from . import tasks
# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=120)
    ticker = models.CharField(max_length=20, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.ticker = f"{self.ticker}".upper()
        super().save(*args, **kwargs)
        tasks.sync_company_stock_quotes.delay(self.pk)

class StockQuote(models.Model):
    """
    'open_price': 140.41,
    'close_price': 140.41,
    'high_price': 140.41,
    'low_price': 140.41,
    'number_of_trades': 3,
    'volume': 134,
    'volume_weighted_average': 140.3984,
    'time': datetime.datetime(2024, 1, 9, 9, 2, tzinfo=<UTC>)
    """
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        related_name="stock_quotes" 
    )
    open_price = models.DecimalField(max_digits=10, decimal_places=4)
    close_price = models.DecimalField(max_digits=10, decimal_places=4)
    high_price = models.DecimalField(max_digits=10, decimal_places=4)
    low_price = models.DecimalField(max_digits=10, decimal_places=4)
    number_of_trades = models.BigIntegerField(blank=True, null=True)
    volume = models.BigIntegerField()
    volume_weighted_average = models.DecimalField(max_digits=10, decimal_places=6)
    raw_timestamp = models.CharField(max_length=120, null=True, blank=True, help_text="Non transformed timestamp string or int or float")
    time = TimescaleDateTimeField(interval="1 week")
    
    sma_value = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    ema_value = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    macd_histogram = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    macd_signal = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    macd_value = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    rsi_value = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)

    treasury_10y_yield  = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    fed_funds_rate  = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    cpi  = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    ppi  = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    u3  = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    u6  = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    gdp  = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    cci  = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    retail_sales  = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)
    m2  = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)


    objects = models.Manager()
    timescale = TimescaleManager()

    class Meta:
        unique_together = [('company', 'time')]
