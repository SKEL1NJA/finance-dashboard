from django.conf import settings
from django.db import models

from core.models import SoftDeleteModel
from transactions.models import Category


class Budget(SoftDeleteModel):
    PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='monthly')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    alert_threshold = models.PositiveSmallIntegerField(default=80)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'category', 'period', 'start_date'], name='unique_budget_per_period'
            )
        ]

    def __str__(self):
        return f'{self.category} budget: {self.amount}/{self.period}'