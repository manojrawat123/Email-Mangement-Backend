from rest_framework import serializers
from emaillog.models import EmailLog
from django.db.models import FileField


class EmailLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailLog
        fields = "__all__"