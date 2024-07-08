from rest_framework import serializers
from myusersession.models import CompanyUser
from django.contrib.auth.hashers import make_password

class MyUserSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password"}, write_only = True)
    class Meta:
        model = CompanyUser
        fields = ["email","company_name", "company_phone", "password", "password2"]
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError("Password Didn't match")
        return attrs
    
    def create(self, validate_data):
        validate_data.pop('password2')
        return CompanyUser.objects.create_user(**validate_data)
    
    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            instance.password = make_password(password)
        instance.save()
        return instance

class MyUserRegisterSerializer(serializers.ModelSerializer):
    active = serializers.SerializerMethodField()
    class Meta:
        model = CompanyUser
        exclude = ["password", "is_superuser", "is_admin"] 
    def get_active(self, obj):
        return obj.is_active


class MyUserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 225)
    class Meta:
        model = CompanyUser
        fields = ["email", "password"]

    def validate(self, data):
        for field_name, value in data.items():
            if value == "":
                raise serializers.ValidationError(f"{field_name} field is required.")
        return data
    

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = CompanyUser
    fields = "__all__"



class CompanyUserDetailCompanyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUser
        fields = ["id","name", "address"]

class CompanyUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUser
        fields = ["id", "company_name", "email", "company_phone", "password"]

# Z6SAGCK6X5V2Y6P72AF14ZAM
