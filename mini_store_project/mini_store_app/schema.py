import graphene

from graphene_django import DjangoObjectType, DjangoListField 
from . import models


class UserType(DjangoObjectType): 
   class Meta:
      model = models.User
      fields = ('id', 'name', 'lastname', 'email', 'is_seller')

class ProductType(DjangoObjectType): 
    class Meta:
        model = models.Product
        fields = "__all__"

class OrderItemType(DjangoObjectType): 
    class Meta:
        model = models.OrderItem
        fields = "__all__"

class OrderType(DjangoObjectType): 
    class Meta:
        model = models.Order
        fields = "__all__"
        
class Query(graphene.ObjectType):
   all_products = graphene.List(ProductType)
   product = graphene.Field(ProductType, product_id=graphene.Int())
   all_orders = graphene.List(OrderType)

   def resolve_all_products(self, info):
      return models.Product.objects.all()

   def resolve_product(self, info, product_id):
      return models.Product.objects.get(pk=product_id)
   
   def resolve_all_orders(self, info):
      return models.Order.objects.filter(customer=info.context.user)

schema = graphene.Schema(query=Query)