from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

class Book(models.Model):
    book_title = models.CharField(max_length=150)
    publication_year = models.IntegerField()
    author = models.CharField(max_length=100)
    plot = models.TextField()

    def __str__(self):
        return self.book_title


from django.db import models

# Create your models here.
from django.db import models


# Create your models here.

class Product(models.Model):
    productname = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    image = models.CharField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return self.productname



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    @receiver(post_save, sender=User)  # add this
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)  # add this
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Movie(models.Model):
    file = models.FileField(upload_to='documents/')  # i changed None=True#
    image = models.ImageField(upload_to='images/')
