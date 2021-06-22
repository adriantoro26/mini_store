from . import models
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

   class Meta:
      model = models.User
      fields = '__all__'

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