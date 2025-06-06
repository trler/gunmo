from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class GrindingBlock(models.Model):
    """磨块信息模型"""
    
    # 基本信息
    block_no = models.CharField(max_length=50, unique=True, verbose_name='磨块编号')
    block_name = models.CharField(max_length=100, verbose_name='磨块名称')
    block_type = models.CharField(max_length=50, verbose_name='磨块类型')
    block_brand = models.CharField(max_length=50, verbose_name='磨块牌号')
    block_factory = models.CharField(max_length=100, verbose_name='磨块厂家')
    
    # 物理特性
    block_shape = models.CharField(max_length=50, verbose_name='磨块形状')
    block_spec = models.CharField(max_length=100, verbose_name='磨块规格')
    block_material = models.CharField(max_length=50, verbose_name='磨块材质')
    block_color = models.CharField(max_length=50, verbose_name='磨块颜色')
    weight = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='重量(g)'
    )
    
    # 性能参数
    wear_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='磨耗率(%)'
    )
    grinding_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='磨削率(%)'
    )
    
    # 其他信息
    batch = models.CharField(max_length=50, blank=True, verbose_name='批次')
    feature1 = models.CharField(max_length=200, blank=True, verbose_name='特征信息1')
    feature2 = models.CharField(max_length=200, blank=True, verbose_name='特征信息2')
    remark = models.TextField(blank=True, verbose_name='备注')
    
    # 图片
    images = models.JSONField(default=list, blank=True, verbose_name='图片列表')
    
    # 管理信息
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_blocks',
        verbose_name='创建者'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '磨块信息'
        verbose_name_plural = '磨块信息'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['block_no']),
            models.Index(fields=['block_type']),
            models.Index(fields=['block_factory']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.block_name} ({self.block_no})"

class BlockHistory(models.Model):
    """磨块信息历史记录"""
    ACTION_CHOICES = [
        ('create', '创建'),
        ('update', '更新'),
        ('delete', '删除'),
    ]
    
    block = models.ForeignKey(
        GrindingBlock,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name='磨块'
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name='操作类型'
    )
    changes = models.JSONField(default=dict, verbose_name='变更内容')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='操作用户'
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    
    class Meta:
        verbose_name = '磨块历史'
        verbose_name_plural = '磨块历史'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.block.block_name} - {self.get_action_display()} ({self.timestamp})"
