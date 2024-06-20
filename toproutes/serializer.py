from rest_framework import serializers
from toproutes.models import Route

class TopRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"