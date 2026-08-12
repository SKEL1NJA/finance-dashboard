from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Category, CategorizationRule


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'transactions/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user, parent__isnull=True).prefetch_related('subcategories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rules'] = CategorizationRule.objects.filter(user=self.request.user).select_related('category')
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'category_type', 'parent', 'color']
    template_name = 'transactions/category_form.html'
    success_url = reverse_lazy('category-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['parent'].queryset = Category.objects.filter(user=self.request.user)
        for field in form.fields.values():
            field.widget.attrs['class'] = 'w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm'
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'category_type', 'parent', 'color']
    template_name = 'transactions/category_form.html'
    success_url = reverse_lazy('category-list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['parent'].queryset = Category.objects.filter(user=self.request.user).exclude(pk=self.object.pk)
        for field in form.fields.values():
            field.widget.attrs['class'] = 'w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm'
        return form


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'transactions/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class RuleCreateView(LoginRequiredMixin, CreateView):
    model = CategorizationRule
    fields = ['keyword', 'category', 'priority']
    template_name = 'transactions/rule_form.html'
    success_url = reverse_lazy('category-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        for field in form.fields.values():
            field.widget.attrs['class'] = 'w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm'
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RuleDeleteView(LoginRequiredMixin, DeleteView):
    model = CategorizationRule
    template_name = 'transactions/rule_confirm_delete.html'
    success_url = reverse_lazy('category-list')

    def get_queryset(self):
        return CategorizationRule.objects.filter(user=self.request.user)