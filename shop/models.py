from Reti_Kapchi.settings import TIME_ZONE
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.base import Model
from django.utils import timezone


# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    selling_price = models.FloatField(null=False, blank=False, default=0.00)
    discounted_price = models.FloatField(null=False, blank=False, default=0.00)
    image = models.ImageField(blank=True, null=True)
    type = models.ForeignKey(
        Categories, on_delete=models.CASCADE, related_name="products")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


stars = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
)


class Testimonial(models.Model):
    name = models.CharField(max_length=255, null=True)
    testimony = models.TextField(null=True)
    rating = models.CharField(max_length=10, choices=stars, default="1")

    def __str__(self):
        return self.name


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="review")
    name = models.CharField(max_length=255)
    rating = models.CharField(max_length=10, choices=stars, default="1")
    review = models.TextField(null=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pincode = models.IntegerField()
    state = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user.username

    @property
    def product_cost(self):
        return self.quantity * self.product. discounted_price


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.status

    @property
    def product_cost(self):
        return self.quantity * self.product.discounted_price


class Transaction(models.Model):
    made_by = models.ForeignKey(
        User, related_name='transaction', on_delete=models.CASCADE)
    made_on = models.DateTimeField(default=timezone.now)
    amount = models.IntegerField()
    order_id = models.CharField(
        unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime(
                'PAY2ME%Y%m%dODR')+str(self.id)
        print(self.order_id, self.made_on, self.id, "##################")
        return super().save(*args, *kwargs)
