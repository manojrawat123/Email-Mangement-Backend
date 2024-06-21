from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from emaillog.models import EmailLog
from emaillog.serializers import EmailLogSerializer
from customer.models import Customer
from emailtemplate.models import EmailTemplate
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.http import JsonResponse
from customer.serializers import CustomerSerializer
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

class EmailLogView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk is not None:
            data = EmailLog.objects.get(ScheduleID= pk)
            serializer = EmailLogSerializer(data)
            return Response(serializer.data)
        else:
            customer_data = Customer.objects.filter(active = True)
            customer_serializer = CustomerSerializer(customer_data, many=True)

            # Email Templates
            email_template_data = EmailTemplate.objects.all()
            email_template_serializer = EmailTemplateSerializers(email_template_data, many=True)

            distinct_rate = RateTabel.objects.values_list('country_name' , flat=True).distinct()
            distinct_routes = Route.objects.values_list('top_route_name', flat=True).distinct()

            route_list = list(distinct_routes)

            # Customer Rate Tabel
            customer_rates = CustomerRateTable.objects.all()
            customer_rate_serializer = CustomerRateSerializer(customer_rates, many=True)

            return Response({
                "customer_data" : customer_serializer.data ,
                "email_template" : email_template_serializer.data,
                "route_list" : route_list,
                "rate_list" : distinct_rate,
                "customer_rate" : customer_rate_serializer.data
            }) 
        

        
    def post(self, request, pk=None):
        try:

            ########## CONDITION ONE SEND RATE EMAIL ############
            email_type = request.data.get('type')
            if email_type == "rate":
                is_allCountry = request.data.get("is_all_country")
                rate_data = RateTabel.objects.filter(customer_rate_id = request.data.get('rate_id')).values(
                'country_name', 
                'country_code', 
                'rate',
                'rate_status',
                'effective_date',
                'billing_increment_1', 
                'billing_increment_n', 
            )
                if is_allCountry != True or is_allCountry != 'true':
                    country_list = request.data.get('country').split(",")
                    rate_data = rate_data.filter(country_name__in = country_list)                
                attachment = generate_excel(rate_data)
                customer_email = Customer.objects.get(id = request.data.get("customer_id")).rates_email
                email = EmailMultiAlternatives(request.data.get('subject'), request.data.get('message'), 'simply2cloud@gmail.com', [customer_email])
                if attachment:
                    email.attach('rate_data.xlsx', attachment.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                if request.data.get('message') != "undefined":
                    email.attach_alternative(request.data.get('message'), "text/html")  # Set the content type to HTML
                email.send()
                return Response({"message" : "Email Send Successfully!!"})


            # Can Change in future
            data = {
            'customer_id': request.data.get('sendTo').split(","),
            'template_id': request.data['template_id'],
            'attachement': request.FILES.get('attachement', None)
            }
            serializers = EmailLogSerializer(data = data)   
            rates_emails = list(Customer.objects.filter(id__in=data['customer_id']).values_list('rates_email', flat=True))
            if serializers.is_valid():
                email_log_data = serializers.save()
                try:
                    message = request.data.get("message")
                    # # Email Sending Logic 
                    attachment = data["attachement"]
                    print(message)
                    email = EmailMultiAlternatives(request.data.get('subject'), request.data.get('body'), 'simply2cloud@gmail.com', rates_emails)
                    if message != "undefined":
                        email.attach_alternative(message, "text/html")  # Set the content type to HTML
                    if attachment:
                        email.attach(attachment.name, attachment.read(), attachment.content_type)
                    email.send()
                    return Response({"message": "Registration and Email send Successfully!"})
                except Exception as e:
                    print(rates_emails)
                    # print(message)
                    print(f"Email sending failed: {e}")
                return Response({"message": "Email Sent Successfully!"})
            return Response(serializers.errors, status=400)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            email_schedule = EmailLog.objects.get(pk=pk)
        except EmailLog.DoesNotExist:
            return Response({"error": "EmailLog not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmailLogSerializer(email_schedule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Msg": "EmailLog updated successfully!!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            email_schedule = EmailLog.objects.get(pk=pk)
        except EmailLog.DoesNotExist:
            return Response({"error": "EmailLog not found"}, status=status.HTTP_404_NOT_FOUND)

        email_schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# class EmailLogEmailAttachmentViews(APIView):
#     def post(self, request, pk=None):
#         if pk is not None:
#             return Response({"Err": "Post Method Not allowed"})
#         serializer = EmailLogSerializer(data=request.data)
        
#         if serializer.is_valid():
#             # Save data to the database
#             data = serializer.save()                                                                
#             try:
#                 email_lis = []
#                 schedul_customer = serializer.data.get('CustomerId')
#                 for i in schedul_customer:
#                     cemail = Customer.objects.get(id = i)
#                     email_lis.append(cemail.RatesEmail)
#                 print("Email List",email_lis)
#                 message_id = serializer.data.get('TemplateID')
#                 email_template = EmailTemplate.objects.get(TemplateID = message_id)
#                 my_message = email_template.TemplateMessage
#                 my_body = email_template.TemplateBody
#                 # Email sending logic
#                 email_from = settings.EMAIL_HOST_USER
#                 email = "positive.mind.123456789@gmail.com"
#                 recipient_list = email_lis
#                 subject = my_message
#                 message = f'''{my_body}'''

#                 send_mail(subject, message, email_from, recipient_list)

#                 # Return a success response
#                 return Response({"Msg ":"Registration and email send successfully"})
            
#             except Exception as e:
#                 # Handle exceptions related to email sending here
#                 # You can log the error for debugging purposes
#                 print(f"Email sending failed: {e}")
#             # Return a success response
#             return Response({"Msg ":"Registration successfully!!"})
#         return Response(serializer.errors, status=400)
    
