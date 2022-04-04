from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"({self.email}), {self.first_name} {self.last_name}"


class Task(models.Model):
    class Status(models.IntegerChoices):
        TODO = 1
        IN_PROGRESS = 2
        ON_HOLD = 3
        DONE = 4

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=600)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=Status.choices)

    def __str__(self):
        return self.name
