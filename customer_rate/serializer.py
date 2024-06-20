from rest_framework import serializers
from customer_rate.models import CustomerRateTable

class CustomerRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRateTable
        fields = "__all__"