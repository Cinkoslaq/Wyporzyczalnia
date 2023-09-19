from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Machinery(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    rental_price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    comments = models.ManyToManyField('Comments')

    def __str__(self):
        return self.name

class Rental(models.Model):
    machinery = models.ManyToManyField(Machinery)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Rental {self.id}"

class Delivery(models.Model):
    DELIVERY_CHOICES = (
        ('self-pickup', 'Self Pickup'),
        ('express-delivery', 'Express Delivery'),
        ('standard-delivery', 'Standard Delivery'),
    )
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE)
    delivery_type = models.CharField(max_length=50, choices=DELIVERY_CHOICES)

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    NIP = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.user.username

class Ratings(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()

class Comments(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    content = models.TextField()

