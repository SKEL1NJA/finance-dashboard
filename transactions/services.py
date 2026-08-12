from django.db import transaction as db_transaction

from accounts.models import Account


def apply_transaction_effect(txn, sign=1):
    with db_transaction.atomic():
        account = Account.objects.select_for_update().get(pk=txn.account_id)

        if txn.transaction_type == 'income':
            account.current_balance += sign * txn.amount
        elif txn.transaction_type in ('expense', 'transfer'):
            account.current_balance -= sign * txn.amount

        account.save(update_fields=['current_balance', 'updated_at'])

        if txn.transaction_type == 'transfer' and txn.transfer_account_id:
            transfer_account = Account.objects.select_for_update().get(pk=txn.transfer_account_id)
            transfer_account.current_balance += sign * txn.amount
            transfer_account.save(update_fields=['current_balance', 'updated_at'])