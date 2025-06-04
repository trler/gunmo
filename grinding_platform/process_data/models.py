from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProcessCategory(models.Model):
    """工艺类别"""
    name = models.CharField(max_length=100, unique=True, verbose_name='类别名称')
    description = models.TextField(blank=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '工艺类别'
        verbose_name_plural = '工艺类别'
        
    def __str__(self):
        return self.name

class ProcessData(models.Model):
    """工艺数据"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('active', '激活'),
        ('inactive', '停用'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='工艺名称')
    category = models.ForeignKey(ProcessCategory, on_delete=models.CASCADE, verbose_name='工艺类别')
    description = models.TextField(verbose_name='工艺描述')
    parameters = models.JSONField(default=dict, verbose_name='工艺参数')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    
    # 工艺具体参数
    grinding_speed = models.FloatField(null=True, blank=True, verbose_name='磨削速度 (rpm)')
    pressure = models.FloatField(null=True, blank=True, verbose_name='压力 (bar)')
    temperature = models.FloatField(null=True, blank=True, verbose_name='温度 (°C)')
    processing_time = models.IntegerField(null=True, blank=True, verbose_name='加工时间 (分钟)')
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '工艺数据'
        verbose_name_plural = '工艺数据'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} - {self.category.name}"

class ProcessHistory(models.Model):
    """工艺历史记录"""
    process_data = models.ForeignKey(ProcessData, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=50, verbose_name='操作类型')
    changes = models.JSONField(default=dict, verbose_name='变更内容')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='操作用户')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    
    class Meta:
        verbose_name = '工艺历史'
        verbose_name_plural = '工艺历史'
        ordering = ['-timestamp']
