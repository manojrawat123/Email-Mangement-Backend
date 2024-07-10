from django.shortcuts import render
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myusersession.serializers import MyUserSerializers , MyUserLoginSerializer,MyUserRegisterSerializer,CompanyUserUpdateSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from myusersession.htmlcontent import emailVerifyContent
from myusersession.ForgotEmailSenderFunc import sendPasswordResetEmail
from django.db.models import Q
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from myusersession.models import CompanyUser
from menu.serializer import MenuSerializer
from submenu.serializer import SubMenuSerializer
from menu.models import Menu
from submenu.models import Submenu
from menuaccess.models import MenuAccess



class CustomTokenObtainPairView(TokenObtainPairView):
    pass

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserLoginView(APIView):
    def post(self, request, id =None):
        try:
            serializers = MyUserLoginSerializer(data=request.data)
            if serializers.is_valid(raise_exception=True):
                email = serializers.data.get("email")
                password = serializers.data.get("password")
                user = authenticate(email = email, password = password)
                if user is not None:
                    token = get_token_for_user(user)
                    return Response({'token': token,"user_type": user.user_type, 'msg': "User Login Sucessfully"})
                else:
                    return Response({"error" : "No User Found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifySessionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        try:
            if request.user:
                if request.user.company_admin:
                    menu = Menu.objects.filter(active = True)
                    menu_serializer = MenuSerializer(menu, many = True)
                    for i in menu_serializer.data:
                        i['label'] = i['name'] 
                        submenu = Submenu.objects.filter(menu = i['id'])
                        submenu_serializer = SubMenuSerializer(submenu, many=True)
                        i['option'] = submenu_serializer.data
                    return Response({"session" : True, "is_company" : True, "navbar" : menu_serializer.data }, status=status.HTTP_200_OK)
                else:
                    try:
                        menu_ids = MenuAccess.objects.get(user_id = request.user.id).menu_id.all()
                    except Exception as e:
                        menu_ids = []
                    try:
                        submenu_ids = MenuAccess.objects.get(user_id = request.user.id).sub_menu.all()
                    except Exception as e:
                        submenu_ids = []
                    menu = Menu.objects.filter(Q(active = True) & Q(id__in = menu_ids))
                    menu_serializer = MenuSerializer(menu, many = True)
                    for i in menu_serializer.data:
                        i['label'] = i['name'] 
                        submenu = Submenu.objects.filter(Q(menu = i['id']) & Q(id__in = submenu_ids))
                        submenu_serializer = SubMenuSerializer(submenu, many=True)
                        i['option'] = submenu_serializer.data
                    return Response({"session" : True, "is_company" : False, "navbar" : menu_serializer.data }, status=status.HTTP_200_OK)
            else:
                return Response({"error" : "UnAuth User!!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserRegisterView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id=None):
        try:

            if (request.user.company_admin):
                serializer = MyUserSerializers(data={**request.data, "company_name" : request.user.company_name})
                if serializer.is_valid():
                    serializer.save()
                    try:
                        user = CompanyUser.objects.get(email = serializer.data.get('email'))
                        user.is_active = True
                        user.parent_user = request.user
                        user.user_name = request.data.get("user_name")
                        user.save()
                        return Response({"message" : "User Registration Successfully"}, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        return Response({"error" : e}, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = MyUserSerializers(data={**request.data, "company_name" : request.user.company_name})
                if serializer.is_valid():
                    serializer.save()
                    try:
                        user = CompanyUser.objects.get(email = serializer.data.get('email'))
                        user.is_active = True
                        user.parent_user = request.user.parent_user
                        user.user_name = request.data.get("user_name")
                        user.save()
                        return Response({"message" : "User Registration Successfully"}, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        return Response({"error" : e}, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"})

class GetAllUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        try:
            all_user = CompanyUser.objects.filter(Q(parent_user = request.user.id) | Q(id = request.user.id)) 
            user_serialzer = MyUserRegisterSerializer(all_user, many=True)
            for i in user_serialzer.data:
                if i['parent_user'] is not None:
                    print(i['parent_user'])
                    i['added_by'] = CompanyUser.objects.get(id = i['parent_user']).user_name
                else:
                    i['added_by'] = 'Admin'
            return Response(user_serialzer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, id = None):
        try:
            if id is None:
                s_user = CompanyUser.objects.get(id = request.user.id)
                request.data['password'] = make_password(request.data.get('password'))
                user_serializer = CompanyUserUpdateSerializer(s_user, data=request.data, partial=True) 
                if user_serializer.is_valid():
                    user_serializer.save()
                    return Response({"message" : "user Updated Successfully"})  
                return Response(user_serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            s_user = CompanyUser.objects.get(Q(id = id) & Q(parent_user = request.user.id))
            if s_user:
                request.data['password'] = make_password(request.data.get('password'))
                print(request.data.get('password') == request.data.get('password2'))
                user_serializer = CompanyUserUpdateSerializer(s_user, data=request.data, partial=True) 
                if user_serializer.is_valid():
                    user_serializer.save()
                    return Response({"message" : "user Updated Successfully"})  
                else:
                    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)           
            else:
                return Response({"error" : "User Not Found"}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            print(request.data)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, id =None):
        try:
            print("Hii")
            if id is None:
                return Response({"error" : "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            s_user = CompanyUser.objects.get(id = id)
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
            user = CompanyUser.objects.get(Q(email = request.data.get("email")))
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
            user = CompanyUser.objects.get(pk= pk)
            if default_token_generator.check_token(user,token):
                h_password = make_password(password)
                print(h_password)
                serializer = MyUserSerializers(user, data={"password" : h_password}, partial=True)
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