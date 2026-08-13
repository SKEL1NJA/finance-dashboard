from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ContributionForm, SavingsGoalForm
from .models import SavingsGoal
from .services import contribute_to_goal


class GoalListView(LoginRequiredMixin, ListView):
    model = SavingsGoal
    template_name = 'goals/goal_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user).select_related('linked_account')


class GoalCreateView(LoginRequiredMixin, CreateView):
    model = SavingsGoal
    form_class = SavingsGoalForm
    template_name = 'goals/goal_form.html'
    success_url = reverse_lazy('goal-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = SavingsGoal
    form_class = SavingsGoalForm
    template_name = 'goals/goal_form.html'
    success_url = reverse_lazy('goal-list')

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = SavingsGoal
    template_name = 'goals/goal_confirm_delete.html'
    success_url = reverse_lazy('goal-list')

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)


class GoalContributeView(LoginRequiredMixin, View):
    template_name = 'goals/goal_contribute.html'

    def get_goal(self, request, pk):
        return get_object_or_404(SavingsGoal, pk=pk, user=request.user)

    def get(self, request, pk):
        goal = self.get_goal(request, pk)
        form = ContributionForm()
        return render(request, self.template_name, {'goal': goal, 'form': form})

    def post(self, request, pk):
        goal = self.get_goal(request, pk)
        form = ContributionForm(request.POST)
        if form.is_valid():
            contribute_to_goal(goal, form.cleaned_data['amount'])
            return redirect('goal-list')
        return render(request, self.template_name, {'goal': goal, 'form': form})