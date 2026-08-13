import csv
import io
from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.db import transaction as db_transaction

from accounts.models import Account

from .models import Category, Transaction
from .services import apply_transaction_effect

EXPORT_HEADERS = ['date', 'account', 'category', 'transaction_type', 'amount', 'description']


def export_transactions_to_csv(user):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(EXPORT_HEADERS)

    queryset = Transaction.objects.filter(user=user).select_related('account', 'category').order_by('-date')
    for txn in queryset:
        writer.writerow([
            txn.date.isoformat(),
            txn.account.name,
            txn.category.name if txn.category else '',
            txn.transaction_type,
            txn.amount,
            txn.description,
        ])

    return buffer.getvalue()


class CSVImportError(Exception):
    def __init__(self, row_number, message):
        self.row_number = row_number
        self.message = message
        super().__init__(f'Row {row_number}: {message}')


def import_transactions_from_csv(user, file_obj):
    decoded = file_obj.read().decode('utf-8-sig')
    reader = csv.DictReader(io.StringIO(decoded))

    required_columns = {'date', 'account', 'transaction_type', 'amount'}
    if not required_columns.issubset(set(reader.fieldnames or [])):
        raise CSVImportError(0, f'CSV must include columns: {", ".join(sorted(required_columns))}')

    accounts = {a.name: a for a in Account.objects.filter(user=user)}
    categories = {c.name: c for c in Category.objects.filter(user=user)}

    rows = list(reader)
    created_count = 0

    with db_transaction.atomic():
        for i, row in enumerate(rows, start=2):
            account = accounts.get(row['account'].strip())
            if not account:
                raise CSVImportError(i, f'Unknown account "{row["account"]}"')

            transaction_type = row['transaction_type'].strip().lower()
            if transaction_type not in ('income', 'expense', 'transfer'):
                raise CSVImportError(i, f'Invalid transaction_type "{row["transaction_type"]}"')

            try:
                amount = Decimal(row['amount'].strip())
            except InvalidOperation:
                raise CSVImportError(i, f'Invalid amount "{row["amount"]}"')

            try:
                txn_date = datetime.strptime(row['date'].strip(), '%Y-%m-%d').date()
            except ValueError:
                raise CSVImportError(i, f'Invalid date "{row["date"]}", expected YYYY-MM-DD')

            category = None
            category_name = (row.get('category') or '').strip()
            if category_name:
                category = categories.get(category_name)
                if not category and transaction_type != 'transfer':
                    raise CSVImportError(i, f'Unknown category "{category_name}"')

            txn = Transaction.objects.create(
                user=user,
                account=account,
                category=category,
                transaction_type=transaction_type,
                amount=amount,
                description=row.get('description', ''),
                date=txn_date,
            )
            apply_transaction_effect(txn, sign=1)
            created_count += 1

    return created_count