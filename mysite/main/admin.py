from django.contrib import admin
from .models import Book, Product, Profile, Movie

# Register your models here.
admin.site.register(Product)
admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(Movie)