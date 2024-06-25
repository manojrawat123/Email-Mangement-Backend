# admin.py

from django.contrib import admin
from .models import CountryCode

class CountryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'status')
    list_filter = ('status',)
    search_fields = ('code', 'name')

admin.site.register(CountryCode, CountryAdmin)