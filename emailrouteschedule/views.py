from django.shortcuts import render
from emailrouteschedule.models import EmailRouteSchedule
from emailrouteschedule.serializers import EmailSheduleSerializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import datetime
from django.conf import settings
from django.core.mail import send_mail
from companycustomer.models import Customer
from emailtemplate.models import EmailTemplate
from toproutes.models import Route
from emaillog.data_to_html import data_to_styled_html_table, data_to_styled_html_table_rate
from django.core.mail import send_mail, EmailMultiAlternatives
from emailrouteschedule.models import EmailRouteSchedule
from django.db.models import Q

class EmailSheduleViews(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        if pk is not None:
            data = EmailRouteSchedule.objects.get(Q(ScheduleID= pk) & Q(user_id = request.user.id))
            serializer = EmailSheduleSerializers(data)
            return Response(serializer.data)
        else:
            data = EmailRouteSchedule.objects.filter(Q(user_id = request.user.id))
            serializer = EmailSheduleSerializers(data, many=True)
            return Response(serializer.data)
    
    def post(self, request, pk=None):
        if pk is not None:
            return Response({"error": "Post Method Not allowed"})
        company_id = request.user.id if request.user.company_admin else request.user.parent_user.id
        serializer = EmailSheduleSerializers(data={ **request.data, "company_id" : company_id })
        if serializer.is_valid():
            # Save data to the database
            data = serializer.save()
            # Return a success response
            return Response({"message ":"Registration successfully!!"})
        return Response(serializer.errors, status=400)
    
    def put(self, request, pk):
        try:
            email_schedule = EmailRouteSchedule.objects.get(Q(pk=pk) & Q(user_id = request.user.id))
        except EmailRouteSchedule.DoesNotExist:
            return Response({"error": "EmailSchedule not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmailSheduleSerializers(email_schedule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "EmailSchedule updated successfully!!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            email_schedule = EmailRouteSchedule.objects.get(Q(pk=pk) & Q(user_id = request.user.id))
        except EmailRouteSchedule.DoesNotExist:
            return Response({"error": "EmailSchedule not found"}, status=status.HTTP_404_NOT_FOUND)
        email_schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   


class SendScheduleEmail(APIView):
    def post(self, request, id =None):
        try:
            data = request.data
            email_list = list(Customer.objects.filter(Q(user_id = request.user.id) & Q(id__in=data['schedule_customer'])).values_list('rates_email', flat=True))
            top_route_name = Route.objects.filter(Q(top_route_name = data.schedule_route_id) & Q(user_id = request.user.id))
            template = EmailTemplate.objects.get(Q(TemplateID = data.get('schedule_template')) & Q(user_id = request.user.id))
            if len(top_route_name) == 0:
                return Response({"error" : "No data for selected top route"}, status=status.HTTP_400_BAD_REQUEST)
            email_data = [
                    {
                        "id" : route.id,
                        "destination": route.destination,
                        "top_route_name": route.top_route_name,
                        "profile": route.profile,
                        "rate": f"{route.rate:.4f}",  
                        "asr": route.asr,
                        "acd": route.acd,
                        "increment": route.increment
                    }
                    for route in top_route_name
                ]
            html_data = data_to_styled_html_table(email_data)
            message = f'''
                        <h4> {template.template_body_before}</h4>
                        {html_data}
                        <h4> {template.template_body_after}</h4>
                        <h4> {template.signatures}</h4>
                    '''
            email = EmailMultiAlternatives(template.TemplateSubject, message, 'simply2cloud@gmail.com', email_list)
            email.send()
        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)