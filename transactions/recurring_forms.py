from django import forms

from accounts.models import Account

from .models import Category, RecurringTransaction

INPUT_CLASSES = 'w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500'


class RecurringTransactionForm(forms.ModelForm):
    class Meta:
        model = RecurringTransaction
        fields = ['account', 'category', 'transaction_type', 'amount', 'description', 'frequency', 'start_date', 'end_date']
        widgets = {
            'account': forms.Select(attrs={'class': INPUT_CLASSES}),
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
            'transaction_type': forms.Select(attrs={'class': INPUT_CLASSES}),
            'amount': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'step': '0.01'}),
            'description': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'frequency': forms.Select(attrs={'class': INPUT_CLASSES}),
            'start_date': forms.DateInput(attrs={'class': INPUT_CLASSES, 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': INPUT_CLASSES, 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=self.user, is_active=True)
        self.fields['category'].queryset = Category.objects.filter(user=self.user)
        self.fields['end_date'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if not instance.pk:
            instance.next_due_date = instance.start_date
        if commit:
            instance.save()
        return instance