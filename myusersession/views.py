from django.shortcuts import render
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myusersession.serializers import UserRegistrationSerializer, UserGetSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from myusersession.htmlcontent import emailVerifyContent
from myusersession.ForgotEmailSenderFunc import sendPasswordResetEmail
from django.db.models import Q
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class CustomTokenObtainPairView(TokenObtainPairView):
    pass

class VerifySessionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        if request.user:
            return Response({"session" : True}, status=status.HTTP_200_OK)
        else:
            return Response({"error" : "User Register Successfully !!"}, status=status.HTTP_400_BAD_REQUEST)

class UserRegisterView(APIView):
    def post(self, request, id=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllUserView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, id = None):
        try:
            all_user = User.objects.all() 
            user_serialzer = UserGetSerializer(all_user, many=True)
            return Response(user_serialzer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, id = None):
        try:
            if id is None:
                return Response({"error" : "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            s_user = User.objects.get(id = id)
            if s_user:
                request.data['password'] = make_password(request.data.get('password'))
                user_serializer = UserRegistrationSerializer(s_user, data=request.data, partial=True) 
                if user_serializer.is_valid():
                    user_serializer.save()
                    return Response({"message" : "user Updated Successfully"})  
                else:
                    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)           
            else:
                return Response({"error" : "User Not Found"}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request, id =None):
        try:
            print("Hii")
            if id is None:
                return Response({"error" : "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            s_user = User.objects.get(id = id)
            if s_user:
                if s_user.is_active == False:
                    s_user.is_active = True
                else:
                    s_user.is_active = False
                s_user.save()
                return Response({"message" : "User Deleted Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error" : "User Not Found"}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class ForgotPassword(APIView):
    def post(self , request, id = None):
        try:
            domain_name = request.data.get('domain')
            print({
                "email" : request.data.get('email'),
                "domain" : domain_name
            })
            user = User.objects.get(Q(email = request.data.get("email")))
            if user is None:
                return Response({"error" : "Email Didn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                sendPasswordResetEmail(user, domain_name)
                return Response({"message" : "Reset Password Link Send to your email"},status=status.HTTP_200_OK)
        except Exception as e: 
            print(e)
            return Response({"error" : f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPassword(APIView):
    def post(self , request, userid_encode = None,token = None):
        try:
            activate = request.data.get("activate")
            password = request.data.get('password')
            pk = urlsafe_base64_decode(userid_encode)
            print(pk)
            user = User.objects.get(pk= pk)
            if default_token_generator.check_token(user,token):
                h_password = make_password(password)
                print(h_password)
                serializer = UserRegistrationSerializer(user, data={"password" : h_password}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "Password Reset Successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error" : "Not Authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR) 