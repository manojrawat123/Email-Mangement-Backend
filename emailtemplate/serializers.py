from rest_framework import serializers
from emailtemplate.models import EmailTemplate

class EmailTemplateSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = "__all__"