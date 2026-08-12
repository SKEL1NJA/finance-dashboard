from django import forms

from accounts.models import Account

from .models import Category, Transaction

INPUT_CLASSES = 'w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500'


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'transfer_account', 'category', 'transaction_type', 'amount', 'description', 'date', 'receipt_image']
        widgets = {
            'account': forms.Select(attrs={'class': INPUT_CLASSES}),
            'transfer_account': forms.Select(attrs={'class': INPUT_CLASSES}),
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
            'transaction_type': forms.Select(attrs={'class': INPUT_CLASSES}),
            'amount': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'step': '0.01'}),
            'description': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'date': forms.DateInput(attrs={'class': INPUT_CLASSES, 'type': 'date'}),
            'receipt_image': forms.ClearableFileInput(attrs={'class': 'text-sm'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=self.user, is_active=True)
        self.fields['transfer_account'].queryset = Account.objects.filter(user=self.user, is_active=True)
        self.fields['category'].queryset = Category.objects.filter(user=self.user)
        self.fields['transfer_account'].required = False
        self.fields['category'].required = False

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        account = cleaned_data.get('account')
        transfer_account = cleaned_data.get('transfer_account')
        category = cleaned_data.get('category')

        if transaction_type == 'transfer':
            if not transfer_account:
                self.add_error('transfer_account', 'Select a destination account for transfers.')
            elif account and transfer_account == account:
                self.add_error('transfer_account', 'Transfer destination must differ from the source account.')
        elif not category:
            self.add_error('category', 'Category is required for income and expense transactions.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance