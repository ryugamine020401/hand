"""
用來繼承原本就有的物件，可以直接使用。
"""
from django.db import models


class OlineChatroom(models.Model):
    """
    英文測驗的題目，
    """
    id = models.IntegerField(primary_key=True)
    context = models.TextField()
    user = models.ForeignKey('reg.UserIfm', to_field='id', on_delete=models.CASCADE, related_name='onlinechat_user')
    context_img = models.CharField(max_length=100)

    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'OlineChatroom'
