"""
引用內建的forms
"""
from django import forms

class UploadEnglishForm(forms.Form):
    """
    上傳圖片的表格，一次5個
    """
    img = forms.ImageField(
        label = "圖片",
        widget = forms.ClearableFileInput()
    )
    describe = forms.CharField(
        label = "描述",
        widget = forms.TextInput()
    )

class UploadTeachTypeForm(forms.Form):
    """
    上傳圖片的表格，一次5個
    """
    type = forms.CharField(
        label = "教學的類型",
        widget = forms.TextInput()
    )
