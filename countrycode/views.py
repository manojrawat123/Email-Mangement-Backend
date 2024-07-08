from django.shortcuts import render
from rest_framework.views import APIView
# from countrycode.country import country_data 
from countrycode.models import NewCountryCode
from rest_framework.response import Response
from rest_framework import status
from countrycode.serializer import CountryCodeSerializer
from django.db.models import Q

# Create your views here.
class CountryEntryView(APIView):
    def get(self, request, id=None):
        try:
            country_code = NewCountryCode.objects.filter(Q(company_id = request.user.id) | Q(company_id = request.user.parent_user))
            country_code_serializer = CountryCodeSerializer(country_code, many=True)
            return Response(country_code_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)