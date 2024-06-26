from vendorratetabel.models import VendorRateTabel
from rest_framework import serializers

class VendorRateTabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRateTabel
        fields = "__all__"