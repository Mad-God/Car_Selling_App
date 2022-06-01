from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", 'username', "password")
    
    
    # def save(self, commit=True, **kwargs):
    #     m = super(CustomUserCreationForm, self).save(commit=True)
    #     return m



class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()