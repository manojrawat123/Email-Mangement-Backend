from vendorrate.models import VendorRate
from rest_framework import serializers

class VendorRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRate
        fields = "__all__"
