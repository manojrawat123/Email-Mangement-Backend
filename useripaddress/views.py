from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from useripaddress.serializer import UserIpAddressSerializer
from useripaddress.models import IpAdderessCompanyCustomer
from django.db.models import Q
from companycustomer.models import Customer

#######  Create your views here.  ##########

class AddUserIpAddress(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id = None):
        try:
            ip = request.GET.get('ip_address')
            user_ip_address = IpAdderessCompanyCustomer.objects.filter(Q(ip_address = ip) & ( Q(company_id = request.user.id) | Q(customer_id__user_id = request.user.id)))
            user_ip_address_serializer = UserIpAddressSerializer(user_ip_address, many=True)
            for i in user_ip_address_serializer.data:
                i["customer_name"] = Customer.objects.get(id = i["customer_id"]).customer_name
                i['added_date'] = i["added_date"][:10]
            return Response(user_ip_address_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, id = None):
        try:
            company_id = request.user.id if request.user.company_admin else request.user.parent_user.id
            user_id_address_serializer = UserIpAddressSerializer(data={**request.data, "company_id" : company_id})
            if user_id_address_serializer.is_valid():
                user_id_address_serializer.save()
                return Response({"message" : "Ip Address Saved Successfully!!"}, status=status.HTTP_200_OK)
            else:
                return Response(user_id_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, id = None):
        try:
            if id is None:
                return Response({"error" : "Not Allowed"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_ip_address = IpAdderessCompanyCustomer.objects.get(Q(id=id) & (Q(company_id = request.user.id) | Q(customer_id__user_id = request.user.id)))
                user_ip_address_serializer = UserIpAddressSerializer(user_ip_address, data=request.data, partial = True)
                if user_ip_address_serializer.is_valid():
                    user_ip_address_serializer.save()
                    return Response({"message" : "Ip Address Updated Successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response(user_ip_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "User Not Found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, id = None):
        try:
            if id is None:
                return Response({"error" : "Not Allowed"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_ip_address = IpAdderessCompanyCustomer.objects.get(Q(id=id) & (Q(company_id = request.user.id) | Q(customer_id__user_id = request.user.id)))
                user_ip_address.active = False
                user_ip_address.save()    
                return Response({"message" : "Ip Address Saved Successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "User Not Found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

