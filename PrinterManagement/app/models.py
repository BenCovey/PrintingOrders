"""
Definition of models.
"""
from django.conf import settings
from django.db import models

# Create your models here.
class order(models.Model):
    ID = models.IntegerField()
    ORDER_NAME = models.CharField(max_length=100)
    DESCRIPTION = models.CharField(max_length=1000)
    LINK = models.CharField(max_length=255)
    ORDER_USER = models.CharField(max_length=100)
    FILES = models.BinaryField
    ORDER_DATE = models.CharField(max_length=100)
    ORDER_STATUS = models.CharField(max_length=100)
    ORDER_DATE_DELIVERED = models.CharField(max_length=100)
    ORDER_DATE_COMPLETED = models.CharField(max_length=100)
    COST_ESTIMATED = models.CharField(max_length=100)
    COST_CHARGED = models.CharField(max_length=100)
    objects = models.Manager()
