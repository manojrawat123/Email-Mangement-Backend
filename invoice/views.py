from django.shortcuts import render
from rest_framework import viewsets
from .models import Invoice
from rest_framework import generics
from invoice.serializer import InvoiceSerializer
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceDetailCustomView(APIView):
    def get(self, request, id = None):
        from_date = request.GET.get('invoice_from_date')
        to_date = request.GET.get('invoice_to_date')
        customer_id = request.GET.get("customer_id")
        try:
            from_date = datetime.strptime(f"{from_date}", "%Y-%m-%d").strftime("%Y-%m-%dT23:59:00Z")
            to_date = datetime.strptime(f"{to_date}", "%Y-%m-%d").strftime("%Y-%m-%dT23:59:00Z")
        except (ValueError, TypeError):
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
        if from_date or to_date or customer_id:
            invoice = Invoice.objects.filter(created_date__range=[from_date, to_date],
                customer_id=customer_id)
            invoice_serializer = InvoiceSerializer(invoice, many=True)
            return Response(invoice_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error" : "Query did not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, id= None):
        try:
            invoice = Invoice.objects.get(id = id)
            invoice_serializer = InvoiceSerializer(invoice, data=request.data, partial =True)
            if invoice_serializer.is_valid():
                invoice_serializer.save()
                return Response({"message" : "Data Updated Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request, id =None):
        try:
            if id is None:
                return Response({"error" : "Method Not Allowed"}, status = status.HTTP_400_BAD_REQUEST)
            else:
                invoice = Invoice.objects.get(id = id)
                invoice.active = not invoice.active
                invoice.save()
                return Response({"message" : "Data Updated Successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
