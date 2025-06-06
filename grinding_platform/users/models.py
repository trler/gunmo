from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """扩展的用户模型 - 适用于滚磨光整加工行业"""
    
    USER_TYPE_CHOICES = [
        ('system_admin', '系统管理员'),
        ('process_engineer', '工艺工程师'),
        ('equipment_operator', '设备操作员'),
        ('quality_inspector', '质量检测员'),
        ('enterprise_admin', '企业管理员'),
        ('fullstack_engineer', '全栈工程师'),
    ]
    
    # 基本信息字段
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPE_CHOICES, 
        default='equipment_operator',
        verbose_name='用户类型'
    )
    company = models.CharField(max_length=200, blank=True, verbose_name='企业名称')
    department = models.CharField(max_length=100, blank=True, verbose_name='部门')
    industry_role = models.CharField(max_length=100, blank=True, verbose_name='产业链角色')
    
    # 联系信息
    phone = models.CharField(max_length=20, blank=True, verbose_name='电话')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        
    def __str__(self):
        return f"{self.username}({self.get_user_type_display()})"

    def get_user_type_display_name(self):
        """获取用户类型显示名称"""
        return dict(self.USER_TYPE_CHOICES).get(self.user_type, self.user_type)

class UserProfile(models.Model):
    """用户配置文件"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    bio = models.TextField(blank=True, verbose_name='个人简介')
    preferences = models.JSONField(default=dict, verbose_name='用户偏好设置')
    
    class Meta:
        verbose_name = '用户配置'
        verbose_name_plural = '用户配置'
        
    def __str__(self):
        return f"{self.user.username}的配置"
