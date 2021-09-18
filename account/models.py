from django.db import models
from django.contrib.auth.models import User

class ThumbnailSize(models.Model):
    name = models.CharField(max_length=200)
    height = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Plan(models.Model):
    name = models.CharField(max_length=200)
    thumbnails_id = models.ManyToManyField(ThumbnailSize)
    def __str__(self):
        return f'{self.name}'

class SpecialUser(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id.username} Plan: {self.plan_id.name}'