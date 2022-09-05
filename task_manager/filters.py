import django_filters
from .models import Task, Label
from django import forms


class TaskFilter(django_filters.FilterSet):
    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name="labels")
    self_tasks = django_filters.BooleanFilter(
        field_name='author',
        widget=forms.CheckboxInput, method='is_author')

    def is_author(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(author=user.id)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
