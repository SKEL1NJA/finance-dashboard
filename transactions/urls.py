from django.urls import path

from .views import TransactionCreateView, TransactionDeleteView, TransactionListView, TransactionUpdateView

urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/new/', TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/edit/', TransactionUpdateView.as_view(), name='transaction-update'),
    path('transactions/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction-delete'),
]