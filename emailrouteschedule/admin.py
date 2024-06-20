from django.contrib import admin
from emailrouteschedule.models import EmailRouteSchedule

@admin.register(EmailRouteSchedule)
class EmailScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'schedule_date_time', 'schedule_template', 'status', 'schedule_route_id')
    list_filter = ('status', 'schedule_date_time')
    search_fields = ('schedule_template__name', 'schedule_route_id')
    ordering = ('-schedule_date_time',)
    filter_horizontal = ('schedule_customer',)
