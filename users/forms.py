from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.validators import MinLengthValidator
from .models import User, UserMessages

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput)
    class Meta:
        model = User
        fields = ('username', 'password1')

class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput, error_messages={'unique': 'Пользователь с таким именем уже существует.'})
    password1 = forms.CharField(widget=forms.PasswordInput, validators=[MinLengthValidator(limit_value=6, message='Пароль должен быть не короче 6 символов')])
    password2 = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ('username', 'password1')


class SendMessaggesForm(forms.ModelForm):
    class Meta:
        model = UserMessages
        fields = ('message',)
        