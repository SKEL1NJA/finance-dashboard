from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import Account, Currency
from transactions.models import Category, Transaction
from transactions.services import apply_transaction_effect


class TransactionBalanceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='testpass123')
        self.currency, _ = Currency.objects.get_or_create(
            code='INR', defaults={'name': 'Indian Rupee', 'symbol': '₹', 'exchange_rate_to_base': 1}
        )
        self.account = Account.objects.create(
            user=self.user, name='Test Account', account_type='bank',
            currency=self.currency, initial_balance=1000, current_balance=1000,
        )
        self.category = Category.objects.create(user=self.user, name='Test Category', category_type='expense')

    def test_expense_reduces_balance(self):
        txn = Transaction.objects.create(
            user=self.user, account=self.account, category=self.category,
            transaction_type='expense', amount=300, date='2026-01-01',
        )
        apply_transaction_effect(txn, sign=1)
        self.account.refresh_from_db()
        self.assertEqual(self.account.current_balance, 700)

    def test_income_increases_balance(self):
        txn = Transaction.objects.create(
            user=self.user, account=self.account, category=self.category,
            transaction_type='income', amount=500, date='2026-01-01',
        )
        apply_transaction_effect(txn, sign=1)
        self.account.refresh_from_db()
        self.assertEqual(self.account.current_balance, 1500)

    def test_reversal_restores_balance(self):
        txn = Transaction.objects.create(
            user=self.user, account=self.account, category=self.category,
            transaction_type='expense', amount=200, date='2026-01-01',
        )
        apply_transaction_effect(txn, sign=1)
        apply_transaction_effect(txn, sign=-1)
        self.account.refresh_from_db()
        self.assertEqual(self.account.current_balance, 1000)


class SoftDeleteTests(TestCase):
    def test_deleted_account_excluded_from_default_manager(self):
        user = User.objects.create_user(username='tester2', password='testpass123')
        currency = Currency.objects.create(code='USD', name='US Dollar', symbol='$', exchange_rate_to_base=83)
        account = Account.objects.create(
            user=user, name='To Delete', account_type='cash', currency=currency, initial_balance=0,
        )
        account.delete()
        self.assertFalse(Account.objects.filter(pk=account.pk).exists())
        self.assertTrue(Account.all_objects.filter(pk=account.pk).exists())