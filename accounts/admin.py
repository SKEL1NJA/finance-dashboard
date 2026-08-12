from django.contrib import admin

from .models import Account, Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol', 'exchange_rate_to_base')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'account_type', 'currency', 'current_balance', 'is_active')
    list_filter = ('account_type', 'is_active', 'currency')
    search_fields = ('name', 'user__username')