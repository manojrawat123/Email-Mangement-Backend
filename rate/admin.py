from django.contrib import admin
from .models import RateTabel

class RateTabelAdmin(admin.ModelAdmin):
    list_display = ('country_code', 'country_name', 'customer_rate_id', 'rate', 'billing_increment_1', 'billing_increment_n', 'status', 'effective_date', 'created_date', 'rate_status')
    search_fields = ('country_code', 'country_name', 'rate_status')
    list_filter = ('status', 'effective_date', 'created_date', 'rate_status')
    ordering = ('country_code',)

admin.site.register(RateTabel, RateTabelAdmin)