from django.shortcuts import render
from invoice.models import Invoice
from invoice.serializer import InvoiceSerializer
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import make_aware
from rest_framework import status
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from companycustomer.models import CompanyUser
from invoice.models import Invoice

class InvoiceDetailCustomView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id = None):
        try:
            if request.user.company_admin:
                invoice_serializer = InvoiceSerializer(data={ **request.data, "company_id" : request.user.id })
            else:
                invoice_serializer = InvoiceSerializer(data={ **request.data, "company_id" : request.user.parent_user.id })                           
            if invoice_serializer.is_valid():
                invoice_serializer.save()
                return Response({"message" : "Invoice Saved Successfully!!"})
            else:
                return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self, request, id = None):
        try:
            from_date = request.GET.get('invoice_from_date')
            to_date = request.GET.get('invoice_to_date')
            customer_id = request.GET.get("customer_id")
            invoice_type = request.GET.get("invoice_type")
            try:
                from_date = datetime.strptime(f"{from_date}", "%Y-%m-%d").strftime("%Y-%m-%dT23:59:00Z")
                to_date = datetime.strptime(f"{to_date}", "%Y-%m-%d").strftime("%Y-%m-%dT23:59:00Z")
            except (ValueError, TypeError):
                from_date = 'all'
                to_date = 'all'
                # return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
            if from_date or to_date or customer_id:
                invoice_d = Invoice.objects.filter(Q(company_id = request.user.id) | Q(customer_id__user_id = request.user.id))
                if from_date == 'all' and to_date == 'all':
                    invoice = invoice_d.filter(Q(invoice_type = invoice_type) & Q(customer_id=customer_id))
                else:
                    invoice = invoice_d.filter(Q(created_date__range=[from_date, to_date]) &
                        Q(customer_id=customer_id))
                invoice_serializer = InvoiceSerializer(invoice, many=True)
                return Response(invoice_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error" : "Query did not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, id= None):
        try:
            invoice = Invoice.objects.get(Q(id = id) & (Q(company_id = request.user.id) | Q(customer_id__user_id = request.user.id)))
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
                invoice = Invoice.objects.get(Q(id = id) & (Q(company_id = request.user.id) | Q(customer_id__user_id = request.user.id)))
                invoice.active = not invoice.active
                invoice.save()
                return Response({"message" : "Data Updated Successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
