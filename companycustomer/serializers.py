from rest_framework import serializers
from companycustomer.models import Customer
from myusersession.serializers import MyUserRegisterSerializer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__" 


class CustomerGetSerializer(serializers.ModelSerializer):
    user_id = MyUserRegisterSerializer()
    class Meta:
        model = Customer
        fields = "__all__"