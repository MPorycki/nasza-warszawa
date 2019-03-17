from django.shortcuts import render, redirect
from rest_framework import viewsets

from .serializers import AccountSerializer
from .models import UM_accounts


# Create your views here.
class AccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = UM_accounts.objects.all()