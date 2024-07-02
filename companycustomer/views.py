from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from companycustomer.models import Customer
from companycustomer.serializers import CustomerSerializer
from django.db.models import Q
from toproutes.models import Route
from rate.models import RateTabel
from customer_rate.models import CustomerRateTable
from customer_rate.serializer import CustomerRateSerializer 
from invoice.models import Invoice
from invoice.serializer import InvoiceSerializer
from django.db.models import Sum
from dispute.models import Dispute
from dispute.serializer import DisputeSerialzer
from payments.models import Payment
from vendorrate.models import VendorRate
from vendorratetabel.models import VendorRateTabel
from vendorratetabel.serializer import VendorRateTabelSerializer
from companycustomer.models import CompanyUser

class CustomerViews(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        try:
            if pk is not None:
                data = Customer.objects.get(Q(ScheduleID= pk) & Q(active = True) & (Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)))
                serializer = CustomerSerializer(data)
                return Response(serializer.data)
            else:
                data = Customer.objects.filter((Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)))

                serializer = CustomerSerializer(data, many=True)
                for i in serializer.data:
                    i["added_by"] = CompanyUser.objects.get(id = i['user_id']).user_name
                return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request, pk=None):
        if pk is not None:
            return Response({"Err": "Post Method Not allowed"})
        serializer = CustomerSerializer(data={**request.data, "user_id" : request.user.id})
        if serializer.is_valid():
            # Save data to the database
            data = serializer.save()
            # Return a success response
            return Response({"Msg ":"Registration successfully!!"})
        return Response(serializer.errors, status=400)
    
    def put(self, request, pk):
        try:
            customer = Customer.objects.get(Q(id=pk) & Q(active = True) & (Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)))
            serializer = CustomerSerializer(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"Msg": "Customer updated successfully!!"})
        except Customer.DoesNotExist:
            return Response({"error": "EmailSchedule not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            customer = Customer.objects.get(Q(id=pk) & (Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)))
            if customer.active == True:
                customer.active = False
            else:
                customer.active = True
            customer.save()
            return Response({"message" : "Customer Deleted Successfully"}, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"error": "EmailSchedule not found"}, status=status.HTTP_404_NOT_FOUND)


class SearchPageApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        try:
            search_page = request.query_params.get("page")
            if search_page is None:
                return Response({"error" : "Please give serach Page"}, status=status.HTTP_400_BAD_REQUEST)
            if search_page == "rate_page":
                
                # Customer Data
                customer = Customer.objects.filter((Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)) & Q(active = True))
                customer_serializer = CustomerSerializer(customer, many=True)

                # Customer Rate Data
                customer_rate_data = CustomerRateTable.objects.filter((Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)))
                customer_rate_serializer = CustomerRateSerializer(customer_rate_data, many=True)
 
                return Response({
                    "customer" : customer_serializer.data,
                    "customer_rate" : customer_rate_serializer.data,
                    "page" : search_page
                    # "data" : distinct_routes 
                    }, status=status.HTTP_200_OK)
            
            elif search_page == "top_route":
                print(request.user)
                distinct_routes = Route.objects.filter((Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id))).values_list('top_route_name' , flat=True).distinct()
                return Response({
                    "page" : search_page,
                    "data" : distinct_routes
                }, status=status.HTTP_200_OK)
            

            elif search_page == "vendor_rate_page":                
                # Customer Details
                customer = Customer.objects.filter((Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)) & Q(active = True))
                customer_serializer = CustomerSerializer(customer, many=True)

                # Customer Rate Data
                customer_rate_data = VendorRateTabel.objects.filter((Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)))
                customer_rate_serializer = VendorRateTabelSerializer(customer_rate_data, many=True)

                return Response({
                    "customer" : customer_serializer.data,
                    "customer_rate" : customer_rate_serializer.data,
                    "page" : search_page
                    # "data" : distinct_routes 
                    }, status=status.HTTP_200_OK)
            elif search_page == "all_country":
                distinct_rate = VendorRate.objects.filter((Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)) & Q(vendor_rate_id__customer_id__active=True)).values_list('country_name' , flat=True).distinct()
                return Response({"country" : distinct_rate,
                "page" : search_page}, status=status.HTTP_200_OK)
            elif search_page == "get_country":
                if id is None:
                    return Response({"error" : "Please give Rate ID Page"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    distinct_rate = []
                    if request.GET.get('url') == '/search-vendor-rate':
                        print()
                        distinct_rate = VendorRate.objects.filter(Q(vendor_rate_id = id) & (Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id))).values_list('country_name' , flat=True).distinct()
                    else:
                        distinct_rate = RateTabel.objects.filter(Q(customer_rate_id = id) & (Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id))).values_list('country_name' , flat=True).distinct()
                    return Response({"country" : distinct_rate}, status = status.HTTP_200_OK)
            elif search_page == "country_code":
                country_name = request.GET.get('country')
                distinct_code = VendorRate.objects.filter(Q(country_name = country_name) & (Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id))).values_list('country_code' , flat=True).distinct()
                return Response({"country_code" : distinct_code}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error" : "internal Server Error"}, status=status.HTTP_400_BAD_REQUEST)
        

class CustomerStatmentOfAmount(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        try:
            customer = Customer.objects.filter(Q(active = True) & (Q(user_id = request.user.id) | Q(user_id__parent_user = request.user.id)))
            customer_serializer = CustomerSerializer(customer, many=True)
            for i in customer_serializer.data:

                # INVOICE Details
                invoice = Invoice.objects.filter(customer_id = i["id"])
                i['invoice_amount_in'] = invoice.filter(invoice_type = "IN").aggregate(total=Sum('invoice_amount'))['total'] or 0
                i['invoice_amount_out'] = invoice.filter(invoice_type = "OUT").aggregate(total=Sum('invoice_amount'))['total'] or 0

                # DISPUTE DETAILS
                dispute = Dispute.objects.filter(customer_id = i["id"])
                i['dispute_amount_in'] = dispute.filter(dispute_type = "IN").aggregate(total = Sum('dispute_amount'))['total'] or 0
                i['dispute_amount_out'] = dispute.filter(dispute_type = "OUT").aggregate(total = Sum('dispute_amount'))['total'] or 0

                # PAYMENT DETAILS
                payment = Payment.objects.filter(customer_id = i['id'])
                i['payment_in'] =  payment.filter(payment_type = "IN").aggregate(total = Sum('payment_amount'))['total'] or 0
                i['payment_out'] =  payment.filter(payment_type = "OUT").aggregate(total = Sum('payment_amount'))['total'] or 0
                
                i['bank_charges_in'] = payment.filter(payment_type = "IN").aggregate(total = Sum('bank_charges'))['total'] or 0
                i['bank_charges_out'] = payment.filter(payment_type = "OUT").aggregate(total = Sum('bank_charges'))['total'] or 0

                i['total_sum'] = i['invoice_amount_out'] - i['invoice_amount_in'] - \
                                    i['dispute_amount_in'] + \
                                    i['dispute_amount_out'] - \
                                    i['payment_in']  + i['payment_out'] + \
                                    i['bank_charges_in'] - \
                                    i['bank_charges_out']   
            return Response(customer_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)