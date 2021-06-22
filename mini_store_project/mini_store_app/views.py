from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from . import serializers
# Create your views here.

class UserView(APIView):

   serializer_class = serializers.UserSerializer

   def post(self, request):
      serializer = serializers.UserSerializer(data = request.data)

      if serializer.is_valid():
         serializer.save()
         return Response({'message': 'User created successfully', 'data':serializer.data})

class Login(TokenObtainPairView):
   
   serializer_class = serializers.LoginSerialiazer