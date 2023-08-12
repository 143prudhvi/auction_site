from django.db import models

# Create your models here.

class Product(models.Model):
    productId = models.AutoField(primary_key=True)
    sellerName = models.CharField(max_length=100)
    productDescription = models.TextField()
    pictureLocation = models.TextField()
    brand = models.CharField(max_length=50)

    def __str__(self):
        return self.productId
