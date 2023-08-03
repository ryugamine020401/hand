"""
用來繼承原本就有的物件，可以直接使用。
"""
from django.db import models


# Create your models here.
class BugSheet(models.Model):
    """
    使用者基本的資料，驗證狀況。
    """
    id = models.IntegerField(primary_key=True)
    context = models.TextField()
    upload_date = models.DateField(default=False)


    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'BugSheet'
