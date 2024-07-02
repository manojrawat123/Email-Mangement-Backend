from vendorratetabel.models import VendorRateTabel
from rest_framework import serializers
from companycustomer.serializers import CustomerSerializer

class VendorRateTabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRateTabel
        fields = "__all__"


class VendorRateTabelGetSerializer(serializers.ModelSerializer):
    customer_id = CustomerSerializer()
    class Meta:
        model = VendorRateTabel
        fields = "__all__"