from datetime import date

from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from accounts.models import Account
from transactions.models import Transaction


def get_net_worth(user):
    return Account.objects.filter(user=user, is_active=True).aggregate(
        total=Sum('current_balance')
    )['total'] or 0


def get_monthly_trend(user, months=6):
    today = date.today()
    start = today.replace(day=1) - relativedelta(months=months - 1)

    rows = (
        Transaction.objects.filter(user=user, date__gte=start, transaction_type__in=['income', 'expense'])
        .annotate(month=TruncMonth('date'))
        .values('month', 'transaction_type')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    labels = []
    cursor = start
    for _ in range(months):
        labels.append(cursor.strftime('%b %Y'))
        cursor += relativedelta(months=1)

    income_by_month = {r['month'].strftime('%b %Y'): r['total'] for r in rows if r['transaction_type'] == 'income'}
    expense_by_month = {r['month'].strftime('%b %Y'): r['total'] for r in rows if r['transaction_type'] == 'expense'}

    return {
        'labels': labels,
        'income': [float(income_by_month.get(label, 0)) for label in labels],
        'expense': [float(expense_by_month.get(label, 0)) for label in labels],
    }


def get_category_breakdown(user):
    today = date.today()
    start = today.replace(day=1)

    rows = (
        Transaction.objects.filter(
            user=user, transaction_type='expense', date__gte=start, category__isnull=False
        )
        .values('category__name', 'category__color')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    return {
        'labels': [r['category__name'] for r in rows],
        'values': [float(r['total']) for r in rows],
        'colors': [r['category__color'] for r in rows],
    }