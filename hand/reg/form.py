"""
引用內建的forms
"""
from django import forms
from django.forms import DateInput
class RegisterForm(forms.Form):
    """
    用來顯示註冊表單。
    """
    Username = forms.CharField(
        label = "暱稱",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    Email = forms.CharField(
        label = "帳號",
        widget=forms.EmailInput()
    )
    Password = forms.CharField(
        label = "密碼",
        widget=forms.PasswordInput()
    )
    Password_check = forms.CharField(
        label = "密碼確認",
        widget=forms.PasswordInput()
    )
    Birthday = forms.DateField(
        label= "生日",
        widget= DateInput()
    )
