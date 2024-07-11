from django.contrib import admin
from .models import VendorRate

@admin.register(VendorRate)
class VendorRateAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'vendor_rate_id', 'country_code', 'country_name', 'rate', 'billing_increment_1', 'billing_increment_n', 'status', 'effective_date', 'created_date', 'rate_status')
    list_filter = ('status', 'rate_status', 'country_code', 'effective_date')
    search_fields = ('country_name', 'vendor_rate_id__id')

    # Customize the admin form if needed
    fieldsets = (
        (None, {
            'fields': ('company_id', 'vendor_rate_id', 'country_code', 'country_name', 'rate', 'billing_increment_1', 'billing_increment_n', 'status', 'effective_date', 'created_date', 'rate_status')
        }),
    )
