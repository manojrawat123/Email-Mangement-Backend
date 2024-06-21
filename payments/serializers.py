from rest_framework import serializers
from payments.models import Payment

class PaymentSerializers(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    class Meta:
        model = Payment
        fields = "__all__"
    def get_customer_name(self, obj):
        return obj.customer_id.customer_name
