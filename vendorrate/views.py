from django.shortcuts import render
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
from vendorrate.serializer import VendorRateSerializer,VendorRateGetSerializer
from vendorratetabel.models import VendorRateTabel
from vendorratetabel.serializer import VendorRateTabelSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from collections import defaultdict

class VendorRateTableViews(APIView):   
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk is not None:
            data = VendorRate.objects.get(Q(ScheduleID= pk) & Q(user_id = request.user.id))
            serializer = VendorRateSerializer(data)
            return Response(serializer.data)
        else:
            # Customer 
            customer_data = Customer.objects.filter(Q(active = True) & (Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)))
            customer_serialzer = CustomerSerializer(customer_data, many=True)

            # Management Profile
            management_profile = ManagementProfileName.objects.filter(Q(user_id = request.user.id))
            management_profile_serializer = ManagementProfileSerializer(management_profile, many=True)

            # Existing Profile
            customer_rates = VendorRateTabel.objects.filter(user_id = request.user.id)
            customer_rate_serializer = VendorRateTabelSerializer(customer_rates, many=True)

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
            try:
                rate_tabel = VendorRateTabel.objects.get(Q(vendor_rate_name = request.data.get('vendor_rate_name')) & (Q(user_id__parent_user = request.user.parent_user) | Q(user_id__parent_user = request.user.id) | Q(user_id = request.user.parent_user)))            
                if rate_tabel is not None:
                    return Response({"error" : "Rate Name should unique"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                try:
                    customer_prefix = VendorRateTabel.objects.get(Q(vendor_prefix = request.data.get('vendor_prefix')) & (Q(user_id__parent_user = request.user.parent_user) | Q(user_id__parent_user = request.user.id) | Q(user_id = request.user.parent_user)))             
                    if customer_prefix is not None:
                        return Response({"error" : "Customer Prefix should unique"}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    pass
            data = {
                'customer_id': request.data.get('customer_id'),
                'vendor_rate_name': request.data.get('vendor_rate_name'),
                'vendor_prefix': request.data.get('vendor_prefix'),
                'vendor_rate_profile': request.data.get('vendor_rate_profile'),
                'user_id': request.user.id
            }
            customer_rate_serializer = VendorRateTabelSerializer(data={ **data})
            if customer_rate_serializer.is_valid():
                customer_rate_data = customer_rate_serializer.save()
                objs = []
                excel_file = request.data.get("excel_sheet")
                df = pd.read_excel(excel_file)
                for index, row in df.iterrows():
                    if isinstance(row['Unnamed: 0'], str) and isinstance(row['Unnamed: 1'], (int, float)) and isinstance(row['Unnamed: 2'], float) and isinstance(row['Unnamed: 3'], str) and isinstance(row['Unnamed: 4'], datetime.datetime):
                        objs.append(VendorRate(
                            country_name=row['Unnamed: 0'],  # replace with your actual field names and DataFrame column names
                            country_code=row['Unnamed: 1'],
                            rate = row['Unnamed: 2'],
                            rate_status = row['Unnamed: 3'],
                            effective_date = row['Unnamed: 4'],
                            billing_increment_1 = row['Unnamed: 5'].split("+")[0],
                            billing_increment_n = row['Unnamed: 5'].split("+")[1],
                            vendor_rate_id = customer_rate_data,
                            user_id = request.user
                        ))
                VendorRate.objects.bulk_create(objs)
                return Response({"Msg ":"Registration Successfully!!"}, status=status.HTTP_200_OK)
            return Response(customer_rate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Invalid File"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk=None):
        try:
            excel_file = request.data.get("excel_sheet")
            customer_rate_id = VendorRateTabel.objects.get(id = request.data.get("rate"))
            df = pd.read_excel(excel_file)
            objs = []
            

            for index, row in df.iterrows():
                if isinstance(row['Unnamed: 0'], str) and isinstance(row['Unnamed: 1'], (int, float)) and isinstance(row['Unnamed: 2'], float) and isinstance(row['Unnamed: 3'], str) and isinstance(row['Unnamed: 4'], datetime.datetime):
                    try:
                        exis_rate = VendorRate.objects.get(Q(country_code = row['Unnamed: 1']) & Q(user_id = request.user.id))
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
                        objs.append(VendorRate(
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
            VendorRate.objects.bulk_create(objs)
            return Response({"Msg ":"Registration Successfully!!"})
        except VendorRate.DoesNotExist:
            return Response({"error": "EmailSchedule not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"} , status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            email_schedule = VendorRate.objects.get(Q(pk=pk) & Q(user_id = request.user.id))
        except VendorRate.DoesNotExist:
            return Response({"error": "EmailSchedule not found"}, status=status.HTTP_404_NOT_FOUND)
        email_schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  

class VendorRateByCountryCode(APIView):
    def get(self, request, id = None):
        try:
            country_code = request.GET.get("country_codes")
            # Country Code
            rate_tabel = VendorRate.objects.filter(Q(country_name = country_code) & ((Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id))))
            rate_serializer = VendorRateSerializer(rate_tabel, many=True)

            # Distinct Rate
            distinct_rate = VendorRate.objects.filter(
                    (Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)) & Q(vendor_rate_id__customer_id__active=True)
                ).values_list('country_name', flat=True).distinct()
            for i in rate_serializer.data:
                vendor_rate_tabel = VendorRateTabel.objects.get(id = i['vendor_rate_id'])
                i['vendor_rate_id_name'] = vendor_rate_tabel.vendor_rate_name
                i["customer_name"] = vendor_rate_tabel.customer_id.customer_name
            return Response({
                "data" : rate_serializer.data,
                "country_list" : distinct_rate 
                }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error"  : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VendorTargetSheetByCountryCode(APIView):
    def get(self, request, id=None):
        try:
            # country_code = request.GET.get("country_codes")
            country_name = request.GET.get('country_name')
            country_code = request.GET.get('country_code')
            # Country Code
            rate_tabel = VendorRate.objects.filter(
                (Q(country_name=country_name) & Q(country_code = country_code)) & 
                (Q(user_id=request.user.id) | Q(user_id__parent_user=request.user.id))
            )
            rate_serializer = VendorRateGetSerializer(rate_tabel, many=True)

            # Distinct Rate
            distinct_rate = VendorRate.objects.filter(
                Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id) & 
                Q(vendor_rate_id__customer_id__active = True) 
            ).values_list('country_name', 'country_code').distinct()
            
            # Prepare the data for collapsing
            print(len(rate_serializer.data))
            data = rate_serializer.data
            result = []
            for i in data:
                if len(result) != 0:
                    for index, j in enumerate(result):
                        if j['country_code'] == i['country_code']:
                            lcr_keys = [key for key in j.keys() if key.startswith('LCR')]
                            if lcr_keys:
                                next_lcr = max(int(key[3:]) for key in lcr_keys) + 1
                            else:
                                next_lcr = 1
                            j[f"LCR{next_lcr}"] = f'''{i['vendor_rate_id']["customer_id"]['customer_name']} - {i["rate"]}'''
                            break
                        else:
                            if not any(obj.get('country_code') == i["country_code"] for obj in result):
                                result.append({"country_name": i.get('country_name'), "country_code": i.get('country_code'), f"LCR{1}": f'''{i['vendor_rate_id']["customer_id"]['customer_name']} - {i["rate"]}'''})
                else:
                    result.append({"country_name": i['country_name'], "country_code": i['country_code'], f"LCR{1}": f'''{i['vendor_rate_id']["customer_id"]['customer_name']} - {i["rate"]}'''})
                 
            for i in result:
                values_with_LCR = [key for key in i if key.startswith('LCR')]
                suggested_byy = float(i[values_with_LCR[0]].split('-')[1].strip()) - 0.05 * float(i[values_with_LCR[0]].split('-')[1].strip())
                suggested_sell = float(i[values_with_LCR[-1]].split('-')[1].strip()) +  0.10* float(i[values_with_LCR[-1]].split('-')[1].strip())
                i['suggested_buy'] = suggested_byy
                i['suggested_sell'] = suggested_sell
 
            return Response({
                "data": result,
                "country_list": distinct_rate
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VendorRateSearchViewOrUpdate(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        try:
            query_params_dict = {key: value for key, value in request.query_params.items() if key != 'customer_id'}
            rate_tabel = VendorRate.objects.filter((Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)) & Q(country_name = query_params_dict.get('country_code')) & Q(vendor_rate_id = query_params_dict.get('customer_rate_id')))
            rate_serializer = VendorRateSerializer(rate_tabel, many=True)
            return Response(rate_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, id = None):
        try:
            if id is None:
                return Response({"error" : "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                rate = VendorRate.objects.get(Q(id = id) & (Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)))
                rate_serializer = VendorRateSerializer(rate, data=request.data, partial = True)
                if rate_serializer.is_valid():
                    rate_serializer.save()
                    return Response({"message" : "Updated Successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error" : "Some Error Occured"}, status=status.HTTP_400_BAD_REQUEST)   
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            if id is None:
                return Response({"error" : "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                rate = VendorRate.objects.get(Q(id = id) & (Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)))
                rate.delete()
                return Response({"message" : "Updated Successfully"}, status=status.HTTP_200_OK)
        except Exception as e: 
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
