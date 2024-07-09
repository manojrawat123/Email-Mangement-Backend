from django.contrib import admin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'company_id', 'user_id', 'company_phone', 'rates_email', 'billing_email', 'country_code', 'legal_email', 'manager_name', 'created_date', 'manager_email', 'manager_phone_country_code', 'manager_phone', 'status', 'active', 'dnd')
    list_filter = ('company_id', 'country_code', 'status', 'active', 'dnd')
    search_fields = ('customer_name', 'company_phone', 'rates_email', 'billing_email', 'legal_email', 'manager_name', 'manager_email', 'manager_phone')
    ordering = ('-created_date',)

admin.site.register(Customer, CustomerAdmin)
