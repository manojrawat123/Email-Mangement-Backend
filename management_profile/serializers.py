from rest_framework import serializers
from management_profile.models import ManagementProfileName

class ManagementProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementProfileName
        fields = "__all__"