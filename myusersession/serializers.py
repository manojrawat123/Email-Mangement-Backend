# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name' ,'password','id' ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    

class UserGetSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(source='is_active')
    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name','id', 'active' ]
    