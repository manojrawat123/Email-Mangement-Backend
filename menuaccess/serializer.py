from rest_framework import serializers
from menuaccess.models import MenuAccess
from submenu.models import Submenu

class MenuAccessSerializer(serializers.ModelSerializer):
    sub_menu = serializers.PrimaryKeyRelatedField(queryset=Submenu.objects.all(), required=False)
    class Meta:
        fields = "__all__"
        model = MenuAccess