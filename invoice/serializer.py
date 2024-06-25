from invoice.models import Invoice
from rest_framework import serializers

class InvoiceSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    class Meta:
        model = Invoice
        fields = '__all__'
    def get_customer_name(self, obj):
        return obj.customer_id.customer_name
    