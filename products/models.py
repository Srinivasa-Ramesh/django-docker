from django.db import models

# Create your models here.
class Product(models.Model):
    objects = None
    name = models.CharField(max_length=223)
    price = models.IntegerField()
    disc = models.IntegerField()
    image_url = models.CharField(max_length=2083)
    def __str__(self):
        return self.name
