from rest_framework import serializers
from rate.models import RateTabel

class RateTableSerializers(serializers.ModelSerializer):
    class Meta:
        model = RateTabel
        fields = "__all__" 