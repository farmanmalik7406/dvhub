from django import forms
from django.contrib.auth.models import User
from django.forms import Form
from django.forms import ModelForm

from user_system.models import Todo


class TodoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TodoForm, self).__init__(*args, **kwargs)
        self.fields['create_date'].widget.attrs = {'class': 'datepicker'}
        self.fields['on_date'].widget.attrs = {'class': 'datepicker'}

    class Meta:
        model = Todo
        fields = ["title", "description", "create_date", "on_date"]
        labels = ["Title", "Description", "Create Date", "TODO date"]


class LoginForm(Form):
    username = forms.CharField(max_length=50, label="User Name", required=True)
    password = forms.CharField(max_length=50, label="password", required=True, widget=forms.PasswordInput)


class RegistrationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget=forms.PasswordInput()

    class Meta:
        model = User
        fields = ["username","first_name", "last_name", "email", "password"]

