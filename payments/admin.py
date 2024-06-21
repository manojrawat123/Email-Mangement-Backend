from django.contrib import admin
from payments.models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'payment_type', 'payment_date', 'payment_amount', 'active')
    search_fields = ('customer_id', 'payment_type', 'active')
    list_filter = ('payment_type', 'active', 'payment_date')
    ordering = ('-payment_date',)

admin.site.register(Payment, PaymentAdmin)
