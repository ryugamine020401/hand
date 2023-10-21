"""
用來繼承原本就有的物件，可以直接使用。
"""
from django.db import models


class UserIfm(models.Model):
    """
    使用者基本的資料，驗證狀況。
    """
    email = models.EmailField(blank=False, max_length=100, primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=256)
    id = models.IntegerField(default=0, unique=True)
    validation = models.BooleanField(default=False)
    validation_num = models.IntegerField(default=0)
    birthday = models.DateField(default='1900-01-01')
    objects = models.Manager()
    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'UserIfm'
