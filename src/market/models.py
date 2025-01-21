from django.db import models, IntegrityError, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager

from . import tasks

# Company Model
class Company(models.Model):
    name = models.CharField(max_length=120)
    ticker = models.CharField(max_length=20, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Ensure ticker is always uppercase
        self.ticker = self.ticker.upper()
        super().save(*args, **kwargs)  # Call parent save method

    # def __str__(self):
    #     return f"{self.name} ({self.ticker})"

# Signal to handle Celery task triggering after company creation
@receiver(post_save, sender=Company)
def sync_stock_quotes(sender, instance, created, **kwargs):
    if created:  # Trigger the task only when a new Company is created
        try:
            tasks.sync_company_stock_quotes.delay(instance.pk)
        except Exception as e:
            print(f"Error triggering task: {e}")

# StockQuote Model
class StockQuote(models.Model):
    """
    Represents stock price data for a given company at a specific timestamp.
    Example:
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
    raw_timestamp = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        help_text="Non-transformed timestamp string or int/float."
    )
    time = TimescaleDateTimeField(interval="1 week")

    # Use TimescaleDB manager for time-based operations
    objects = models.Manager()
    timescale = TimescaleManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'time'], name='unique_company_time')
        ]

    # def __str__(self):
    #     return f"{self.company.name} - {self.time}: Open={self.open_price}, Close={self.close_price}"
