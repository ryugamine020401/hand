"""
引用內建的forms
"""
from django import forms

class ReProfileForm(forms.Form):
    """
    使用者個人資料重設的表格
    """
    username = forms.CharField(
        label = "使用者名稱",
        widget = forms.TextInput()
    )
    headimg = forms.ImageField(
        label = "頭貼",
                # 可以讓使用者選擇輸入的東東
        widget = forms.ClearableFileInput()
    )
    describe = forms.CharField(
        label = "描述",
        widget = forms.TextInput()
    )
    birthday = forms.DateField(
        label= "出生年月",
        widget = forms.DateInput(
                    # CSS可以定義使用者需要輸入的樣子
            attrs={'placeholder':'yyyy-mm-dd'}
        )
    )
    email = forms.CharField(
        label = "電子郵件",
        widget = forms.EmailInput()
    )
