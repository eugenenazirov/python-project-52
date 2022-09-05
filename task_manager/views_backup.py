from django.shortcuts import render, redirect
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
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import TaskFilter
from django_filters.views import FilterView


def base(request):
    return render(request, 'base.html', context={})


# def users(request):
#     users_list = User.objects.all()
#     return render(request, 'users.html', context={
#         'users_list': users_list,
#     })


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


class UserUpdate(SuccessMessageMixin, UpdateView):
    model = User
    form_class = MyRegisterUserForm
    template_name = "update.html"
    success_url = reverse_lazy('users_list')
    success_message = _('Пользователь успешно изменён')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        if self.get_object().pk is not request.user.id and not request.user.is_superuser:
            # return HttpResponse("Permission's error")
            messages.error(request, _("У вас нет прав для изменения другого пользователя"))
            return redirect('users_list')
        return super().dispatch(request, *args, **kwargs)


class UserDelete(SuccessMessageMixin, DeleteView):
    model = User
    template_name = "users_delete.html"
    success_url = reverse_lazy('users_list')
    success_message = _('Пользователь успешно удалён')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        if self.get_object().pk is not request.user.id and not request.user.is_superuser:
            messages.error(request, _("У вас нет прав для изменения другого пользователя"))
            return redirect('users_list')
        return super().dispatch(request, *args, **kwargs)

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


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "login.html"

    def get_success_url(self) -> str:
        messages.success(self.request, _("Вы залогинены!"))
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    messages.success(request, _("Вы разлогинены!"))
    return redirect('home')


class StatusList(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses_list.html"
    login_url = reverse_lazy('user_login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)


class StatusCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = MyCreateStatusForm
    template_name = "statuses_create.html"
    success_url = reverse_lazy('statuses_list')
    success_message = _('Статус успешно создан')
    login_url = reverse_lazy('user_login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)


class StatusUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = MyCreateStatusForm
    template_name = "statuses_update.html"
    success_url = reverse_lazy('statuses_list')
    success_message = _('Статус успешно изменён')
    login_url = reverse_lazy('user_login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)


class StatusDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "statuses_delete.html"
    success_url = reverse_lazy('statuses_list')
    success_message = _('Статус успешно удалён')
    login_url = reverse_lazy('user_login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.get_object().task_set.all():
            messages.error(request, _('Невозможно удалить статус, потому что он используется'))
            return redirect('statuses_list')

        return super().post(request, *args, **kwargs)


class TaskList(ListView):
    model = Task
    template_name = "tasks_list.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)


class TaskCreate(SuccessMessageMixin, CreateView):
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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)


class TaskUpdate(SuccessMessageMixin, UpdateView):
    model = Task
    form_class = MyCreateTaskForm
    template_name = "tasks_create.html"
    success_url = reverse_lazy('tasks_list')
    success_message = _('Задача успешно изменена')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['btn'] = _("Изменить")
        return context


class TaskDelete(SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "tasks_delete.html"
    success_url = reverse_lazy('tasks_list')
    success_message = _('Задача успешно удалена')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        if self.get_object().author.id is not request.user.id and not request.user.is_superuser:
            # return HttpResponse("Permission's error")
            messages.error(request, _("У вас нет прав для удаления задачи другого пользователя"))
            return redirect('tasks_list')
        return super().dispatch(request, *args, **kwargs)


class TaskDetail(DetailView):
    model = Task
    template_name = 'tasks_detail.html'
    context_object_name = 'task_detail'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)


class LabelList(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels_list.html"
    login_url = reverse_lazy('user_login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)


class LabelCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = MyCreateLabelForm
    template_name = "labels_create.html"
    success_url = reverse_lazy('labels_list')
    success_message = _('Метка успешно создана')
    login_url = reverse_lazy('user_login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)


class LabelUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = MyCreateLabelForm
    template_name = "labels_update.html"
    success_url = reverse_lazy('labels_list')
    success_message = _('Метка успешно изменена')
    login_url = reverse_lazy('user_login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)


class LabelDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = "labels_delete.html"
    success_url = reverse_lazy('labels_list')
    success_message = _('Метка успешно удалена')
    login_url = reverse_lazy('user_login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.get_object().task_set.all():
            messages.error(request, _('Невозможно удалить метку, потому что он связана с задачей.'))
            return redirect('labels_list')

        return super().post(request, *args, **kwargs)


class TaskListWithFilter(FilterView):
    template_name = "tasks_list_with_filter.html"
    filterset_class = TaskFilter

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)
