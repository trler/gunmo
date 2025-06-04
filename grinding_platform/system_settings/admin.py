from django.contrib import admin
from .models import SystemSettings, SystemBackup, SystemLog

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    """系统设置管理"""
    list_display = ['key', 'description', 'created_at', 'updated_at']
    search_fields = ['key', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['key']

@admin.register(SystemBackup)
class SystemBackupAdmin(admin.ModelAdmin):
    """系统备份管理"""
    list_display = ['filename', 'backup_type', 'size', 'created_at', 'created_by', 'is_auto']
    list_filter = ['backup_type', 'is_auto', 'created_at']
    search_fields = ['filename', 'description']
    readonly_fields = ['created_at', 'size']
    ordering = ['-created_at']

@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    """系统日志管理"""
    list_display = ['level', 'message', 'module', 'user', 'ip_address', 'created_at']
    list_filter = ['level', 'module', 'created_at']
    search_fields = ['message', 'module', 'ip_address']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        """禁止手动添加日志"""
        return False

    def has_change_permission(self, request, obj=None):
        """禁止修改日志"""
        return False
