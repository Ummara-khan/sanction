from django.db import models

from .constants import TRANSACTION_TYPE_CHOICES



from django.db import models

class UploadStatistics(models.Model):
    LIST_CHOICES = [
        ('ofac', 'OFAC'),
        ('un', 'UN'),
        ('eu', 'EU'),
    ]

    list_name = models.CharField(max_length=10, choices=LIST_CHOICES, unique=True)
    last_import_date = models.DateField()
    records_added = models.PositiveIntegerField(default=0)
    records_updated = models.PositiveIntegerField(default=0)
    records_deleted = models.PositiveIntegerField(default=0)
    total_active_records = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.list_name

# transactions/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction by {self.user.email} on {self.timestamp}'
