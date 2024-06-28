from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rate.models import RateTabel
from rate.serializer import RateTableSerializers
from companycustomer.models import Customer
from companycustomer.serializers import CustomerSerializer
from management_profile.models import ManagementProfileName
from management_profile.serializers import ManagementProfileSerializer
from customer_rate.models import CustomerRateTable
from customer_rate.serializer import CustomerRateSerializer
import pandas as pd
import datetime
from toproutes.models import Route
from django.db import connection, transaction
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class RateTableViews(APIView):   
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk is not None:
            data = RateTabel.objects.get(Q(ScheduleID= pk) & Q(user_id = request.user.id))
            serializer = RateTableSerializers(data)
            return Response(serializer.data)
        else:
            # Customer 
            customer_data = Customer.objects.filter(Q(active = True) & (Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)))
            customer_serialzer = CustomerSerializer(customer_data, many=True)

            # Management Profile
            management_profile = ManagementProfileName.objects.filter((Q(user_id = request.user.id) | Q(user_id = request.user.parent_user)))
            management_profile_serializer = ManagementProfileSerializer(management_profile, many=True)

            # Existing Profile
            customer_rates = CustomerRateTable.objects.filter((Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)))
            customer_rate_serializer = CustomerRateSerializer(customer_rates, many=True)

            # # existing top-route ids 
            return Response({
                "customer_data" : customer_serialzer.data,
                "management_profile" : management_profile_serializer.data,
                "customer_rate" : customer_rate_serializer.data
             }, status=status.HTTP_200_OK)
    
    def post(self, request, pk=None):
        try:
            if pk is not None:
                return Response({"Err": "Post Method Not allowed"})
            radio_value = request.data.get("radio_value")
            try:
                rate_tabel = CustomerRateTable.objects.get(Q(rate_name = request.data.get('rate_name')) & (Q(user_id__parent_user = request.user.parent_user) | Q(user_id__parent_user = request.user.id) | Q(user_id = request.user.parent_user)))            
                if rate_tabel is not None:
                    return Response({"error" : "Rate Name should unique"}, status=status.HTTP_400_BAD_REQUEST)
                print(request.data.get('customer_prefix'))
            except Exception as e:
                try:
                    customer_prefix = CustomerRateTable.objects.get(Q(customer_prefix = request.data.get('customer_prefix')) & (Q(user_id__parent_user = request.user.parent_user) | Q(user_id__parent_user = request.user.id) | Q(user_id = request.user.parent_user)))             
                    if customer_prefix is not None:
                        return Response({"error" : "Customer Prefix should unique"}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    pass
            data = {
                'customer_id': request.data.get('customer_id'),
                'rate_status': request.data.get('rate_status'),
                'rate_name': request.data.get('rate_name'),
                'customer_prefix': request.data.get('customer_prefix'),
                'rate_profile': request.data.get('rate_profile'),
                'user_id': request.user.id
            }
            customer_rate_serializer = CustomerRateSerializer(data={ **data})
            if customer_rate_serializer.is_valid():
                customer_rate_data = customer_rate_serializer.save()
                objs = []
                if radio_value == 1 or radio_value == "1":
                    excel_file = request.data.get("excel_sheet")
                    df = pd.read_excel(excel_file)
                    for index, row in df.iterrows():
                        if isinstance(row['Unnamed: 0'], str) and isinstance(row['Unnamed: 1'], (int, float)) and isinstance(row['Unnamed: 2'], float) and isinstance(row['Unnamed: 3'], str) and isinstance(row['Unnamed: 4'], datetime.datetime):
                            objs.append(RateTabel(
                                country_name=row['Unnamed: 0'],  # replace with your actual field names and DataFrame column names
                                country_code=row['Unnamed: 1'],
                                rate = row['Unnamed: 2'],
                                rate_status = row['Unnamed: 3'],
                                effective_date = row['Unnamed: 4'],
                                billing_increment_1 = row['Unnamed: 5'].split("+")[0],
                                billing_increment_n = row['Unnamed: 5'].split("+")[1],
                                customer_rate_id = customer_rate_data,
                                user_id = request.user
                            ))
                    RateTabel.objects.bulk_create(objs)
                    return Response({"Msg ":"Registration Successfully!!"}, status=status.HTTP_200_OK)
                elif radio_value == 2 or radio_value == "2":
                    customer_rate_id = request.data.get('customer_rate_id')

                    if customer_rate_id is None:
                        return Response({"error" : "Please Select Customer Rate Id"}, status=status.HTTP_400_BAD_REQUEST)
                    existing_rates = RateTabel.objects.filter(Q(customer_rate_id = customer_rate_id) & Q(user_id = request.user.id))
                    for rate in existing_rates:
                        objs.append(RateTabel(
                            country_name = rate.country_name,
                            country_code = rate.country_code,
                            rate = rate.rate,
                            rate_status = rate.rate_status,
                            effective_date = rate.effective_date,
                            billing_increment_1 = rate.billing_increment_1,
                            billing_increment_n = rate.billing_increment_n,
                            customer_rate_id = customer_rate_data,
                            user_id = request.user.id
                        ))
                    RateTabel.objects.bulk_create(objs)
                    return Response({"message" : "Data Created Successfully"})
                    # # Return a success response
                return Response({"error ":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(customer_rate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : f"{e}"} , status= status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        try:
            excel_file = request.data.get("excel_sheet")
            customer_rate_id = CustomerRateTable.objects.get(id = request.data.get("rate"))
            df = pd.read_excel(excel_file)
            objs = []
            

            for index, row in df.iterrows():
                if isinstance(row['Unnamed: 0'], str) and isinstance(row['Unnamed: 1'], (int, float)) and isinstance(row['Unnamed: 2'], float) and isinstance(row['Unnamed: 3'], str) and isinstance(row['Unnamed: 4'], datetime.datetime):
                    try:
                        exis_rate = RateTabel.objects.get(Q(country_code = row['Unnamed: 1']) & Q(user_id = request.user.id))
                        if exis_rate:
                            exis_rate.country_name = row['Unnamed: 0']
                            exis_rate.country_code = row['Unnamed: 1']
                            exis_rate.rate = row['Unnamed: 2']
                            exis_rate.rate_status = row['Unnamed: 3']
                            exis_rate.effective_date = row['Unnamed: 4']
                            exis_rate.billing_increment_1 = row['Unnamed: 5'].split("+")[0]
                            exis_rate.billing_increment_n = row['Unnamed: 5'].split("+")[1]
                            exis_rate.customer_rate_id = customer_rate_id
                            exis_rate.save()
                    except Exception as e:    
                        objs.append(RateTabel(
                            country_name=row['Unnamed: 0'],  # replace with your actual field names and DataFrame column names
                            country_code=row['Unnamed: 1'],
                            rate = row['Unnamed: 2'],
                            rate_status = row['Unnamed: 3'],
                            effective_date = row['Unnamed: 4'],
                            billing_increment_1 = row['Unnamed: 5'].split("+")[0],
                            billing_increment_n = row['Unnamed: 5'].split("+")[1],
                            customer_rate_id = customer_rate_id,
                            user_id = request.user
                        ));    
            RateTabel.objects.bulk_create(objs)
            return Response({"Msg ":"Registration Successfully!!"})
        except RateTabel.DoesNotExist:
            return Response({"error": "EmailSchedule not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"} , status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            email_schedule = RateTabel.objects.get(Q(pk=pk) & Q(user_id = request.user.id))
        except RateTabel.DoesNotExist:
            return Response({"error": "EmailSchedule not found"}, status=status.HTTP_404_NOT_FOUND)
        email_schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  


class RateSearchViewOrUpdate(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        try:
            query_params_dict = {key: value for key, value in request.query_params.items() if key != 'customer_id'}
            rate_tabel = RateTabel.objects.filter(Q(user_id = request.user.id) & Q(country_name = query_params_dict.get('country_code')) & Q(customer_rate_id = query_params_dict.get('customer_rate_id')))
            rate_serializer = RateTableSerializers(rate_tabel, many=True)
            return Response(rate_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id = None):
        try:
            if id is None:
                return Response({"error" : "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                rate = RateTabel.objects.get(Q(id = id) & Q(user_id = request.user.id))
                rate_serializer = RateTableSerializers(rate, data=request.data, partial = True)
                if rate_serializer.is_valid():
                    rate_serializer.save()
                    return Response({"message" : "Updated Successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error" : "Some Error Occured"}, status=status.HTTP_400_BAD_REQUEST)   
        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            if id is None:
                return Response({"error" : "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                rate = RateTabel.objects.get(Q(id = id) & Q(user_id = request.user.id))
                rate.delete()
                return Response({"message" : "Updated Successfully"}, status=status.HTTP_200_OK)
        except Exception as e: 
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
