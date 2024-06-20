from django.contrib import admin
from .models import Route

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('top_route_name', 'date', 'destination', 'profile', 'rate', 'asr', 'acd', 'increment', 'status')
    search_fields = ('top_route_name', 'destination', 'profile')
    list_filter = ('date', 'status', 'destination')