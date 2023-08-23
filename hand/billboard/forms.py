"""
引用內建的forms
"""
from django import forms
class BillboardForm(forms.Form):
    """
    用來顯示註冊表單。
    """
    title = forms.CharField(
        label = "標題",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    content = forms.CharField(
        label = "內文",
        widget=forms.Textarea()
    )
