from django.contrib import admin

from .models import Category, RecurringTransaction, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category_type', 'parent')
    list_filter = ('category_type',)
    search_fields = ('name',)


@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'user', 'account', 'amount', 'frequency', 'next_due_date', 'is_active')
    list_filter = ('frequency', 'is_active')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'account', 'category', 'transaction_type', 'amount')
    list_filter = ('transaction_type', 'account', 'category')
    search_fields = ('description',)