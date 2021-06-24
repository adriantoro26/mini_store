from django.db import models
# Base Djando user model.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Assings specific persmissions to users.
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class UserManager(BaseUserManager):

   def create_user(self, email, name, password = None):
      
      if not email:
         raise ValueError('Please provide an email address')

      email = self.normalize_email(email)

      # Create a new user profile.
      user = self.model(email = email, name = name)

      # This will encrypt the password first and then assign it to the user.
      user.set_password(password)

      # Save user into database.
      user.save(using = self._db)

      return user

   def create_superuser(self, email, name, password = None):

      user = self.create_user(email, name, password)
      user.is_superuser = True
      user.is_staff = True

      # Save user into database.
      user.save(using = self._db)

      return user
class User(AbstractBaseUser, PermissionsMixin):
   name = models.CharField(max_length=255, null=False)
   lastname = models.CharField(max_length=255, null=False)
   email = models.EmailField(max_length=255, unique=True, null=False)
   password = models.CharField(max_length=255)
   is_seller = models.BooleanField(default=False) # Default: Buyer.
   is_staff = models.BooleanField(default = False)
   objects = UserManager()
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['name']

   def get_full_name(self):
      return self.name 

   def get_short_name(self):
      return self.name 
   
   def __str__(self):
      # Convert the object to a string.
      return self.email      
class Product(models.Model):
   title = models.CharField(max_length=20, null=False)
   description = models.TextField(null=False)
   price = models.DecimalField(max_digits = 5, decimal_places= 2 ,null=False) # By default it is USD.
   creator = models.ForeignKey(User, on_delete=models.CASCADE) # Many to one Relationship.
   createdAt = models.DateTimeField(auto_now_add=True)
   updateAt = models.DateTimeField(auto_now=True)
   def __str__(self):
      return self.title
class Cart(models.Model):
   customer = models.OneToOneField(User, on_delete= models.CASCADE)
class CartItem(models.Model):
   cart = models.ForeignKey(Cart, on_delete= models.CASCADE)
   product = models.ForeignKey(Product, on_delete= models.CASCADE)
   quantity = models.IntegerField(default=1)
class Order(models.Model):
   customer = models.ForeignKey(User, on_delete= models.CASCADE) # Many to one relationship.
class OrderItem(models.Model):
   order = models.ForeignKey(Order, on_delete= models.CASCADE) # Many to one relationship.
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   quantity = models.IntegerField(default=1)