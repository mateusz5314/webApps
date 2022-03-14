from django.db import models


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Task(models.Model):
    class Status(models.IntegerChoices):
        TODO = 1
        IN_PROGRESS = 2
        ON_HOLD = 3
        DONE = 4

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=600)
    assignee = models.ForeignKey(Person, on_delete=models.CASCADE)
    status = models.IntegerField(choices=Status.choices)

    def __str__(self):
        return self.name
