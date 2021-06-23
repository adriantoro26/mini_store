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
      products = models.Product.objects.all()
      serializer = serializers.ProductSerializer(products, many=True)
      return Response({'products':serializer.data})

   def post(self, request):

      if not request.user.is_authenticated:
         return Response({'message':'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)

      serializer = serializers.ProductSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save(creator=request.user)
         return Response({'post':serializer.data}, status=status.HTTP_201_CREATED)
      else:
         print('error', serializer.errors)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CartView(APIView):

   def get(self, request):
      if not request.user.is_authenticated:
         return Response({'message':'Not authenticated'}, status=status.HTTP_404_NOT_FOUND) 
      
      cart = models.Cart.objects.filter(customer=request.user)
      if cart:
         cart_items = models.CartItem.objects.filter(cart=cart[0])
         serializer = serializers.CartItemSerializer(cart_items, many=True)
         
         total = 0
         for item in cart_items:
            # product = models.Product.objects.get(pk=item.product)
            total += item.quantity*item.product.price
         
         return Response({'cart':serializer.data, 'total':total})

      return Response({'message':'Cart is empty'})

   def post(self, request):
      if not request.user.is_authenticated:
         return Response({'message':'Not authenticated'}, status=status.HTTP_404_NOT_FOUND) 

      product_id = request.data['product_id']
      if not product_id:
         return Response({'message':'Not Found'}, status=status.HTTP_404_NOT_FOUND)

      (cart, created) = models.Cart.objects.get_or_create(customer=request.user)

      cart_item = models.CartItem.objects.filter(cart=cart, product=product_id)

      if not cart_item:
         cart_item = models.CartItem.objects.create(cart=cart, product=product_id)
         serializer = serializers.CartItemSerializer(cart_item)
         return Response({'cartItem': serializer.data})
      
      cart_item[0].quantity += 1
      cart_item[0].save()
      serializer = serializers.CartItemSerializer(cart_item[0])        

      return Response({'cartItem': serializer.data})

