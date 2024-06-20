from django.contrib import admin
from .models import ManagementProfileName

class ManagementProfileNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ('active',)
    search_fields = ('name',)

admin.site.register(ManagementProfileName, ManagementProfileNameAdmin)
