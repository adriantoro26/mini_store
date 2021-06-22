from . import models
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):

   class Meta:
      model = models.User
      fields = ('id', 'name', 'lastname', 'email', 'password', 'is_seller', 'is_active' )
      extra_kwargs = {'password': {'write_only':True}}

   def create(self, validated_data):
      user = models.User(
         name = validated_data['name'],
         lastname = validated_data['lastname'],
         email = validated_data['email'],
         is_seller = validated_data['is_seller']
      )

      user.set_password(validated_data['password'])
      user.save()
      return user

class LoginSerialiazer(TokenObtainPairSerializer):

   @classmethod
   def get_token(cls, user):
      token = super().get_token(user)

      # Add custom claims
      token['name'] = user.name
      token['email'] = user.email
      return token
