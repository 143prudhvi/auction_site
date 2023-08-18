from django.db import models

# Create your models here.

class Product(models.Model):
    productId = models.CharField(primary_key=True, max_length=30)
    sellerName = models.CharField(max_length=100)
    productDescription = models.TextField()
    pictureLocation = models.TextField()
    brand = models.CharField(max_length=50)

    def __str__(self):
        return self.productId
