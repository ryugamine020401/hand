"""
引用內建的forms
"""
from django import forms
class ForumForm(forms.Form):
    """
    用來顯示發送文章的表單。
    """
    title = forms.CharField(
        label = "標題",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    content = forms.CharField(
        label = "內文",
        widget=forms.Textarea()
    )

class ResponseForm(forms.Form):
    """
    用來顯示送出留言的表單。
    """
    response =forms.CharField(
        label = "回覆",
        widget=forms.Textarea()
    )
