from rest_framework import serializers
from emailrouteschedule.models import EmailRouteSchedule

class EmailSheduleSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmailRouteSchedule
        fields = "__all__"