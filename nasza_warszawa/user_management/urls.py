from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user_management')

urlpatterns = [
    path('', include(router.urls)),
]