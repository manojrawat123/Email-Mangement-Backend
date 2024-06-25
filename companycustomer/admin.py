from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'company_name',
        'company_phone',
        'rates_email',
        'billing_email',
        'legal_email',
        'manager_name',
        'manager_email',
        'manager_phone',
        'status',
        'dnd',
    )

    list_filter = ('status', 'dnd')
    search_fields = ('customer_name', 'company_name', 'manager_name', 'manager_email')
    list_per_page = 20
