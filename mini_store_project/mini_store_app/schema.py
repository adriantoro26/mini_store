import graphene
import graphql
import graphql_jwt
from graphene_django import DjangoObjectType
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
      return models.Product.objects.all().order_by('-createdAt')

   def resolve_product(self, info, product_id):
      if not info.context.user.is_authenticated:
         raise graphql.GraphQLError('User not authenticated') 
      return models.Product.objects.get(pk=product_id)

   def resolve_all_orders(self, info):
      if not info.context.user.is_authenticated:
         raise graphql.GraphQLError('User not authenticated') 

      if info.context.user.is_seller:
         raise graphql.GraphQLError('Not a customer')

      return models.Order.objects.filter(customer=info.context.user).order_by('-createdAt')
class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)
class AddProductInput(graphene.InputObjectType):
   title = graphene.String(required=True)
   description = graphene.String(required=True)
   price = graphene.Decimal(max_digits = 5, decimal_places= 2, required=True)

# Separate input types are used for adding and updating a product in order to update a product without inserting every field.
class UpdateProductInput(graphene.InputObjectType):
   title = graphene.String()
   description = graphene.String()
   price = graphene.Decimal(max_digits = 5, decimal_places= 2)
class AddProduct(graphene.Mutation):
   class Arguments:
      product_input = AddProductInput(required=True)

   product = graphene.Field(ProductType)

   @staticmethod
   def mutate(root, info, product_input=None):
      if not info.context.user.is_authenticated:
         raise graphql.GraphQLError('User not authenticated')

      if not info.context.user.is_seller:
         raise graphql.GraphQLError('Not a seller')

      product = models.Product.objects.create(title=product_input.title, description=product_input.description, price=product_input.price, creator=info.context.user)  
      return AddProduct(product=product)
class UpdateProduct(graphene.Mutation):
   class Arguments:
      product_id = graphene.ID(required=True)
      product_input = UpdateProductInput(required=True)

   product = graphene.Field(ProductType)

   @staticmethod
   def mutate(root, info, product_id=None, product_input=None):
      if not info.context.user.is_authenticated:
         raise graphql.GraphQLError('User not authenticated')
      if not info.context.user.is_seller:
         raise graphql.GraphQLError('Not a seller')
      try:
         product = models.Product.objects.get(pk=product_id)
      except:
         return graphql.GraphQLError('Product not found')

      if not product.creator == info.context.user:
         raise graphql.GraphQLError('User not authorized')

      if product_input.title:
         product.title = product_input.title
      if product_input.description:
         product.description = product_input.description
      if product_input.price:
         product.price = product_input.price  
      product.save()
      return UpdateProduct(product=product)
class DeleteProduct(graphene.Mutation):
   class Arguments:
      product_id = graphene.ID(required=True)

   message = graphene.String()
   @staticmethod
   def mutate(root, info, product_id=None):
      if not info.context.user.is_authenticated:
         raise graphql.GraphQLError('User not authenticated')
      if not info.context.user.is_seller:
         raise graphql.GraphQLError('Not a seller')
         
      try:
         product = models.Product.objects.get(pk=product_id)
      except:
         return graphql.GraphQLError('Product not found')

      if not product.creator == info.context.user:
         raise graphql.GraphQLError('User not authorized')

      product.delete()

      return DeleteProduct(message='Product removed successfully')
class Mutation(graphene.ObjectType):
   login = ObtainJSONWebToken.Field()
   verify_token = graphql_jwt.Verify.Field()
   refresh_token = graphql_jwt.Refresh.Field()
   add_product = AddProduct.Field()
   update_product = UpdateProduct.Field()
   delete_product = DeleteProduct.Field()
   
schema = graphene.Schema(query=Query, mutation=Mutation)