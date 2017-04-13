from django import forms
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(error_messages={'required': '请填写您的姓名'})
    password = forms.CharField(min_length=6, error_messages={'required': '请填写您的密码',
                                                             'min_length': '密码不能少于6位'})


class RegisterForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('username', )
