from django.shortcuts import render
from rest_framework.views import APIView
# from countrycode.country import country_data 
from country.models import CountryCode
from rest_framework.response import Response
from rest_framework import status
from country.serializer import CountryCodeSerializer

# Create your views here.
class CountryEntryView(APIView):
    def get(self, request, id=None):
        try:
            country_code = CountryCode.objects.filter(user_id = request.user.id)
            country_code_serializer = CountryCodeSerializer(country_code, many=True)
            return Response(country_code_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)