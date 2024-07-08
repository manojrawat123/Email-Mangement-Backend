from django.shortcuts import render
from rest_framework.views import APIView
import pandas as pd
import datetime
from rest_framework.response import Response
from rest_framework import status
from toproutes.models import Route
from django.db.models import Q
from emaillog.data_to_html import data_to_styled_html_table, data_to_styled_html_table_rate,data_to_styled_html_table_react
from toproutes.serializer import TopRouteSerializer
from rest_framework.permissions import IsAuthenticated
from rate.models import RateTabel

# Create your views here.
class AddTopRoutes(APIView):
    permission_classes = [IsAuthenticated]
    def post(self , request, id = None):
        try:
            excel_file = request.data.get("excel_sheet")
            df = pd.read_excel(excel_file)
            top_route = request.data.get("route_name")
            required_columns = ["Route", "Profile", "Rate", "ASR", "ACD", "Increment"]
            company_id = request.user if request.user.company_admin else request.user.parent_user

            all_top_route = Route.objects.filter(Q(top_route_name = top_route) & (Q(company_id = request.user.id) |
                                                                                   Q(user_id = request.user.id)))
            if len(all_top_route) != 0:
                return Response({"error" : "Route Name should unique"}, status=status.HTTP_400_BAD_REQUEST)
            if not all(column in df.columns for column in required_columns):
                return Response({"error": "Missing required columns in the uploaded file"}, status=status.HTTP_400_BAD_REQUEST)
            for index, row in df.iterrows():
                missing_fields = [column for column in required_columns if pd.isna(row[column])]
                if missing_fields:
                    error_message = f"Missing values in columns {missing_fields} in row {index + 1}"
                    return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
                # Check types of fields
                objs = []
                for column in required_columns:
                    if column not in ["ASR", "Rate"] and not isinstance(row[column], str):
                        error_message = f"Invalid type for field {column} in row {index + 1}"
                        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
                    elif column in ["ASR", "Rate"] and not isinstance(row[column], (str, int, float)):
                        error_message = f"Invalid type for field {column} in row {index + 1}"
                        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
            for index, row in df.iterrows():
                try:
                    route = Route.objects.get(
                        Q(top_route_name = top_route) & Q(destination = row["Route"]) & (Q(company_id = request.user.id) | Q(customer_id__user_id = request.user.id))
                    )
                    route.destination = row["Route"]
                    route.profile = row["Profile"]
                    route.rate = row["Rate"]
                    route.asr = row["ASR"]
                    route.acd = row["ACD"]
                    route.increment = row["Increment"]
                    route.status = True
                    route.save()
                except Exception as e:
                    objs.append(Route(
                        top_route_name = top_route,
                        destination =row["Route"],
                        profile = row["Profile"],
                        rate =  row["Rate"] ,
                        asr = row["ASR"]  ,
                        acd  =row["ACD"]  ,
                        increment=  row["Increment"] ,
                        company_id = company_id,
                        user_id = request.user,
                        status = True
                    ))
            Route.objects.bulk_create(objs)
            return Response({"message" : "Route Added Successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id=None):
        try:
            if id is None:
                return Response({"error" : "Method Not Allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                top_route = Route.objects.get(Q(id = id) & (Q(company_id = request.user.id) | Q(user_id = request.user.id)))
                top_route_serializer = TopRouteSerializer(top_route, data=request.data, partial =True)
                if top_route_serializer.is_valid():
                    top_route_serializer.save()
                    return Response({"message" : "Top Route Updated Successfully"}, status= status.HTTP_200_OK)
                else:
                    return Response(top_route_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

    def delete(self, request, id = None):
        if id == None:
            return Response({"error" : "Method Not Allowed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                route = Route.objects.get(Q(id = id) & (Q(user_id = request.user.id) | Q(company_id = request.user.id)))
                route.delete()
                return Response({"error" : "Data Removed Successfully!!"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetTopRouteTable(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id = None):
        try:
            route_id = request.data.get('top_route_name')
            company_id = request.user if request.user.company_admin else request.user.parent_user

            objs = []
            if route_id is None:
                return Response({"error" : "Please Provide Route Id"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                required_columns = ["Route", "Profile", "Rate", "ASR", "ACD", "Increment"]
                excel_file = request.data.get("excel_sheet")
                df = pd.read_excel(excel_file)
                for index, row in df.iterrows():
                    missing_fields = [column for column in required_columns if pd.isna(row[column])]
                    if missing_fields:
                        error_message = f"Missing values in columns {missing_fields} in row {index + 1}"
                        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
                objs = []
                for column in required_columns:
                    if column not in ["ASR", "Rate"] and not isinstance(row[column], str):
                        error_message = f"Invalid type for field {column} in row {index + 1}"
                        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
                    elif column in ["ASR", "Rate"] and not isinstance(row[column], (str, int, float)):
                        error_message = f"Invalid type for field {column} in row {index + 1}"
                        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
                for index ,row in df.iterrows():
                    objs.append(Route(
                            top_route_name = route_id,
                            destination =row["Route"],
                            profile = row["Profile"],
                            rate =  row["Rate"] ,
                            asr = row["ASR"]  ,
                            acd  =row["ACD"]  ,
                            increment=  row["Increment"] ,
                            status = True,
                            user_id = request.user,
                            company_id = company_id
                        ))
                route_all = Route.objects.filter(Q(top_route_name = route_id) & Q(user_id = request.user.id))
                route_all.delete()
                Route.objects.bulk_create(objs)
                return Response({"messsage" : "Data Updated Successfully"})
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error" }, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, id=None):
        try:
            route_id = request.query_params.get("route_id")
            if route_id is None:
                return Response({"error" : "Please Provide Route Id"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                top_route_name = Route.objects.filter(Q(top_route_name = route_id) & (Q(user_id = request.user.id) | Q(company_id = request.user.id)))
                if len(top_route_name) != 0:
                    email_data = [
                            {
                                "id" : route.id,
                                "destination": route.destination,
                                "top_route_name": route.top_route_name,
                                "profile": route.profile,
                                "rate": f"{route.rate:.4f}",  
                                "asr": route.asr,
                                "acd": route.acd,
                                "increment": route.increment,
                                "user_id" : request.user.id
                            }
                            for route in top_route_name
                        ]
                    html_data = data_to_styled_html_table(email_data)
                    react_data = data_to_styled_html_table_react(email_data)
                    return Response({
                        "html_data" : html_data,
                        "normal_data" : email_data,
                        "react_data" : react_data
                    } , status=status.HTTP_200_OK)
                else:
                    return Response({"normal_data" : []}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Occured"}, status=status.HTTP_400_BAD_REQUEST)           
