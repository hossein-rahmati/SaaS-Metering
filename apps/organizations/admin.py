from django.contrib import admin
from .models import Organization, APIKey

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ("organization", "name", "key", "created_at", "is_active")
    list_filter = ("organization", "is_active")
    readonly_fields = ("key", "created_at")

admin.site.register(Organization)
