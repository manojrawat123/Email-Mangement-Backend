from django.contrib import admin
from .models import EmailLog

class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'date', 'template_id')
    list_filter = ('date', 'template_id')
    search_fields = ('log_id', 'template_id')

    # Optionally, define actions to perform bulk actions on selected email logs
    actions = ['mark_as_read', 'mark_as_unread']
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_read.short_description = 'Mark selected email logs as read'
    mark_as_unread.short_description = 'Mark selected email logs as unread'

admin.site.register(EmailLog, EmailLogAdmin)
