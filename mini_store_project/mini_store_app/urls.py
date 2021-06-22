from django.urls import path
from . import views
urlpatterns = [
   path('signup', views.UserView.as_view())
]