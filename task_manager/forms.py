from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext as _
from .models import Task, Status, Label


class MyRegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label=_('Имя пользователя'),
        widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(
        label=_('Имя'),
        widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(
        label=_('Фамилия'),
        widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(
        label=_('Подтверждение пароля'),
        widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2'
        )


class MyCreateStatusForm(forms.ModelForm):
    name = forms.CharField(
        label=_('Имя'),
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Status
        fields = ('name',)


class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.first_name + " " + obj.last_name)


class MyCreateTaskForm(forms.ModelForm):
    name = forms.CharField(
        label=_('Имя'),
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    description = forms.CharField(
        label=_('Описание'),
        required=False,
        widget=forms.Textarea(
            attrs={'cols': '40', 'rows': '10', 'class': 'form-input'}
        ))
    status = forms.ModelChoiceField(
        label=_('Статус'),
        queryset=Status.objects.all()
    )
    executor = MyModelChoiceField(
        label=_('Исполнитель'),
        queryset=User.objects.all(),
        required=False)
    labels = forms.ModelMultipleChoiceField(
        label=_('Метки'),
        queryset=Label.objects.all(),
        required=False)

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'labels')


class MyCreateLabelForm(forms.ModelForm):
    name = forms.CharField(
        label=_('Имя'),
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Label
        fields = ('name',)
