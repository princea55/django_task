from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    ownerId = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.TextField()
    franchise_name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class FoodItems(models.Model):
    restaurantId = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    foodName = models.CharField(max_length=30)
    price = models.CharField(max_length=20)
    foodType = models.CharField(max_length=20)
    noOfVariety = models.IntegerField()

    def __str__(self):
        return self.foodName

class Orders(models.Model):
    FoodItemId = models.ForeignKey(FoodItems, on_delete=models.DO_NOTHING)
    restaurantId = models.ForeignKey(Restaurant, on_delete=models.DO_NOTHING)
    orderDate = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    tableNo = models.IntegerField()
    totalBill = models.IntegerField()
    noOdItems = models.IntegerField()

    def __str__(self):
        return str(self.FoodItemId)