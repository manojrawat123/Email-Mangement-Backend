from django.shortcuts import render
from rest_framework.views import APIView
# from countrycode.country import country_data 
from countrycode.models import Country
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
# class CountryEntryView(APIView):
#     def get(self, request, id=None):
#         try:
#             objs = []
#             for i in country_data:
#                 objs.append(Country(
#                     code = i['code'],
#                     name = i['name']
#                 ))
#             Country.objects.bulk_create(objs)
#             return Response({"message" : "Country Code Save Successfully"})
#         except Exception as e:
#             print(e)
#             return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    