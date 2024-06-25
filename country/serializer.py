from rest_framework import serializers
from country.models import CountryCode

class CountryCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryCode
        fields = "__all__"
        