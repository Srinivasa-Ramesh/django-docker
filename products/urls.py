from django.urls import path
from .views import register,user_login,user_logout,user_home,cart

urlpatterns = [
    path('home/',user_home,name='home'),
    path('login/',user_login,name ='login'),
    path('',register,name ='register'),
    path('logout/',user_logout,name ='logout'),
    path('home/cart/',cart, name="cart"),
]
