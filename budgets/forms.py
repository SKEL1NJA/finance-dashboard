from django import forms

from transactions.models import Category

from .models import Budget

INPUT_CLASSES = 'w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500'


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'period', 'start_date', 'end_date', 'alert_threshold', 'is_active']
        widgets = {
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
            'amount': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'step': '0.01'}),
            'period': forms.Select(attrs={'class': INPUT_CLASSES}),
            'start_date': forms.DateInput(attrs={'class': INPUT_CLASSES, 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': INPUT_CLASSES, 'type': 'date'}),
            'alert_threshold': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=self.user, category_type='expense')
        self.fields['end_date'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance