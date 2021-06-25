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

      if not request.user.is_seller:
         return Response({'message':'Not a seller'}, status=status.HTTP_401_UNAUTHORIZED)

      serializer = serializers.ProductSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save(creator=request.user)
         return Response({'post':serializer.data}, status=status.HTTP_201_CREATED)
      else:
         print('error', serializer.errors)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SingleProductView(APIView):
   serializer_class = serializers.ProductSerializer

   def get(self, request, pk):
      if not request.user.is_authenticated:
         return Response({'message':'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)
      try:
         product = models.Product.objects.get(pk=pk)
      except:
         return Response({'message': 'Product not found'}, status.HTTP_404_NOT_FOUND)
      serializer = serializers.ProductSerializer(product)
      return Response({'product':serializer.data})

   def put(self, request, pk):
      if not request.user.is_authenticated:
         return Response({'message':'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)
      try:
         product = models.Product.objects.get(pk=pk)
      except:
         return Response({'message': 'Product not found'}, status.HTTP_404_NOT_FOUND)
      
      if not product.creator == request.user:
         return Response({'message':'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

      serializer = serializers.ProductSerializer(product, data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response({'product':serializer.data})
      return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
   
   def patch(self, request, pk):
      if not request.user.is_authenticated:
         return Response({'message':'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)
      try:
         product = models.Product.objects.get(pk=pk)
      except:
         return Response({'message': 'Product not found'}, status.HTTP_404_NOT_FOUND)
      
      if not product.creator == request.user:
         return Response({'message':'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

      serializer = serializers.ProductSerializer(product, data=request.data, partial=True)
      if serializer.is_valid():
         serializer.save()
         return Response({'product':serializer.data})
      return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
   
   def delete(self, request, pk):
      if not request.user.is_authenticated:
         return Response({'message':'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)
      try:
         product = models.Product.objects.get(pk=pk)
      except:
         return Response({'message': 'Product not found'}, status.HTTP_404_NOT_FOUND)
      
      if not product.creator == request.user:
         return Response({'message':'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

      product.delete()
      return Response({'message': 'Product removed successfully'})
class CartView(APIView):

   def get(self, request):
      if not request.user.is_authenticated:
         return Response({'message':'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)       
      
      if request.user.is_seller:
         return Response({'message':'Not a customer'}, status=status.HTTP_401_UNAUTHORIZED)
      
      try:         
         cart = request.user.cart        
      except:
         return Response({'message':'Cart not found'},status.HTTP_404_NOT_FOUND)     
     
      cart_items = cart.cartitem_set.all() # Relational Manager queryset
      serializer = serializers.CartItemSerializer(cart_items, many=True)
      
      total = 0
      for item in cart_items:
         # product = models.Product.objects.get(pk=item.product)
         total += item.quantity*item.product.price
      
      return Response({'cart':{'id':cart.id,'items':serializer.data, 'total':total}})    

   def post(self, request):
      if not request.user.is_authenticated:
         return Response({'message':'Not authenticated'}, status=status.HTTP_404_NOT_FOUND) 

      if request.user.is_seller:         
         return Response({'message':'Not a customer'}, status=status.HTTP_401_UNAUTHORIZED)

      product_id = request.data['product_id']
      if not product_id:
         return Response({'message':'Not Found'}, status=status.HTTP_404_NOT_FOUND)

      # (cart, created) = models.Cart.objects.get_or_create(customer=request.user)
      if not hasattr(request.user, 'cart'):
         cart = models.Cart.objects.create(customer = request.user)
      else:
         cart = request.user.cart
      try:
         product = models.Product.objects.get(pk=product_id)
      except:
         return Response({'message': 'Product not found'}, status.HTTP_404_NOT_FOUND)
      try:
         cart_item = cart.cartitem_set.get(product=product)
         cart_item.quantity += 1
         cart_item.save()
         serializer = serializers.CartItemSerializer(cart_item)
         return Response({'cartItem': serializer.data})
      except:  
         cart_item = cart.cartitem_set.create(product=product)
         serializer = serializers.CartItemSerializer(cart_item)
         return Response({'cartItem': serializer.data})
   
   def delete(self, request):
      if not request.user.is_authenticated:
         return Response({'message':'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)
      
      if request.user.is_seller:         
         return Response({'message':'Not a customer'}, status=status.HTTP_401_UNAUTHORIZED)

      product_id = request.data['product_id']

      try:
         product = models.Product.objects.get(pk=product_id)
      except:
         return Response({'message':'Product not found'}, status.HTTP_404_NOT_FOUND)
      try:
         cart = request.user.cart
      except:
         return Response({'message':'Cart not found'}, status.HTTP_404_NOT_FOUND)
      try:
         cart_item = cart.cartitem_set.get(product=product)         
      except:
         return Response({'message':'Item not found in cart'}, status.HTTP_404_NOT_FOUND)  

      cart_item.delete()
      return Response({'message': 'Item removed from Cart successfully'})
class OrderView(APIView):

   def get(self, request):
      if not request.user.is_authenticated:
         return Response({'message':'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)
      
      if request.user.is_seller:         
         return Response({'message':'Not a customer'}, status=status.HTTP_401_UNAUTHORIZED)
      
      # orders_list = models.Order.objects.filter(customer=request.user).order_by('-createdAt')
      orders_list = request.user.order_set.all().order_by('-createdAt')
      orders = []      
      for order in orders_list:         
         # items = models.OrderItem.objects.filter(order=order)
         items = order.orderitem_set.all() # Relational Manager queryset
         total = 0
         for item in items:
            total += item.quantity*item.product.price            
         serializer = serializers.OrderItemSerializer(items, many=True)
         orders.append({'id':order.id, 'createdAt':order.createdAt,'items':serializer.data, 'total':total})
      
      return Response({'orders':orders})

   def post(self, request):

      if not request.user.is_authenticated:
         return Response({'message':'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)
      
      if request.user.is_seller:         
         return Response({'message':'Not a customer'}, status=status.HTTP_401_UNAUTHORIZED)

      # Create an order based on current cart, then delete the cart.
      # Get user cart.

      if not hasattr(request.user, 'cart') or not request.user.cart.cartitem_set.all():
         return Response({'message':'Cart is empty'},status.HTTP_404_NOT_FOUND)
    
      cart = request.user.cart

      # Get cart items.
      cart_items = cart.cartitem_set.all().order_by('-createdAt')

      # Create order.
      order = request.user.order_set.create()
      total = 0
      for item in cart_items:
         order.orderitem_set.create(product=item.product, quantity = item.quantity)
         total += item.quantity*item.product.price
      order_items = order.orderitem_set.all()
      serializer = serializers.OrderItemSerializer(order_items, many = True)

      cart.delete()
      return Response({'order': {'id':order.id, 'items': serializer.data, 'total':total}})