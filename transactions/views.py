import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .forms import TransactionForm
from .models import Transaction
from .services import apply_transaction_effect
from .csv_utils import CSVImportError, export_transactions_to_csv, import_transactions_from_csv


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 25

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).select_related('account', 'category')


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        apply_transaction_effect(self.object, sign=1)
        return redirect(self.success_url)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self._original = Transaction.objects.get(pk=obj.pk)
        return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        apply_transaction_effect(self._original, sign=-1)
        self.object = form.save()
        apply_transaction_effect(self.object, sign=1)
        return redirect(self.success_url)


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction-list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        apply_transaction_effect(self.object, sign=-1)
        self.object.delete()
        return redirect(self.success_url)

class TransactionExportView(LoginRequiredMixin, View):
    def get(self, request):
        csv_data = export_transactions_to_csv(request.user)
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
        return response


class TransactionImportView(LoginRequiredMixin, View):
    template_name = 'transactions/transaction_import.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        file_obj = request.FILES.get('csv_file')
        if not file_obj:
            messages.error(request, 'Please choose a CSV file.')
            return render(request, self.template_name)

        try:
            count = import_transactions_from_csv(request.user, file_obj)
        except CSVImportError as e:
            messages.error(request, str(e))
            return render(request, self.template_name)

        messages.success(request, f'Imported {count} transactions successfully.')
        return redirect('transaction-list')