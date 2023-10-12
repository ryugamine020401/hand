"""
用來繼承原本就有的物件，可以直接使用。
"""
from django.db import models


# Create your models here.
class Billboard(models.Model):
    """
    使用者基本的資料，驗證狀況。
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30, default="公告")
    content = models.TextField()
    upload_date = models.DateField(default=False)
    objects = models.Manager()
    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'Billboard'
