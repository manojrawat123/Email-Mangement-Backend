from django.contrib import admin
from .models import EmailTemplate

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'TemplateID',
        'TemplateName',
        'TemplateSubject',
        'Status',
        'CreatedDateTime',
        'LastUpdatedDateTime',
        'CCTO',
        'template_body_before',
        'template_body_after'
    )
    list_filter = ('Status',)
    search_fields = ('TemplateName', 'TemplateSubject', 'CCTO')
    list_per_page = 20
