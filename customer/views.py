from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from customer.models import Customer
from customer.serializers import CustomerSerializer
from django.db.models import Q
from toproutes.models import Route
from rate.models import RateTabel
from customer_rate.models import CustomerRateTable
from customer_rate.serializer import CustomerRateSerializer 


class CustomerViews(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk is not None:
            data = Customer.objects.get(Q(ScheduleID= pk) & Q(active = True))
            serializer = CustomerSerializer(data)
            return Response(serializer.data)
        else:
            data = Customer.objects.all()
            serializer = CustomerSerializer(data, many=True)
            return Response(serializer.data)
    
    def post(self, request, pk=None):
        if pk is not None:
            return Response({"Err": "Post Method Not allowed"})
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            # Save data to the database
            data = serializer.save()
            # Return a success response
            return Response({"Msg ":"Registration successfully!!"})
        return Response(serializer.errors, status=400)
    
    def put(self, request, pk):
        try:
            customer = Customer.objects.get(Q(id=pk) & Q(active = True))
            serializer = CustomerSerializer(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"Msg": "Customer updated successfully!!"})
        except Customer.DoesNotExist:
            return Response({"error": "EmailSchedule not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            customer = Customer.objects.get(Q(id=pk))
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
                # distinct_routes = Route.objects.all()

                # Customer Data
                customer = Customer.objects.filter(active = True)
                customer_serializer = CustomerSerializer(customer, many=True)

                # Customer Rate Data
                customer_rate_data = CustomerRateTable.objects.all()
                customer_rate_serializer = CustomerRateSerializer(customer_rate_data, many=True)

                return Response({
                    "customer" : customer_serializer.data,
                    "customer_rate" : customer_rate_serializer.data,
                    "page" : search_page
                    # "data" : distinct_routes 
                    }, status=status.HTTP_200_OK)
            
            elif search_page == "top_route":
                distinct_routes = Route.objects.values_list('top_route_name' , flat=True).distinct()
                return Response({
                    "page" : search_page,
                    "data" : distinct_routes
                }, status=status.HTTP_200_OK)
            elif search_page == "get_country":
                if id is None:
                    return Response({"error" : "Please give Rate ID Page"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    distinct_rate = RateTabel.objects.filter(customer_rate_id = id).values_list('country_name' , flat=True).distinct()
                    return Response({"country" : distinct_rate}, status = status.HTTP_200_OK)



        except Exception as e:
            return Response({"error" : "internal Server Error"}, status=status.HTTP_400_BAD_REQUEST)