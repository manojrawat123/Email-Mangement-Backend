from django.contrib import admin
from .models import CustomerRateTable

class RateAdmin(admin.ModelAdmin):
    list_display = ('rate_name', 'customer_id', 'customer_prefix', 'rate_profile', 'created_date', 'rate_status')
    list_filter = ('rate_profile', 'rate_status')
    search_fields = ('rate_name', 'customer_prefix')

admin.site.register(CustomerRateTable, RateAdmin)