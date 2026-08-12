from django.conf import settings
from django.db import models

from accounts.models import Account
from core.models import SoftDeleteModel


class Category(SoftDeleteModel):
    CATEGORY_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories'
    )
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#6366f1')

    class Meta:
        verbose_name_plural = 'categories'
        constraints = [
            models.UniqueConstraint(fields=['user', 'name', 'parent'], name='unique_category_per_user')
        ]

    def __str__(self):
        return self.name


class RecurringTransaction(SoftDeleteModel):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recurring_transactions'
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='recurring_transactions')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='recurring_transactions'
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    next_due_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.description or self.category} - {self.amount}'


class Transaction(SoftDeleteModel):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transfer_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='incoming_transfers'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions'
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    receipt_image = models.ImageField(upload_to='receipts/%Y/%m/', null=True, blank=True)
    recurring_source = models.ForeignKey(
        RecurringTransaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_transactions'
    )

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.transaction_type} {self.amount} on {self.date}'