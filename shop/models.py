# models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    image_url = models.URLField()  # Adjust based on how you store images
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.IntegerField()  # Adjust based on how you store ratings

    def __str__(self):
        return self.name
