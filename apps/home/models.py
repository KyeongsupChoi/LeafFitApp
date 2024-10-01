# -*- encoding: utf-8 -*-
 

from django.db import models
from django.contrib.auth.models import User

from django.contrib.postgres.fields import JSONField  # If using PostgreSQL

from django.contrib.auth.models import User


class WendlerPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wendler_plans')
    name = models.CharField(max_length=100, default='Default Wendler Plan')
    weight = models.FloatField()
    exercise_data = models.JSONField(blank=True, null=True)  # For storing exercise plans as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class RepMax(models.Model):
    weight = models.IntegerField(max_length=200)

    def __str__(self):
        return self.title

# Create your models here.

