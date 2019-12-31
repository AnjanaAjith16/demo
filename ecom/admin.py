from django.contrib import admin
from . models import Book, Author, Cart, CartItem, Order
# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
