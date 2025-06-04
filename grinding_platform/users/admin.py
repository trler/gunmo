from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """自定义用户管理界面"""
    list_display = [
        'username', 'email', 'first_name', 'last_name', 
        'user_type', 'company', 'department', 'is_active', 'date_joined'
    ]
    list_filter = [
        'user_type', 'company', 'department', 'is_active', 
        'is_staff', 'date_joined'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'company']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('行业信息', {
            'fields': (
                'user_type', 'company', 'department', 
                'industry_role', 'phone'
            )
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('行业信息', {
            'fields': (
                'user_type', 'company', 'department', 
                'industry_role', 'phone'
            )
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """用户配置文件管理界面"""
    list_display = ['user', 'user__user_type', 'user__company']
    list_filter = ['user__user_type', 'user__company']
    search_fields = ['user__username', 'user__company']
    
    def user__user_type(self, obj):
        return obj.user.get_user_type_display()
    user__user_type.short_description = '用户类型'
    
    def user__company(self, obj):
        return obj.user.company
    user__company.short_description = '企业名称'
