from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from emaillog.models import EmailLog
from emaillog.serializers import EmailLogSerializer
from companycustomer.models import Customer
from emailtemplate.models import EmailTemplate
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.http import JsonResponse
from companycustomer.serializers import CustomerSerializer
from emailtemplate.models import EmailTemplate
from emailtemplate.serializers import EmailTemplateSerializers
from toproutes.models import Route
from emaillog.data_to_html import data_to_styled_html_table, data_to_styled_html_table_react
from rest_framework.permissions import IsAuthenticated
from rate.models import RateTabel
from customer_rate.models import CustomerRateTable
from customer_rate.serializer import CustomerRateSerializer
import pandas as pd
from emaillog.genrateExcel import generate_excel
from django.db.models import Q

class EmailLogView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        try:

            if pk is not None:
                data = EmailLog.objects.get(Q(ScheduleID= pk) & Q(user_id = request.user.id))
                serializer = EmailLogSerializer(data)
                return Response(serializer.data)
            else:
                customer_data = Customer.objects.filter(Q(active = True) & (Q(company_id = request.user.id) | Q(user_id = request.user.id)))
                customer_serializer = CustomerSerializer(customer_data, many=True)

                # Email Templates
                email_template_data = EmailTemplate.objects.filter(Q(company_id = request.user.id) | Q(company_id = request.user.parent_user))
                email_template_serializer = EmailTemplateSerializers(email_template_data, many=True)

                distinct_rate = RateTabel.objects.filter((Q(company_id = request.user.id) | 
                                                    Q(customer_rate_id__customer_id__user_id = request.user.id))).values_list('country_name' , flat=True).distinct()

                distinct_routes = Route.objects.filter((Q(user_id = request.user.id) | Q(company_id = request.user.id))).values_list('top_route_name', flat=True).distinct()
                route_list = list(distinct_routes)

                # Customer Rate Tabel
                customer_rates = CustomerRateTable.objects.filter((Q(company_id = request.user.id) | 
                                                    Q(customer_id__user_id = request.user.id)))
                customer_rate_serializer = CustomerRateSerializer(customer_rates, many=True)
                return Response({
                    "customer_data" : customer_serializer.data ,
                    "email_template" : email_template_serializer.data,
                    "route_list" : route_list,
                    "rate_list" : distinct_rate,
                    "customer_rate" : customer_rate_serializer.data
                }) 
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)    
     
    def post(self, request, pk=None):
        try:
            ############ CONDITION ONE SEND RATE EMAIL ############
            email_type = request.data.get('type')
            if email_type == "rate":
                is_allCountry = request.data.get("is_all_country")
                rate_id = request.data.get('rate_id')
                # Fetch rate data based on user and rate_id
                rate_data = RateTabel.objects.filter(
                    (Q(company_id=request.user.id) | Q(customer_rate_id__customer_id__user_id = request.user.id)) & Q(customer_rate_id=rate_id)
                ).values(
                    'country_name', 
                    'country_code', 
                    'rate',
                    'rate_status',
                    'effective_date',
                    'billing_increment_1', 
                    'billing_increment_n', 
                )                
                # Optionally filter by selected countries if not all countries
                if not is_allCountry or is_allCountry.lower() == 'false':
                    country_list = request.data.get('country').split(",")
                    rate_data = rate_data.filter(country_name__in=country_list)
                
                # Generate Excel attachment
                attachment = generate_excel(rate_data)
                
                # Fetch customer's email address
                customer_id = request.data.get("customer_id")
                customer = Customer.objects.get(Q(user_id=request.user.id) & Q(id=customer_id))
                customer_email = customer.rates_email
                
                # Create EmailMultiAlternatives object
                email = EmailMultiAlternatives(
                    request.data.get('subject'),
                    request.data.get('message'),
                    'simply2cloud@gmail.com',
                    [customer_email]
                )
                
                # Attach generated Excel file if available
                if attachment:
                    email.attach(
                        'rate_data.xlsx',  # File name
                        attachment.getvalue(),  # File content as bytes
                        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # MIME type for Excel
                    )
                
                # Optionally attach HTML content
                if request.data.get('message') and request.data.get('message') != "undefined":
                    email.attach_alternative(request.data.get('message'), "text/html")
                
                # Send the email
                email.send()
                
                return Response({"message": "Email sent successfully"})

            # Can Change in future
            company_id = request.user.id if request.user.company_admin else request.user.parent_user.id
            data = {
            'customer_id': request.data.get('sendTo').split(","),
            'template_id': request.data['template_id'],
            'attachement': request.FILES.get('attachement', None),
            'company_id' : company_id
            }
            serializers = EmailLogSerializer(data = data)   
            rates_emails = list(Customer.objects.filter(Q(id__in=data['customer_id']) & (Q(user_id = request.user.id) | Q(company_id = request.user.id))).values_list('rates_email', flat=True))
            if serializers.is_valid():
                email_log_data = serializers.save()
                try:
                    message = request.data.get("message")
                    attachment = data["attachement"]
                    email = EmailMultiAlternatives(request.data.get('subject'), request.data.get('body'), 'simply2cloud@gmail.com', rates_emails)
                    if message != "undefined":
                        email.attach_alternative(message, "text/html")
                    if attachment:
                        email.attach(attachment.name, attachment.read(), attachment.content_type)
                    email.send()
                    return Response({"message": "Email sent Successfully!"})
                except Exception as e:
                    # print(message)
                    print(f"Email sending failed: {e}")
                return Response({"message": "Email Sent Successfully!"})
            return Response(serializers.errors, status=400)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            email_schedule = EmailLog.objects.get(Q(pk=pk) & Q(user_id = request.user.id))
        except EmailLog.DoesNotExist:
            return Response({"error": "EmailLog not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmailLogSerializer(email_schedule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Msg": "EmailLog updated successfully!!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            email_schedule = EmailLog.objects.get(Q(pk=pk) & Q(user_id = request.user.id))
        except EmailLog.DoesNotExist:
            return Response({"error": "EmailLog not found"}, status=status.HTTP_404_NOT_FOUND)

        email_schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)