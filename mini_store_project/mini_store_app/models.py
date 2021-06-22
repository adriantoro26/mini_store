from django.db import models
# Base Djando user model.
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.fields.related import OneToOneField

# Create your models here.
class User(AbstractBaseUser):
   name = models.CharField(max_length=255, null=False)
   lastLname = models.CharField(max_length=255, null=False)
   email = models.EmailField(max_length=255, unique=True, null=False)
   is_seller = models.BooleanField(default=False) # Default: Buyer.

   def __str__(self):
      return self.email
class Cart(models.Model):
   buyer_id = models.OneToOneField(User, on_delete= models.CASCADE)
class Orders(models.Model):
   buyer_id = models.ForeignKey(User, on_delete= models.CASCADE) # Many to one relationship.
class Products(models.Model):
   title = models.CharField(max_length=20, null=False)
   description = models.TextField(null=False)
   price = models.FloatField(null=False) # By default it is USD.
   creator_id = models.ForeignKey(User, on_delete=models.CASCADE) # Many to one Relationship.
   cart_id = models.ManyToManyField(Cart) 
   order_id = models.ManyToManyField(Orders) 
   createdAt = models.DateTimeField(auto_now_add=True)
   updateAt = models.DateTimeField(auto_now=True)

   def __str__(self):
      return self.title