from django.db import migrations


def create_inr(apps, schema_editor):
    Currency = apps.get_model('accounts', 'Currency')
    Currency.objects.get_or_create(
        code='INR',
        defaults={'name': 'Indian Rupee', 'symbol': '₹', 'exchange_rate_to_base': 1},
    )


def remove_inr(apps, schema_editor):
    Currency = apps.get_model('accounts', 'Currency')
    Currency.objects.filter(code='INR').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_inr, remove_inr),
    ]