from django.contrib import admin
from .models import VendorRateTabel

@admin.register(VendorRateTabel)
class VendorRateTabelAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'vendor_rate_name', 'customer_id', 'vendor_prefix', 'vendor_rate_profile',  'rate_status')
    list_filter = ('rate_status', 'vendor_rate_profile')
    search_fields = ('vendor_rate_name', 'vendor_prefix', 'company_id__username', 'customer_id__customer_name', 'vendor_rate_profile__profile_name')

    # Customize the admin form if needed
    fieldsets = (
        (None, {
            'fields': ('company_id', 'vendor_rate_name', 'customer_id', 'vendor_prefix', 'vendor_rate_profile', 'rate_status')
        }),
    )
