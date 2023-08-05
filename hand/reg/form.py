"""
引用內建的forms
"""
from django import forms
from django.forms import DateInput
class RegisterForm(forms.Form):
    """
    用來顯示註冊表單。
    """
    username = forms.CharField(
        label = "暱稱",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        label = "帳號",
        widget=forms.EmailInput()
    )
    password = forms.CharField(
        label = "密碼",
        widget=forms.PasswordInput()
    )
    password_check = forms.CharField(
        label = "密碼確認",
        widget=forms.PasswordInput()
    )
    birthday = forms.DateField(
        label= "生日",
        widget= DateInput()
    )

class LoginForm(forms.Form):
    """
    用來顯示註冊表單。
    """
    email = forms.CharField(
        label = "帳號",
        widget=forms.EmailInput()
    )
    password = forms.CharField(
        label = "密碼",
        widget=forms.PasswordInput()
    )
