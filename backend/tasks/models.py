from django.db import models
from django.utils import timezone
from users.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.


class Team(models.Model):
    title = models.CharField(max_length=100)


class Plan(models.Model):
    title = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="plans")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Task(models.Model):
    title = models.CharField(max_length=100)
    responsibles = models.ManyToManyField(User, related_name="tasks")
    mentors = models.ManyToManyField(User, null=True)
    description = models.TextField(null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    depends_on = models.ForeignKey("Task", on_delete=models.SET_NULL, related_name="tasks", null=True)

    class Type(models.IntegerChoices):
        TASK = 1
        ISSUE = 2

    type = models.IntegerField(choices=Type.choices)

    class State(models.IntegerChoices):
        TODO = 1
        IN_PROGRESS = 2
        DONE = 3
        CLOSED = 4

    state = models.IntegerField(choices=State.choices)

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="tasks")
    column_order = models.IntegerField()
    #
    # def save(self, *args, **kwargs):
    #     super(Task, self).save(*args, **kwargs)


class Notification(models.Model):
    checked = models.BooleanField()
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="notifications"
    )
    timestamp = models.DateTimeField(auto_now_add=timezone.now)


class History(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="histories")
    timestamp = models.DateTimeField(auto_now_add=timezone.now)

    class Type(models.IntegerChoices):
        INITIALIZE = 1
        FINISH = 2
        CHANGE_DESCRIPTION = 3
        CHANGE_STATE = 4

    type = models.IntegerField(choices=Type.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='histories')
