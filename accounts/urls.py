from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view, post_registration_view
from main.views import menu 
from .views import register, user_login
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", user_login, name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),  # Выход с редиректом на login
    path('register/', register_view, name='register'),
    path('welcome/', post_registration_view, name='post_registration'),
    path("menu/", menu, name="menu"),
    
]
