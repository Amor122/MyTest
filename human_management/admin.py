from django.contrib import admin

from . import models


@admin.register(models.Permission)
class PermissionModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'permission_name', 'permission_number')
    fields = ('permission_name', 'permission_number')
    list_per_page = 10
    search_fields = ('permission_name',)


@admin.register(models.OrganizationType)
class OrganizationTypeModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization_type_name')
    fields = ('organization_type_name', 'permissions')
    list_per_page = 10
    search_fields = ('organization_type_name',)


@admin.register(models.Organization)
class OrganizationModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization_name', 'organization_type')
    fields = ('organization_name', 'up_organization', 'organization_type')
    list_per_page = 10
    list_filter = ('organization_type',)
    search_fields = ('organization_name',)


@admin.register(models.Human)
class HumanModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'user_name', 'organization')
    fields = ('user_id', 'user_name', 'organization', 'password')
    list_per_page = 10
    list_filter = ('organization',)
    search_fields = ('user_name',)


@admin.register(models.HumanPost)
class HumanPostModelAdmin(admin.ModelAdmin):
    list_display = ('post_name', 'is_primary')
    fields = ('post_name', 'is_primary')
    list_per_page = 10
    search_fields = ('post_name',)
