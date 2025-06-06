from django.contrib import admin
from .models import Company, Department, Personnel, Standard


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'company_type', 'scale', 'phone', 'is_active', 'created_at']
    list_filter = ['company_type', 'scale', 'is_active', 'created_at']
    search_fields = ['code', 'name', 'short_name', 'unified_social_code']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('code', 'name', 'short_name', 'company_type')
        }),
        ('注册信息', {
            'fields': ('unified_social_code', 'legal_representative', 'registered_capital', 
                      'establishment_date', 'scale')
        }),
        ('联系信息', {
            'fields': ('address', 'postal_code', 'phone', 'fax', 'email', 'website')
        }),
        ('业务信息', {
            'fields': ('business_scope', 'main_products', 'industry_category')
        }),
        ('资质信息', {
            'fields': ('certifications', 'quality_system')
        }),
        ('状态信息', {
            'fields': ('is_active', 'remarks')
        }),
        ('时间戳', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'company', 'department_type', 'level', 'manager', 'is_active']
    list_filter = ['company', 'department_type', 'level', 'is_active']
    search_fields = ['code', 'name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('code', 'name', 'department_type', 'company', 'parent_department')
        }),
        ('部门信息', {
            'fields': ('level', 'manager', 'description', 'responsibilities')
        }),
        ('联系信息', {
            'fields': ('office_location', 'extension', 'email')
        }),
        ('状态信息', {
            'fields': ('is_active', 'establishment_date')
        }),
        ('时间戳', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'name', 'company', 'department', 'position', 'status', 'is_active']
    list_filter = ['company', 'department', 'gender', 'education', 'employment_type', 'status', 'is_active']
    search_fields = ['employee_id', 'name', 'phone', 'position']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('employee_id', 'user', 'name', 'gender', 'birth_date', 'id_card')
        }),
        ('组织信息', {
            'fields': ('company', 'department', 'position', 'job_level', 'employment_type')
        }),
        ('入职信息', {
            'fields': ('hire_date', 'contract_start', 'contract_end', 'probation_end')
        }),
        ('教育背景', {
            'fields': ('education', 'major', 'graduate_school', 'graduation_date')
        }),
        ('联系信息', {
            'fields': ('phone', 'email', 'address', 'emergency_contact', 'emergency_phone')
        }),
        ('工作信息', {
            'fields': ('skills', 'certifications', 'work_experience')
        }),
        ('状态信息', {
            'fields': ('status', 'is_active')
        }),
        ('时间戳', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ['standard_code', 'title', 'standard_type', 'publisher', 'publish_date', 'status', 'is_active']
    list_filter = ['standard_type', 'status', 'is_mandatory', 'is_active', 'publish_date']
    search_fields = ['standard_code', 'title', 'keywords', 'publisher']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('standard_code', 'title', 'english_title', 'standard_type')
        }),
        ('发布信息', {
            'fields': ('publisher', 'publish_date', 'implement_date', 'revision_date')
        }),
        ('内容信息', {
            'fields': ('scope', 'abstract', 'keywords', 'classification')
        }),
        ('关联信息', {
            'fields': ('replaced_standards', 'referenced_standards', 'related_standards')
        }),
        ('文档信息', {
            'fields': ('file_url', 'page_count', 'language')
        }),
        ('状态信息', {
            'fields': ('status', 'is_mandatory', 'is_active')
        }),
        ('时间戳', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    ) 