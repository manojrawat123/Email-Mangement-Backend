from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from companycustomer.models import Customer
from companycustomer.serializers import CustomerSerializer
from management_profile.models import ManagementProfileName
from management_profile.serializers import ManagementProfileSerializer
import pandas as pd
import datetime
from django.db import connection, transaction
from vendorrate.models import VendorRate
from vendorrate.serializer import VendorRateSerializer
from vendorratetabel.models import VendorRateTabel
from vendorratetabel.serializer import VendorRateTabelSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


# Create your views here.
class VendorRateTabelView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        try:
            # Customer Details
            customer = Customer.objects.filter(Q(user_id = request.user.id) & Q(active = True))
            customer_serializer = CustomerSerializer(customer, many = True)

            # Vendor Rate Tabel
            vendor_rate_tabel = VendorRateTabel.objects.filter(Q(user_id = request.user.id))
            vendor_rate_tabel_serializer = VendorRateTabelSerializer(vendor_rate_tabel, many=True)

            return Response({
                "customer" : customer_serializer.data,
                "vendor_rate_tabel" : vendor_rate_tabel_serializer.data
            })
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, id = None):
        try:
            vendor_rate_serializer = VendorRateSerializer(data={**request.data, "user_id" : request.user.id})
            if vendor_rate_serializer.is_valid():
                vendor_rate_serializer.save()
                return Response({"message" : "Vendor Rate Serializer"}, status=status.HTTP_200_OK)
            else:
                print(request.data)
                return Response(vendor_rate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            print(request.data)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
