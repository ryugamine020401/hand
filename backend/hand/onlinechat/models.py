"""
用來繼承原本就有的物件，可以直接使用。
"""
from django.db import models


class OlineChatroom(models.Model):
    """
    英文測驗的題目，
    """
    id = models.AutoField(primary_key=True)
    message = models.TextField()
    username = models.CharField(max_length=100, default='我沒有登入')
    message_img = models.CharField(max_length=100)
    objects = models.Manager()

    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'OlineChatroom'
