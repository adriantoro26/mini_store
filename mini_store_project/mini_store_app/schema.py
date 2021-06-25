import graphene
import graphql
import graphql_jwt
from graphene_django import DjangoObjectType, DjangoListField 
from graphql_jwt.decorators import login_required
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
      if not info.context.user.is_authenticated:
         raise graphql.GraphQLError('User not authenticated')  
      return models.Product.objects.all()

   def resolve_product(self, info, product_id):
      if not info.context.user.is_authenticated:
         raise graphql.GraphQLError('User not authenticated') 
      return models.Product.objects.get(pk=product_id)

   def resolve_all_orders(self, info):
      if not info.context.user.is_authenticated:
         raise graphql.GraphQLError('User not authenticated') 
      return models.Order.objects.filter(customer=info.context.user)
class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)
class Mutation(graphene.ObjectType):
   login = ObtainJSONWebToken.Field()
   verify_token = graphql_jwt.Verify.Field()
   refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)