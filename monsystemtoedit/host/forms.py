from django import forms
from django.core import validators
from .models import all_users_data

def check_for_positive(value):
    if value < 0:
        raise forms.ValidationError('NEEDS TO BE GREATER THEAN 0!')

class DoubleCheck(forms.ModelForm):
    # Form Fields go here
    class Meta:
        model = all_users_data
        exclude = ['name']

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserLoginForm(AuthenticationForm):
    # Добавьте дополнительные поля, если нужно
    pass

class UserRegistrationForm(UserCreationForm):
    # Добавьте дополнительные поля, если нужно
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
