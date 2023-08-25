"""
用來繼承原本就有的物件，可以直接使用。
"""
from django.db import models

class TeachWordCard(models.Model):
    """
    基本有的字卡。
    """
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='studyimage/english', blank=False, null= False)
    upload_date = models.DateField(default='1900-01-01')
    describe = models.CharField(max_length=100)
    objects = models.Manager()

    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'TeachWordCard'

class TeachType(models.Model):
    """
    學習中心有的資源，英文、中文等。
    """
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    objects = models.Manager()
    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'Teach'

class Test1(models.Model):
    """
    英文測驗的題目，
    """
    id = models.AutoField(primary_key=True)
    mondai = models.CharField(max_length=50)
    objects = models.Manager()


    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'Test1'

class Test2(models.Model):
    """
    中文測驗的題目，
    """
    id = models.AutoField(primary_key=True)
    mondai = models.CharField(max_length=50)
    objects = models.Manager()

    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'Test2'

class Test1Ans(models.Model):
    """
    英文測驗的題目，
    """
    id = models.AutoField(primary_key=True)
    kotae_ichi = models.CharField(max_length=20)
    kotae_ni = models.CharField(max_length=20)
    kotae_san = models.CharField(max_length=20)
    kotae_yon = models.CharField(max_length=20)
    kotae_go = models.CharField(max_length=20)
    user_id = models.ForeignKey('reg.UserIfm', to_field='id', on_delete=models.CASCADE)
    cor_rate = models.FloatField(default=100.0)
    objects = models.Manager()

    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'Test1Ans'

class Test2Ans(models.Model):
    """
    英文測驗的題目，
    """
    id = models.AutoField(primary_key=True)
    kotae_ichi = models.CharField(max_length=20)
    kotae_ni = models.CharField(max_length=20)
    kotae_san = models.CharField(max_length=20)
    kotae_yon = models.CharField(max_length=20)
    kotae_go = models.CharField(max_length=20)
    user_id = models.ForeignKey('reg.UserIfm', to_field='id', on_delete=models.CASCADE)
    cor_rate = models.FloatField(default=100.0)
    objects = models.Manager()

    class META:
        """
        定義這個DATABESE的名字
        """
        db_name = 'Test2Ans'
