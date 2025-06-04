from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError
import json

class SystemSettings(models.Model):
    """系统设置模型"""
    key = models.CharField(max_length=50, unique=True, verbose_name='设置键')
    value = models.JSONField(verbose_name='设置值')
    description = models.TextField(blank=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '系统设置'
        verbose_name_plural = '系统设置'
        ordering = ['key']

    def __str__(self):
        return f"{self.key}"

    def clean(self):
        """验证设置值的格式"""
        try:
            # 确保值可以被序列化为JSON
            json.dumps(self.value)
        except (TypeError, ValueError):
            raise ValidationError({'value': '设置值必须是有效的JSON格式'})

    def save(self, *args, **kwargs):
        """保存时更新缓存"""
        super().save(*args, **kwargs)
        # 更新缓存
        cache_key = f'system_settings_{self.key}'
        cache.set(cache_key, self.value)

    @classmethod
    def get_setting(cls, key, default=None):
        """获取设置值，优先从缓存获取"""
        cache_key = f'system_settings_{key}'
        value = cache.get(cache_key)
        
        if value is None:
            try:
                setting = cls.objects.get(key=key)
                value = setting.value
                cache.set(cache_key, value)
            except cls.DoesNotExist:
                value = default
                
        return value

    @classmethod
    def set_setting(cls, key, value, description=''):
        """设置值，同时更新缓存"""
        setting, created = cls.objects.update_or_create(
            key=key,
            defaults={
                'value': value,
                'description': description
            }
        )
        return setting

class SystemBackup(models.Model):
    """系统备份模型"""
    filename = models.CharField(max_length=255, verbose_name='文件名')
    file_path = models.FileField(upload_to='backups/', verbose_name='备份文件')
    backup_type = models.CharField(
        max_length=20,
        choices=[
            ('full', '完整备份'),
            ('database', '数据库备份'),
            ('files', '文件备份'),
            ('settings', '设置备份')
        ],
        verbose_name='备份类型'
    )
    size = models.BigIntegerField(verbose_name='文件大小')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    created_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='创建人'
    )
    description = models.TextField(blank=True, verbose_name='备份说明')
    is_auto = models.BooleanField(default=False, verbose_name='是否自动备份')

    class Meta:
        verbose_name = '系统备份'
        verbose_name_plural = '系统备份'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.filename} ({self.get_backup_type_display()})"

    def save(self, *args, **kwargs):
        """保存时更新文件大小"""
        if self.file_path and not self.size:
            self.size = self.file_path.size
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """删除时同时删除文件"""
        if self.file_path:
            self.file_path.delete()
        super().delete(*args, **kwargs)

class SystemLog(models.Model):
    """系统日志模型"""
    LEVEL_CHOICES = [
        ('info', '信息'),
        ('warning', '警告'),
        ('error', '错误'),
        ('critical', '严重错误')
    ]

    level = models.CharField(
        max_length=10,
        choices=LEVEL_CHOICES,
        default='info',
        verbose_name='日志级别'
    )
    message = models.TextField(verbose_name='日志消息')
    module = models.CharField(max_length=100, verbose_name='模块')
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='操作用户'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    metadata = models.JSONField(default=dict, blank=True, verbose_name='元数据')

    class Meta:
        verbose_name = '系统日志'
        verbose_name_plural = '系统日志'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['level', 'created_at']),
            models.Index(fields=['module', 'created_at']),
            models.Index(fields=['user', 'created_at'])
        ]

    def __str__(self):
        return f"[{self.level}] {self.message[:50]}"

    @classmethod
    def log(cls, level, message, module, user=None, ip_address=None, **metadata):
        """记录日志的便捷方法"""
        return cls.objects.create(
            level=level,
            message=message,
            module=module,
            user=user,
            ip_address=ip_address,
            metadata=metadata
        )
