from django.contrib import admin
from django.conf import settings

# 自定义管理界面
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE

# 注册模型
from users.models import User, UserProfile
from equipment.models import Equipment, EquipmentType, EquipmentMaintenance, EquipmentAlert
from process_data.models import ProcessData, ProcessParameter, ProcessResult

# 用户管理
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active', 'date_joined')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'department', 'position', 'phone')
    search_fields = ('user__username', 'full_name', 'department')
    list_filter = ('department', 'position')

# 设备管理
@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'equipment_type', 'status', 'location', 'responsible_person')
    list_filter = ('status', 'equipment_type', 'responsible_person')
    search_fields = ('name', 'code', 'serial_number', 'location')
    date_hierarchy = 'created_at'

@admin.register(EquipmentMaintenance)
class EquipmentMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'maintenance_type', 'performed_by', 'start_time', 'end_time', 'cost')
    list_filter = ('maintenance_type', 'performed_by', 'start_time')
    search_fields = ('equipment__name', 'description', 'notes')
    date_hierarchy = 'start_time'

@admin.register(EquipmentAlert)
class EquipmentAlertAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'level', 'title', 'is_resolved', 'created_at', 'resolved_at')
    list_filter = ('level', 'is_resolved', 'created_at')
    search_fields = ('equipment__name', 'title', 'message')
    date_hierarchy = 'created_at'

# 工艺数据管理
@admin.register(ProcessData)
class ProcessDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'equipment', 'operator', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'equipment', 'operator')
    search_fields = ('name', 'description', 'notes')
    date_hierarchy = 'start_time'

@admin.register(ProcessParameter)
class ProcessParameterAdmin(admin.ModelAdmin):
    list_display = ('process', 'parameter_name', 'parameter_value', 'unit')
    list_filter = ('parameter_name', 'unit')
    search_fields = ('process__name', 'parameter_name', 'parameter_value')

@admin.register(ProcessResult)
class ProcessResultAdmin(admin.ModelAdmin):
    list_display = ('process', 'result_type', 'value', 'unit', 'created_at')
    list_filter = ('result_type', 'created_at')
    search_fields = ('process__name', 'result_type', 'value')
    date_hierarchy = 'created_at' 