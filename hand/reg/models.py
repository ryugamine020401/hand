"""
用來繼承原本就有的物件，可以直接使用。
"""
from django.db import models


class UserIfm(models.Model):
    """
    使用者基本的資料，驗證狀況。
    """
    Email = models.EmailField(blank=False, max_length=100, primary_key=True)
    Username = models.CharField(max_length=30)
    Password = models.CharField(max_length=256)
    id = models.IntegerField(default=0)
    Validation = models.BooleanField(default=False)
    Validation_Num = models.IntegerField(default=0)
    Birthday = models.DateField(default='1900-01-01')

    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'UserIfm'


class UserDefIfm(models.Model):
    """
    使用者基本的資料，驗證狀況。
    """
    id = models.IntegerField(primary_key=True)
    headimg = models.CharField(max_length=100)
    describe = models.CharField(max_length=256)
    user_id = models.IntegerField(default=0)
    score = models.FloatField(default=0.0)

    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'UserDefIfm'
