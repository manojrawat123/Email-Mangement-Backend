from useripaddress.models import IpAdderessCompanyCustomer
from rest_framework import serializers

class UserIpAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = IpAdderessCompanyCustomer
        fields = "__all__"


        