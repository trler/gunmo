from django.db import models
from django.conf import settings

class PolishingRequirement(models.Model):
    """光整需求模型"""
    REQUIREMENT_STATUS_CHOICES = [
        ('draft', '草稿'),
        ('submitted', '已提交'),
        ('under_review', '审核中'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
    ]
    
    URGENCY_LEVEL_CHOICES = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
        ('urgent', '紧急'),
    ]

    # 基本信息
    requirement_id = models.CharField(max_length=50, unique=True, verbose_name='需求编号')
    title = models.CharField(max_length=200, verbose_name='需求标题')
    description = models.TextField(verbose_name='需求描述')
    
    # 零件信息
    part_name = models.CharField(max_length=100, verbose_name='零件名称')
    part_number = models.CharField(max_length=50, verbose_name='零件编号')
    material = models.CharField(max_length=100, verbose_name='材料')
    quantity = models.IntegerField(verbose_name='数量')
    
    # 光整要求
    surface_roughness_before = models.FloatField(null=True, blank=True, verbose_name='初始表面粗糙度(μm)')
    surface_roughness_after = models.FloatField(null=True, blank=True, verbose_name='目标表面粗糙度(μm)')
    dimensional_tolerance = models.CharField(max_length=100, blank=True, verbose_name='尺寸公差')
    geometric_tolerance = models.CharField(max_length=100, blank=True, verbose_name='几何公差')
    
    # 特殊要求
    special_requirements = models.TextField(blank=True, verbose_name='特殊要求')
    technical_drawings = models.FileField(upload_to='requirements/drawings/', null=True, blank=True, verbose_name='技术图纸')
    
    # 状态和优先级
    status = models.CharField(max_length=20, choices=REQUIREMENT_STATUS_CHOICES, default='draft', verbose_name='状态')
    urgency_level = models.CharField(max_length=10, choices=URGENCY_LEVEL_CHOICES, default='medium', verbose_name='紧急程度')
    
    # 时间要求
    required_completion_date = models.DateField(null=True, blank=True, verbose_name='要求完成日期')
    
    # 用户关联
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='polishing_requirements', verbose_name='需求提出者')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_requirements', verbose_name='审核人')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='审核时间')
    
    class Meta:
        db_table = 'polishing_requirements'
        verbose_name = '光整需求'
        verbose_name_plural = '光整需求'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.requirement_id} - {self.title}"


class RequirementComment(models.Model):
    """需求评论模型"""
    requirement = models.ForeignKey(PolishingRequirement, on_delete=models.CASCADE, related_name='comments', verbose_name='关联需求')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='评论者')
    content = models.TextField(verbose_name='评论内容')
    is_internal = models.BooleanField(default=False, verbose_name='内部评论')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'requirement_comments'
        verbose_name = '需求评论'
        verbose_name_plural = '需求评论'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.requirement.requirement_id} - {self.author.username}"


class RequirementAttachment(models.Model):
    """需求附件模型"""
    requirement = models.ForeignKey(PolishingRequirement, on_delete=models.CASCADE, related_name='attachments', verbose_name='关联需求')
    file = models.FileField(upload_to='requirements/attachments/', verbose_name='附件文件')
    file_name = models.CharField(max_length=255, verbose_name='文件名')
    file_size = models.IntegerField(verbose_name='文件大小(字节)')
    file_type = models.CharField(max_length=50, verbose_name='文件类型')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='上传者')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    
    class Meta:
        db_table = 'requirement_attachments'
        verbose_name = '需求附件'
        verbose_name_plural = '需求附件'

    def __str__(self):
        return f"{self.requirement.requirement_id} - {self.file_name}"


class RequirementTemplate(models.Model):
    """需求模板模型"""
    template_name = models.CharField(max_length=100, verbose_name='模板名称')
    description = models.TextField(blank=True, verbose_name='模板描述')
    template_data = models.JSONField(verbose_name='模板数据')
    category = models.CharField(max_length=50, verbose_name='模板分类')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='创建者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'requirement_templates'
        verbose_name = '需求模板'
        verbose_name_plural = '需求模板'
        ordering = ['category', 'template_name']

    def __str__(self):
        return f"{self.category} - {self.template_name}"
