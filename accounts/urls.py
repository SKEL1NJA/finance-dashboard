from django.urls import path

from .views import AccountCreateView, AccountDeleteView, AccountListView, AccountUpdateView

urlpatterns = [
    path('accounts/', AccountListView.as_view(), name='account-list'),
    path('accounts/new/', AccountCreateView.as_view(), name='account-create'),
    path('accounts/<int:pk>/edit/', AccountUpdateView.as_view(), name='account-update'),
    path('accounts/<int:pk>/delete/', AccountDeleteView.as_view(), name='account-delete'),
]