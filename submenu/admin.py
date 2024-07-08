from django.contrib import admin
from .models import Submenu
from menu.models import Menu

@admin.register(Submenu)
class SubmenuAdmin(admin.ModelAdmin):
    list_display = ('label', 'link', 'menu', 'active')
    list_filter = ('active', 'menu')
    search_fields = ('label', 'link')
