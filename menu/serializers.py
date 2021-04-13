
from rest_framework import serializers
from .models import Menu, MenuItem

class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'title', 'slug']
           
class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'link_title', 'link_url',
                  'link_page', 'open_in_new_tab']
           
        


