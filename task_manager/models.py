from django.db import models
from django.contrib.auth.models import User


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="author")
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="tasks")
    labels = models.ManyToManyField("Label", through="AttachLabelToTask", blank=True)
    time_create = models.DateTimeField(auto_now_add=True)


class AttachLabelToTask(models.Model):
    attach_label = models.ForeignKey(Task, on_delete=models.CASCADE)
    attach_task = models.ForeignKey("Label", on_delete=models.PROTECT)


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


def get_full_name(self):
    return self.first_name + " " + self.last_name


User.add_to_class("__str__", get_full_name)
