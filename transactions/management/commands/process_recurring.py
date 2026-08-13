from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from transactions.models import RecurringTransaction, Transaction
from transactions.services import apply_transaction_effect

FREQUENCY_DELTAS = {
    'daily': relativedelta(days=1),
    'weekly': relativedelta(weeks=1),
    'monthly': relativedelta(months=1),
    'yearly': relativedelta(years=1),
}


class Command(BaseCommand):
    help = 'Generates due recurring transactions and sends upcoming bill reminder emails.'

    def handle(self, *args, **options):
        today = date.today()
        generated_count = self.generate_due_transactions(today)
        reminder_count = self.send_upcoming_reminders(today)
        self.stdout.write(self.style.SUCCESS(
            f'Generated {generated_count} transactions, sent {reminder_count} reminder emails.'
        ))

    def generate_due_transactions(self, today):
        due_items = RecurringTransaction.objects.filter(
            is_active=True, next_due_date__lte=today
        ).select_related('account', 'category', 'user')

        count = 0
        for item in due_items:
            if item.end_date and item.next_due_date > item.end_date:
                item.is_active = False
                item.save(update_fields=['is_active', 'updated_at'])
                continue

            txn = Transaction.objects.create(
                user=item.user,
                account=item.account,
                category=item.category,
                transaction_type=item.transaction_type,
                amount=item.amount,
                description=item.description,
                date=item.next_due_date,
                recurring_source=item,
            )
            apply_transaction_effect(txn, sign=1)

            item.next_due_date += FREQUENCY_DELTAS[item.frequency]
            item.save(update_fields=['next_due_date', 'updated_at'])
            count += 1

        return count

    def send_upcoming_reminders(self, today):
        reminder_window = today + timedelta(days=3)
        upcoming = RecurringTransaction.objects.filter(
            is_active=True,
            transaction_type='expense',
            next_due_date__gt=today,
            next_due_date__lte=reminder_window,
        ).select_related('account', 'user')

        count = 0
        for item in upcoming:
            if not item.user.email:
                continue

            send_mail(
                subject=f'Upcoming bill: {item.description or item.category} due {item.next_due_date}',
                message=(
                    f'Reminder: {item.description or item.category} for '
                    f'{item.account.currency.symbol}{item.amount} is due on {item.next_due_date} '
                    f'from {item.account.name}.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[item.user.email],
            )
            count += 1

        return count