from rest_framework import serializers
from submenu.models import Submenu

class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submenu
        fields = "__all__"
