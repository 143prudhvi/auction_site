from django.db import models

# Create your models here.

class Item(models.Model):
    itemId = models.CharField(max_length=30)
    sellerName = models.CharField(max_length=100, null=True)
    itemDescription = models.TextField(null=True)
    pictureLocation = models.TextField(null=True)
    brand = models.CharField(max_length=50, null=True)
    price = models.CharField(max_length=20, null=True)
    title = models.CharField(max_length=100, default=None, null=True)
    status = models.CharField(max_length=20, choices=[
        ('Active', 'Active'),
        ('Not Active', 'Not Active'),
        ('Sold', 'Sold'),
        ('Dataset', 'Dataset')
    ],
                              default='Active', null=True)
    url = models.CharField(max_length=200, default=None, null=True)
    platform = models.CharField(max_length=20, default=None, null=True)
    dateTime = models.CharField(max_length=30, default=None, null=True)
    isMatched = models.BooleanField(default=0)
    matchedCount = models.IntegerField(default=0, null=True)
    imageExist = models.BooleanField(default=0)
    isGrouped = models.BooleanField(default=0)
    groupId = models.CharField(max_length=40, default=None, null=True)
    isNewImage = models.BooleanField(default=0)
    isNewMatch = models.BooleanField(default=0)
    isNewGroup = models.BooleanField(default=0)
    def __str__(self):
        return self.itemId

class MatchItems(models.Model):
    itemId = models.CharField(max_length=30, default=None, null=True)
    matchedId = models.CharField(max_length=30, default=None, null=True)