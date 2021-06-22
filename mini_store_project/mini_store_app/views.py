from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from . import serializers
from . import models
# Create your views here.

class UserView(APIView):

   serializer_class = serializers.UserSerializer

   def post(self, request):
      serializer = serializers.UserSerializer(data = request.data)

      if serializer.is_valid():
         serializer.save()
         return Response({'message': 'User created successfully', 'data':serializer.data})
class LoginView(TokenObtainPairView):
   
   serializer_class = serializers.LoginSerialiazer
class ProductView(APIView):
   serializer_class = serializers.ProductSerializer

   def get(self, request):
      if not request.user.is_authenticated:
         return Response({'message':'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)
      products = models.Products.objects.all()
      serializer = serializers.ProductSerializer(products, many=True)
      return Response({'products':serializer.data})

   def post(self, request):

      if not request.user.is_authenticated:
         return Response({'message':'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)

      serializer = serializers.ProductSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save(creator_id=request.user)
         return Response({'post':serializer.data}, status=status.HTTP_201_CREATED)
      else:
         print('error', serializer.errors)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
