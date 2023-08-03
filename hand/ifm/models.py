"""
用來繼承原本就有的物件，可以直接使用。
"""
from django.db import models


# Create your models here.
class UseWordCard(models.Model):
    """
    使用者基本的資料，驗證狀況。
    """
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey('reg.UserIfm', to_field='id', on_delete=models.CASCADE)
    img = models.CharField(max_length=100)
    word = models.CharField(max_length=10)
    upload_date = models.DateTimeField(default=False)


    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'UseWordCard'

class UserDefIfm(models.Model):
    """
    使用者基本的資料，驗證狀況。
    """
    id = models.IntegerField(primary_key=True)
    headimg = models.CharField(max_length=100)
    describe = models.CharField(max_length=256)
    user_id = models.ForeignKey('reg.UserIfm', to_field='id', on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)

    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'UserDefIfm'
