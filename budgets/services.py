from datetime import date

from django.db.models import Sum
from dateutil.relativedelta import relativedelta

from transactions.models import Transaction


def get_period_bounds(budget, reference_date=None):
    reference_date = reference_date or date.today()

    if budget.period == 'monthly':
        start = reference_date.replace(day=1)
        end = start + relativedelta(months=1) - relativedelta(days=1)
    else:
        start = reference_date.replace(month=1, day=1)
        end = start + relativedelta(years=1) - relativedelta(days=1)

    return start, end


def calculate_budget_progress(budget):
    start, end = get_period_bounds(budget)

    category_ids = [budget.category_id] + list(
        budget.category.subcategories.values_list('id', flat=True)
    )

    spent = Transaction.objects.filter(
        user=budget.user,
        category_id__in=category_ids,
        transaction_type='expense',
        date__gte=start,
        date__lte=end,
    ).aggregate(total=Sum('amount'))['total'] or 0

    percentage = 0 if budget.amount == 0 else min(100, round((spent / budget.amount) * 100, 1))
    is_over_threshold = percentage >= budget.alert_threshold
    is_over_budget = spent > budget.amount

    return {
        'spent': spent,
        'remaining': budget.amount - spent,
        'percentage': percentage,
        'is_over_threshold': is_over_threshold,
        'is_over_budget': is_over_budget,
        'period_start': start,
        'period_end': end,
    }