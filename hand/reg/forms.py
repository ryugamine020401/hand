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
        widget= DateInput(
            attrs={'placeholder':'yyyy-mm-dd'}
        )
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

class ResetPasswordForm(forms.Form):
    """
    用來顯示註冊表單。
    """
    email = forms.CharField(
        label = "帳號",
        widget=forms.EmailInput()
    )
    password_old = forms.CharField(
        label = "舊密碼",
        widget=forms.PasswordInput()
    )
    password_new = forms.CharField(
        label = "新密碼",
        widget=forms.PasswordInput()
    )
    password_check = forms.CharField(
        label = "確認密碼",
        widget=forms.PasswordInput()
    )

class EmailCheckForm(forms.Form):
    """
    用來顯示驗證碼表單。
    """
    validation_num = forms.IntegerField(
        label = "驗證碼",
        widget=forms.NumberInput()
    )

class DeleteForm(forms.Form):
    """
    用來顯示欲刪除使用者表單。
    """
    delete_num = forms.IntegerField(
        label = "欲刪除使用者id",
        widget=forms.NumberInput()
    )
    