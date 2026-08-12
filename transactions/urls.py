from django.urls import path

from .category_views import (
    CategoryCreateView, CategoryDeleteView, CategoryListView, CategoryUpdateView,
    RuleCreateView, RuleDeleteView,
)
from .views import TransactionCreateView, TransactionDeleteView, TransactionListView, TransactionUpdateView

urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/new/', TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/edit/', TransactionUpdateView.as_view(), name='transaction-update'),
    path('transactions/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction-delete'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/new/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('rules/new/', RuleCreateView.as_view(), name='rule-create'),
    path('rules/<int:pk>/delete/', RuleDeleteView.as_view(), name='rule-delete'),
]