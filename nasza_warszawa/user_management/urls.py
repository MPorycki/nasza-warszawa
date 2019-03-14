from django.urls import path
from .views import register, logout


app_name = 'user_management'

urlpatterns = [
    path('register/', register),
    path('logout/', logout)
]