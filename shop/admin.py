from django.contrib import admin
from django.contrib.admin.options import get_content_type_for_model
from django.utils.decorators import classonlymethod
from .models import Cart, Categories, Customer, OrderPlaced, Product, Testimonial, ProductReview, Transaction, Wishlist
from . import models

# Register your models here.


@admin.register(Categories)
class categoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Product)
class productAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "testimony", "rating")


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "name", "rating", "review")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['User', 'name', 'Address', 'city', 'pincode', 'pincode']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']


@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['user', 'customer', 'product',
                    'quantity', 'ordered_date', 'status']


@admin.register(Transaction)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'made_by', 'made_on',
                    'amount', 'order_id', 'checksum']
