from django.contrib import admin
from useripaddress.models import IpAdderessCompanyCustomer

@admin.register(IpAdderessCompanyCustomer)
class IpAdderessCompanyCustomer(admin.ModelAdmin):
    list_display = ('customer_id', 'ip_address', 'company_id', 'active', 'added_date')
    search_fields = ('customer_id__username', 'ip_address', 'company_id__username')
    list_filter = ('active', 'added_date')
    ordering = ('-added_date',)
