from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=20)

    def __str__(self):
        return self.tag


class Script(models.Model):
    class LevelChoices(models.TextChoices):  # 어떻게......AI...?
        LEVEL1 = ("level1", "Level1")
        LEVEL2 = ("level2", "Level2")
        LEVEL3 = ("level3", "Level3")

    title = models.CharField(
        max_length=200,
        primary_key=True,
    )
    hashtag = models.ManyToManyField(Tag)
    contents = models.ForeignKey(
        "chats.RolePlayingRoom",
        on_delete=models.SET_NULL,
        related_name="scripts",
        null=True,
    )
    level = models.CharField(
        max_length=10,
        choices=LevelChoices.choices,
    )
    learningDate = models.DateField()
    email = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="scripts",
    )
