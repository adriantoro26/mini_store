from django.urls import path
from . import views
from rest_framework_simplejwt.views import  TokenObtainPairView, TokenRefreshView

urlpatterns = [
   path('auth/signup', views.UserView.as_view()),
   path('auth/login', views.LoginView.as_view()),
   path('product', views.ProductView.as_view()),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]