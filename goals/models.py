from django.conf import settings
from django.db import models

from accounts.models import Account
from core.models import SoftDeleteModel


class SavingsGoal(SoftDeleteModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='savings_goals')
    linked_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='savings_goals'
    )
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=14, decimal_places=2)
    current_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    target_date = models.DateField(null=True, blank=True)
    is_achieved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def progress_percentage(self):
        if self.target_amount == 0:
            return 0
        return min(100, round((self.current_amount / self.target_amount) * 100, 1))