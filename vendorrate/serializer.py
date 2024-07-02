from vendorrate.models import VendorRate
from rest_framework import serializers
from vendorratetabel.serializer import VendorRateTabelGetSerializer

class VendorRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRate
        fields = "__all__"


class VendorRateGetSerializer(serializers.ModelSerializer):
    vendor_rate_id = VendorRateTabelGetSerializer()
    class Meta:
        model = VendorRate
        fields = "__all__"
