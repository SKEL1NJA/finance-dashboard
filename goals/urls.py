from django.urls import path

from .views import GoalContributeView, GoalCreateView, GoalDeleteView, GoalListView, GoalUpdateView

urlpatterns = [
    path('goals/', GoalListView.as_view(), name='goal-list'),
    path('goals/new/', GoalCreateView.as_view(), name='goal-create'),
    path('goals/<int:pk>/edit/', GoalUpdateView.as_view(), name='goal-update'),
    path('goals/<int:pk>/delete/', GoalDeleteView.as_view(), name='goal-delete'),
    path('goals/<int:pk>/contribute/', GoalContributeView.as_view(), name='goal-contribute'),
]