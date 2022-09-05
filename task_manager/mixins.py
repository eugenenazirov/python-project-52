from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect


class MyLoginRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _(
                "Вы не авторизованы! Пожалуйста, выполните вход."
            ))
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)


class MyUserPermissionMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().pk is not request.user.id \
                and not request.user.is_superuser:
            messages.error(request, _(
                "У вас нет прав для изменения другого пользователя"
            ))
            return redirect('users_list')
        return super().dispatch(request, *args, **kwargs)


class MyTaskPermissionMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author.id is not request.user.id \
                and not request.user.is_superuser:
            messages.error(request, _(
                "У вас нет прав для удаления задачи другого пользователя"
            ))
            return redirect('tasks_list')
        return super().dispatch(request, *args, **kwargs)
