from django.db import transaction as db_transaction

from accounts.models import Account


def contribute_to_goal(goal, amount):
    with db_transaction.atomic():
        if goal.linked_account_id:
            account = Account.objects.select_for_update().get(pk=goal.linked_account_id)
            account.current_balance -= amount
            account.save(update_fields=['current_balance', 'updated_at'])

        goal.current_amount += amount
        if goal.current_amount >= goal.target_amount:
            goal.is_achieved = True
        goal.save(update_fields=['current_amount', 'is_achieved', 'updated_at'])