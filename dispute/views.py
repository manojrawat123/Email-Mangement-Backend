from django.shortcuts import render
from rest_framework import viewsets
from .models import Invoice
from rest_framework import generics
from invoice.serializer import InvoiceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from invoice.models import Invoice
from django.utils import timezone
from datetime import timedelta
from invoice.serializer import InvoiceSerializer
from companycustomer.serializers import CustomerSerializer
from companycustomer.models import Customer
from dispute.serializer import DisputeSerialzer
from datetime import datetime, timedelta
from dispute.models import Dispute
from dispute.serializer import DisputeSerialzer
from django.db.models import Q,Subquery
from rest_framework.permissions import IsAuthenticated

class DisputeDetailsViews(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        try:
            page =  request.GET.get('page')
            if page in ['true', True, "True"]:
                # Get Customers
                customer = Customer.objects.filter(Q(active = True) & (Q(company_id = request.user.id) | Q(user_id = request.user.id)))
                customer_serializer = CustomerSerializer(customer, many=True)

                # Select Invoices
                two_months_ago = timezone.now() - timedelta(days=60)
                disputed_invoices = Dispute.objects.filter(active=True).values('invoice_number')
                invoice = Invoice.objects.filter(Q(created_date__gte=two_months_ago) & (Q(company_id = request.user.id) | Q(customer_id__user_id = request.user.id))).exclude(
            Q(id__in=Subquery(disputed_invoices))
        ).order_by('-created_date')

                invoice_serializer = InvoiceSerializer(invoice, many=True)
                return Response({
                    "customer" : customer_serializer.data,
                    "invoice" : invoice_serializer.data
                }, status=status.HTTP_200_OK)
            else:
                from_date = request.GET.get('dispute_from_date')
                to_date = request.GET.get('dispute_to_date')
                customer_id = request.GET.get("customer_id")
                dispute_type = request.GET.get("dispute_type")
                try:
                    from_date = datetime.strptime(f"{from_date}", "%Y-%m-%d").strftime("%Y-%m-%dT23:59:00Z")
                    to_date = datetime.strptime(f"{to_date}", "%Y-%m-%d").strftime("%Y-%m-%dT23:59:00Z")
                except Exception as e:
                    dispute = Dispute.objects.filter(Q(dispute_type = dispute_type) &
                        Q(customer_id=customer_id) & (Q(company_id = request.user.id) | Q(customer_id__user_id = request.user.id))
                )
                    dispute_serializer = DisputeSerialzer(dispute, many=True)
                    return Response(dispute_serializer.data, status = status.HTTP_200_OK)            
                if from_date or to_date or customer_id:
                    dispute = Dispute.objects.filter(Q(created_date__range=[from_date, to_date]) & 
                        Q(customer_id=customer_id) & (Q(company_id = request.user.id) | Q(customer_id__user_id = request.user.id)))
                    dispute_serializer = DisputeSerialzer(dispute, many=True)
                    return Response(dispute_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"error" : "Query did not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, id =None):
        try:
            if request.user.company_admin:
                dispute_serializer = DisputeSerialzer(data={**request.data, "company_id" : request.user.id})
            else:
                dispute_serializer = DisputeSerialzer(data={**request.data, "company_id" : request.user.parent_user.id})
            if dispute_serializer.is_valid():
                dispute_serializer.save()
                return Response({"message" : "Data Saved Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(dispute_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, id= None):
        try:
            dispute = Dispute.objects.get(Q(id = id) & (Q(company_id = request.user.id) | Q(customer_id__user_id = request.user.id)))
            dispute_serializer = DisputeSerialzer(dispute, data=request.data, partial =True)
            if dispute_serializer.is_valid():
                dispute_serializer.save()
                return Response({"message" : "Data Updated Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(dispute_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request, id =None):
        try:
            if id is None:
                return Response({"error" : "Method Not Allowed"}, status = status.HTTP_400_BAD_REQUEST)
            else:
                dispute = Dispute.objects.get(Q(id = id) & (Q(company_id = request.user.id) | Q(customer_id__user_id = request.user.id)))
                dispute.active = not dispute.active
                dispute.save()
                return Response({"message" : "Data Updated Successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)