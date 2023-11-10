from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User, UserMessages

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password1')

class RegistrationForm(UserCreationForm):
    password2 = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ('username', 'password1')


class SendMessaggesForm(forms.ModelForm):
    class Meta:
        model = UserMessages
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={'class': 'input_form_msg'})
        }