from django import forms

from accounts.models import Account

from .models import SavingsGoal

INPUT_CLASSES = 'w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500'


class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['name', 'linked_account', 'target_amount', 'target_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'linked_account': forms.Select(attrs={'class': INPUT_CLASSES}),
            'target_amount': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'step': '0.01'}),
            'target_date': forms.DateInput(attrs={'class': INPUT_CLASSES, 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['linked_account'].queryset = Account.objects.filter(user=self.user, is_active=True)
        self.fields['linked_account'].required = False
        self.fields['target_date'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance


class ContributionForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=14, decimal_places=2, min_value=0.01,
        widget=forms.NumberInput(attrs={'class': INPUT_CLASSES, 'step': '0.01'})
    )