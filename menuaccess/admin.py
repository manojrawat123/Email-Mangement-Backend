from django.contrib import admin
from .models import MenuAccess

class MenuAccessAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'company_id', 'active')
    list_filter = ('active', 'company_id')
    search_fields = ('user_id__username', 'company_id__username')
    filter_horizontal = ('menu_id', 'sub_menu')

admin.site.register(MenuAccess, MenuAccessAdmin)
