from django.db import models


# Create your models here.
class Diary(models.Model):
    nowDate = models.DateField()
    diaryContents = models.ManyToManyField("scripts.Script")
