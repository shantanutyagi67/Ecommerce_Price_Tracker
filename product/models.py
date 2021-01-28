from django.db import models
from django.utils import timezone


# Create your models here.
class Product(models.Model):
    url = models.URLField(max_length=1000)
    price = models.FloatField()
    email = models.EmailField()
    created_at = models.DateTimeField(default = timezone.now())
