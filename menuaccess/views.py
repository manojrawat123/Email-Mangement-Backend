from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from menu.serializer import MenuSerializer
from submenu.serializer import SubMenuSerializer
from menu.models import Menu
from submenu.models import Submenu
from menuaccess.models import MenuAccess
from django.db.models import Q
from menuaccess.serializer import MenuAccessSerializer
from django.shortcuts import get_object_or_404

# Create your views here.
class MenuAccessApiView(APIView):
    def get(self, request, id = None):
        try:
            if id is None:
                return Response({ "error" : "Method Not Allowed !!" }, status=status.HTTP_400_BAD_REQUEST)
            else:
                ######### Data Of accessed NavBar #######
                try:
                    menu_access = MenuAccess.objects.get(user_id = id)
                except Exception as e:
                    menu = Menu.objects.filter(Q(active = True) & ~ Q(id = 2))
                    menu_serializer = MenuSerializer(menu, many = True)
                    for i in menu_serializer.data:
                        i['label'] = i['name']
                        submenu = Submenu.objects.filter(menu = i['id'])
                        submenu_serializer = SubMenuSerializer(submenu, many=True)
                        i['option'] = []
                    return Response({
                        "not_allowed" : menu_serializer.data,
                        "allowed" : []
                    }, status=status.HTTP_200_OK)
                menu = Menu.objects.filter(Q(active = True) & Q(id__in = menu_access.menu_id.all()) & ~Q(id = 2))
                menu_serializer = MenuSerializer(menu, many = True)

                # Not Accessed Menus
                no_menu = Menu.objects.exclude(Q(active = True) & Q(id__in = menu_access.menu_id.all())).filter(~Q(id = 2))
                not_menu_serializer = MenuSerializer(no_menu, many = True)
                for i in not_menu_serializer.data:
                    i['label'] = i['name'] 
                    i['option'] = []
                    
                for i in menu_serializer.data:
                    i['label'] = i['name'] 
                    submenu = Submenu.objects.filter(Q(menu = i['id'])).exclude(id__in = menu_access.sub_menu.all())
                    submenu_serializer = SubMenuSerializer(submenu, many=True)
                    submenu_fil = Submenu.objects.filter(Q(menu = i['id'])).filter(id__in = menu_access.sub_menu.all())
                    submenu_serializer_fil = SubMenuSerializer(submenu_fil, many=True)
                    i["allowed_option"] = submenu_serializer_fil.data
                    i['option'] = []
                    i['not_allowed_option'] = submenu_serializer.data

                return Response({
                    "not_allowed" : not_menu_serializer.data,
                    "allowed" : menu_serializer.data
                }, status = status.HTTP_200_OK)       
                
                
        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self , request, id= None):
        try:
            if id is None:
                return Response({ "error" : "Method Not Allowed !!"} , status=status.HTTP_400_BAD_REQUEST)
            try: 
                menu_access = MenuAccess.objects.get(Q(user_id = id))
            except Exception as e:
                menu_access_serializer = MenuAccessSerializer(data={**request.data, "user_id" : id, "company_id" : request.user.id})    
                if menu_access_serializer.is_valid():
                    menu_access_serializer.save()
                    return Response({"message" :"Menu Assigned Successfully"})
                else:
                    return Response(menu_access_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if request.data.get('post_menu') in ['True', True, "true"]:
                new_menu = get_object_or_404(Menu, id=request.data.get("menu_id")[0])
                menu_access.menu_id.add(new_menu)
                return Response({"message" : "Data Saved Successfully!!"})
            else:
                new_sub_menu = get_object_or_404(Submenu, id=request.data.get("submenu"))
                menu_access.sub_menu.add(new_sub_menu)
                return Response({"message" : "Submenu Accessed Granted Successfully!!"}, status=status.HTTP_200_OK)
                

        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request, id = None):
        try:
            if id is None:
                return Response({"error" : "Method Not Allowed"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if request.data.get('menu_delete') in ['true', True, "True"]:
                    menu_access = MenuAccess.objects.get(Q(user_id = id) & Q(company_id = request.user.id))
                    menu = Menu.objects.get(id = request.data.get('menu_id'))
                    menu_access.menu_id.remove(menu)
                    return Response({"message" : "Deleted Successfully!!"}, status=status.HTTP_200_OK)
                else:
                    menu_access = MenuAccess.objects.get(Q(user_id = id) & Q(company_id = request.user.id))
                    sub_menu = Submenu.objects.get(id = request.data.get('sub_menuid'))
                    menu_access.sub_menu.remove(sub_menu)
                    return Response({"message" : "Deleted Successfully!!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                            