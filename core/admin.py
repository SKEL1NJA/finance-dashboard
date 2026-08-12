from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'content_type', 'object_id')
    list_filter = ('action', 'content_type')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False