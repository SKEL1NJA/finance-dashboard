from django.urls import path

from .views import BudgetCreateView, BudgetDeleteView, BudgetListView, BudgetUpdateView

urlpatterns = [
    path('budgets/', BudgetListView.as_view(), name='budget-list'),
    path('budgets/new/', BudgetCreateView.as_view(), name='budget-create'),
    path('budgets/<int:pk>/edit/', BudgetUpdateView.as_view(), name='budget-update'),
    path('budgets/<int:pk>/delete/', BudgetDeleteView.as_view(), name='budget-delete'),
]