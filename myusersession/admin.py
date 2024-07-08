from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CompanyUser

class CompanyUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form_template = None
    change_user_password_template = None

    list_display = ('email', 'company_name', 'company_phone', 'is_admin', 'parent_user', 'user_name')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('company_name', 'company_address', 'company_phone', 'company_desc', 'parent_user', 'company_admin', 'user_name')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_superuser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'company_name', 'company_phone', 'password1', 'password2', 'parent_user'),
        }),
    )
    search_fields = ('email', 'company_name')
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(CompanyUser, CompanyUserAdmin)
# Unregister the Group model from admin.
# admin.site.unregister(Group)
