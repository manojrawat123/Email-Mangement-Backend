from rest_framework import serializers
from submenu.serializer import SubMenuSerializer 
from menu.models import Menu

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Menu