from django import forms
from sales.models import User
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "mobile")
        error_messages = {
                    'mobile': {
                        'min_value':"This writer's name is too long.",
                        'min_length':"This writer's name is too long.",
                        'min':"This writer's name is too long.",
                    },
                }
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["mobile"] = forms.IntegerField(min_value = 1000000000, max_value = 9999999999)
        # breakpoint()


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()