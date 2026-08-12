from django import forms

from .models import Account, Currency

INPUT_CLASSES = 'w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500'


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'currency', 'initial_balance', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'account_type': forms.Select(attrs={'class': INPUT_CLASSES}),
            'currency': forms.Select(attrs={'class': INPUT_CLASSES}),
            'initial_balance': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['currency'].queryset = Currency.objects.all()
        if not self.instance.pk:
            default_currency = Currency.objects.filter(code='INR').first()
            if default_currency:
                self.fields['currency'].initial = default_currency.pk

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if not instance.pk:
            instance.current_balance = instance.initial_balance
        if commit:
            instance.save()
        return instance