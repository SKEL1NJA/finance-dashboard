from django.conf import settings
from django.db import models

from core.models import SoftDeleteModel


class Currency(SoftDeleteModel):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)
    exchange_rate_to_base = models.DecimalField(max_digits=12, decimal_places=6, default=1)

    class Meta:
        verbose_name_plural = 'currencies'

    def __str__(self):
        return self.code


class Account(SoftDeleteModel):
    ACCOUNT_TYPES = [
        ('bank', 'Bank'),
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('wallet', 'Wallet'),
        ('investment', 'Investment'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='accounts')
    initial_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.get_account_type_display()})'