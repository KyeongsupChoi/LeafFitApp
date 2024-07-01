# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User



class RepMax(models.Model):
    weight = models.IntegerField(max_length=200)

    def __str__(self):
        return self.title

# Create your models here.

