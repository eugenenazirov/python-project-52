from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from .forms import MyRegisterUserForm, MyCreateStatusForm, MyCreateTaskForm, MyCreateLabelForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from .models import Status, Task, Label
from .filters import TaskFilter
from django_filters.views import FilterView
from .mixins import MyLoginRequiredMixin, MyUserPermissionMixin, MyTaskPermissionMixin


class BaseView(TemplateView):
    template_name: str = 'base.html'


class UserList(ListView):
    model = User
    template_name = "users_list.html"


class UserCreate(SuccessMessageMixin, CreateView):
    form_class = MyRegisterUserForm
    template_name = "register.html"
    success_url = reverse_lazy('user_login')
    success_message = _('Пользователь успешно зарегистрирован')


class UsersDetail(DetailView):
    model = User
    template_name = 'users_details.html'
    context_object_name = 'user_details'


class UserUpdate(MyLoginRequiredMixin, MyUserPermissionMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = MyRegisterUserForm
    template_name = "update.html"
    success_url = reverse_lazy('users_list')
    success_message = _('Пользователь успешно изменён')


class UserDelete(MyLoginRequiredMixin, MyUserPermissionMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = "users_delete.html"
    success_url = reverse_lazy('users_list')
    success_message = _('Пользователь успешно удалён')

    def post(self, request, *args, **kwargs):
        if self.get_object().author.all() or self.get_object().tasks.all():
            messages.error(
                request, _('Невозможно удалить пользователя, потому что он связан с задачами.'))
            return redirect('users_list')

        return super().post(request, *args, **kwargs)


class TestPage(TemplateView):
    template_name = "test.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['aaa'] = 'Privet!'
        context['aaa'] = self.request.user.id
        return context


class TestPage2(ListView):
    model = User
    template_name = "test.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['aaa'] = 'Privet!'
        context['aaa'] = self.request.user.id
        return context


class LoginUser(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = "login.html"
    next_page = reverse_lazy('home')
    success_message = _('Вы залогинены!')


def logout_user(request):
    logout(request)
    messages.success(request, _("Вы разлогинены!"))
    return redirect('home')


class StatusList(MyLoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses_list.html"


class StatusCreate(MyLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = MyCreateStatusForm
    template_name = "statuses_create.html"
    success_url = reverse_lazy('statuses_list')
    success_message = _('Статус успешно создан')


class StatusUpdate(MyLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = MyCreateStatusForm
    template_name = "statuses_update.html"
    success_url = reverse_lazy('statuses_list')
    success_message = _('Статус успешно изменён')


class StatusDelete(MyLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "statuses_delete.html"
    success_url = reverse_lazy('statuses_list')
    success_message = _('Статус успешно удалён')

    def post(self, request, *args, **kwargs):
        if self.get_object().task_set.all():
            messages.error(request, _('Невозможно удалить статус, потому что он используется'))
            return redirect('statuses_list')

        return super().post(request, *args, **kwargs)


class TaskList(MyLoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks_list.html"


class TaskCreate(MyLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = MyCreateTaskForm
    template_name = "tasks_create.html"
    success_url = reverse_lazy('tasks_list')
    success_message = _('Задача успешно создана')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['btn'] = _("Создать")
        return context


class TaskUpdate(MyLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = MyCreateTaskForm
    template_name = "tasks_create.html"
    success_url = reverse_lazy('tasks_list')
    success_message = _('Задача успешно изменена')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['btn'] = _("Изменить")
        return context


class TaskDelete(MyLoginRequiredMixin, MyTaskPermissionMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "tasks_delete.html"
    success_url = reverse_lazy('tasks_list')
    success_message = _('Задача успешно удалена')


class TaskDetail(MyLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks_detail.html'
    context_object_name = 'task_detail'


class LabelList(MyLoginRequiredMixin, ListView):
    model = Label
    template_name = "labels_list.html"


class LabelCreate(MyLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = MyCreateLabelForm
    template_name = "labels_create.html"
    success_url = reverse_lazy('labels_list')
    success_message = _('Метка успешно создана')


class LabelUpdate(MyLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = MyCreateLabelForm
    template_name = "labels_update.html"
    success_url = reverse_lazy('labels_list')
    success_message = _('Метка успешно изменена')


class LabelDelete(MyLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = "labels_delete.html"
    success_url = reverse_lazy('labels_list')
    success_message = _('Метка успешно удалена')

    def post(self, request, *args, **kwargs):
        if self.get_object().task_set.all():
            messages.error(request, _('Невозможно удалить метку, потому что он связана с задачей.'))
            return redirect('labels_list')

        return super().post(request, *args, **kwargs)


class TaskListWithFilter(MyLoginRequiredMixin, FilterView):
    template_name = "tasks_list_with_filter.html"
    filterset_class = TaskFilter
