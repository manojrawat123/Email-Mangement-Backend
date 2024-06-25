from django.shortcuts import render
from payments.serializers import PaymentSerializers
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import make_aware
from rest_framework import status
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from payments.models import Payment
from django.db.models import Q

# Create your views here.

class PaymentView(APIView):
    def post(self,request, id =None):
        try:
            payment_serializer = PaymentSerializers(data={**request.data, "user_id" : request.user.id })
            if payment_serializer.is_valid():
                payment_serializer.save()
                return Response({"message" : "Payment Saved Successfully!!"}, status=status.HTTP_200_OK)
            else:

                return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def get(self, request, id = None):
        from_date = request.GET.get('payment_from_date')
        to_date = request.GET.get('payment_to_date')
        customer_id = request.GET.get("customer_id")
        try:
            from_date = datetime.strptime(f"{from_date}", "%Y-%m-%d").strftime("%Y-%m-%dT23:59:00Z")
            to_date = datetime.strptime(f"{to_date}", "%Y-%m-%d").strftime("%Y-%m-%dT23:59:00Z")
        except (ValueError, TypeError):
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
        if from_date or to_date or customer_id:
            payment = Payment.objects.filter(Q(created_date__range=[from_date, to_date]) & Q(customer_id=customer_id) & Q(user_id = request.user.id))
            payment_serializer = PaymentSerializers(payment, many=True)
            return Response(payment_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error" : "Query did not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, id= None):
        try:
            payment = Payment.objects.get(Q(id = id) & Q(user_id = request.user.id))
            payment_serializer = PaymentSerializers(payment, data=request.data, partial =True)
            if payment_serializer.is_valid():
                payment_serializer.save()
                return Response({"message" : "Data Updated Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request, id =None):
        try:
            if id is None:
                return Response({"error" : "Method Not Allowed"}, status = status.HTTP_400_BAD_REQUEST)
            else:
                payment = Payment.objects.get(Q(id = id) & Q(user_id = request.user.id))
                payment.active = not payment.active
                payment.save()
                return Response({"message" : "Data Updated Successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
