from rest_framework import serializers
from dispute.models import Dispute

class DisputeSerialzer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    invoice = serializers.SerializerMethodField()
    class Meta:
        model = Dispute
        fields = "__all__"
    def get_customer_name(self, obj):
        return obj.customer_id.customer_name
    def get_invoice(self, obj):
        return obj.invoice_number.invoice_number