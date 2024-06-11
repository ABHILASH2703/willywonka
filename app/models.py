from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Signuptable(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='signuptable', null=True, blank=True)
    first_name = models.CharField(max_length=100, default='default')
    last_name = models.CharField(max_length=100, default='default')
    mobile = models.IntegerField(default=0)
    email = models.EmailField(max_length=100, unique=True)
    place = models.CharField(max_length=100, default='default')
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, default='default')

    def __str__(self):
        return self.first_name

class Producttable(models.Model):
    product_name = models.CharField(max_length=100)
    image = models.FileField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.product_name

class Chocolatetable(Producttable):
    pass

class Caketable(Producttable):
    pass

class Carttable(models.Model):
    product_id = models.IntegerField(default=0)
    image = models.FileField()
    product_name = models.CharField(max_length=100, default='default')
    quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.CharField(max_length=100, default='default')

    def __str__(self):
        return self.product_name

class Billtable(models.Model):
    product_id = models.IntegerField(default=0)
    first_name = models.CharField(max_length=100, default='default')
    last_name = models.CharField(max_length=100, default='default')
    mobile = models.IntegerField(default=0)
    email = models.EmailField(default='default@default.com')
    date = models.DateField(default=timezone.now)
    product_name = models.CharField(max_length=100, default='default')
    quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.CharField(max_length=100, default='default')

    def __str__(self):
        return self.product_name
