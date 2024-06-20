from django.contrib import admin
from invoice.models import Invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number', 
        'customer_id', 
        'invoice_type', 
        'invoice_from_date', 
        'invoice_to_date', 
        'invoice_amount', 
        'created_date', 
        'active'
    )
    search_fields = (
        'invoice_number', 
        'customer_id__name',  # Assuming Customer has a 'name' field
        'invoice_type', 
        'status'
    )
    list_filter = (
        'invoice_type', 
        'created_date', 
        'active'
    )

admin.site.register(Invoice, InvoiceAdmin)
