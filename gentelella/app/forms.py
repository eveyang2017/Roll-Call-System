from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"username",
        error_messages={'required': 'input username'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"username",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"password",
        error_messages={'required': u'input password'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"password",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"must input")
        else:
            cleaned_data = super(LoginForm, self).clean()


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

