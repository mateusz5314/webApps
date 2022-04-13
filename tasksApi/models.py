from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"({self.username}), {self.first_name} {self.last_name}"


class Table(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    access = models.ManyToManyField(User, related_name="access", blank=True)

    def __str__(self):
        return self.name
