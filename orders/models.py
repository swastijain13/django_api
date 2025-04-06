from django.db import models
from django.contrib.auth.models import AbstractUser

from food_ordering_api import settings


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ordered_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.menu_item.name}"
