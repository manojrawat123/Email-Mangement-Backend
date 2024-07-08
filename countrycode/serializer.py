from rest_framework import serializers
from countrycode.models import NewCountryCode

class CountryCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewCountryCode
        fields = "__all__"
        