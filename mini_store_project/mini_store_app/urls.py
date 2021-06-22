from django.urls import path
from . import views
from rest_framework_simplejwt.views import  TokenObtainPairView, TokenRefreshView

urlpatterns = [
   path('signup', views.UserView.as_view()),
   path('login', views.Login.as_view()),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]