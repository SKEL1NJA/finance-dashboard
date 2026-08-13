from django.contrib import admin

from .models import AuditLog


class SoftDeleteAdminMixin:
    def get_queryset(self, request):
        return self.model.all_objects.all()

    def is_deleted_display(self, obj):
        return obj.is_deleted
    is_deleted_display.short_description = 'Deleted'
    is_deleted_display.boolean = True

    @admin.action(description='Restore selected items')
    def restore_items(self, request, queryset):
        updated = queryset.update(is_deleted=False, deleted_at=None)
        self.message_user(request, f'{updated} item(s) restored.')

    actions = ['restore_items']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'content_type', 'object_id')
    list_filter = ('action', 'content_type')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False