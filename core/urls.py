from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import dashboard_view

urlpatterns = [
    path('', login_required(dashboard_view), name='dashboard'),
]