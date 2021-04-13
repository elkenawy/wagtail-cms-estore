from django.shortcuts import render
from rest_framework import viewsets

from .serializers import MenuItemSerializer, MenuSerializer
from .models import Menu, MenuItem


class MenuViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    

class MenuItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
