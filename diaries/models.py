from django.db import models


# Create your models here.
class Diary(models.Model):
    nowDate = models.DateField()
    comment = models.TextField(
        null=True,
    )
    diaryContents = models.ManyToManyField("scripts.Script")
    user_email = models.ForeignKey(
        "users.USer",
        on_delete=models.CASCADE,
        related_name="diaries",
    )


#
