"""
用來繼承原本就有的物件，可以直接使用。
"""
from django.db import models


# Create your models here.
class Discuss(models.Model):
    """
    使用者基本的資料，驗證狀況。
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('reg.UserIfm', to_field='id', on_delete=models.CASCADE, null=True, related_name='forum_user')
    content = models.TextField()
    title = models.CharField(max_length=30)
    upload_date = models.DateField(default=False)
    objects = models.Manager()

    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'Discuss'
class DiscussResponse(models.Model):
    """
    使用者基本的資料，驗證狀況。
    """
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('reg.UserIfm', to_field ='id', on_delete=models.SET_NULL, null=True)
    response = models.TextField()
    dis_id = models.ForeignKey('Discuss', to_field='id', on_delete=models.CASCADE)
    upload_date = models.DateField(default=False)
    objects = models.Manager()

    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'DiscussResponse'
