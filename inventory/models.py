from django.db import models
from django.contrib.auth.models import User

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):    
    name = models.CharField(max_length=255)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_discontinued = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    order_status_choices = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Cancelled', 'Cancelled'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=255, choices=order_status_choices, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
