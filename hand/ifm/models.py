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
    user_id_ifm = models.ForeignKey('reg.UserIfm', to_field='id', on_delete=models.CASCADE)
    img = models.CharField(max_length=100)
    word = models.CharField(max_length=10)
    upload_date = models.DateTimeField(default=False)
    objects = models.Manager()

    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'UseWordCard'

class UserDefIfm(models.Model):
    """
    使用者定義的資料。
    """
    id = models.AutoField(primary_key=True) # 自動生成累進的數字
    headimg = models.CharField(max_length=100)
    describe = models.CharField(max_length=256)
    user_id = models.ForeignKey('reg.UserIfm', to_field='id', on_delete = models.CASCADE, related_name='ifm_user')
    score = models.FloatField(default=0.0, null=True)
    objects = models.Manager()
    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'UserDefIfm'
