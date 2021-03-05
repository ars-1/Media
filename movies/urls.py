from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home),
    path('browse/', views.search, name="search"),
    path('movie/<str:pk>/', views.movie, name="movie"),

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('user/', views.userPage, name="user-page"),
]