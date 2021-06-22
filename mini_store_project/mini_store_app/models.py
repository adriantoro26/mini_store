from django.db import models
# Base Djando user model.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import OneToOneField

# Create your models here.
class UserManager(BaseUserManager):

   def create_user(self, email, name, lastname, is_seller,password = None):
      
      if not email:
         raise ValueError('Please provide an email address')

      email = self.normalize_email(email)

      # Create a new user profile.
      user = self.model(email = email, name = name, lastname = lastname, is_seller = is_seller)

      # This will encrypt the password first and then assign it to the user.
      user.set_password(password)

      # Save user into database.
      user.save(using = self._db)

      return user

   def create_superuser(self, email, name, lastname, password = None):

      user = self.create_user(email, name, lastname, True, password)
      user.is_superuser = True
      user.is_staff = True

      # Save user into database.
      user.save(using = self._db)

      return user
class User(AbstractBaseUser):
   name = models.CharField(max_length=255, null=False)
   lastname = models.CharField(max_length=255, null=False)
   email = models.EmailField(max_length=255, unique=True, null=False)
   password = models.CharField(max_length=255)
   is_seller = models.BooleanField(default=False) # Default: Buyer.
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