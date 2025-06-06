from django.db import models
from django.conf import settings

class PolishingProcess(models.Model):
    """光整工艺模型"""
    PROCESS_STATUS_CHOICES = [
        ('draft', '草稿'),
        ('pending_review', '待审核'),
        ('under_review', '审核中'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
        ('published', '已发布'),
        ('archived', '已归档'),
    ]
    
    PROCESS_TYPE_CHOICES = [
        ('wet', '湿式光整'),
        ('dry', '干式光整'),
        ('compound', '复合光整'),
        ('custom', '自定义工艺'),
    ]

    # 基本信息
    process_id = models.CharField(max_length=50, unique=True, verbose_name='工艺编号')
    process_name = models.CharField(max_length=200, verbose_name='工艺名称')
    process_type = models.CharField(max_length=20, choices=PROCESS_TYPE_CHOICES, verbose_name='工艺类型')
    description = models.TextField(blank=True, verbose_name='工艺描述')
    
    # 适用范围
    applicable_materials = models.JSONField(default=list, verbose_name='适用材料')
    applicable_part_types = models.JSONField(default=list, verbose_name='适用零件类型')
    
    # 工艺参数
    processing_time = models.FloatField(null=True, blank=True, verbose_name='加工时间(分钟)')
    rotation_speed = models.FloatField(null=True, blank=True, verbose_name='转速(rpm)')
    vibration_frequency = models.FloatField(null=True, blank=True, verbose_name='振动频率(Hz)')
    liquid_ratio = models.CharField(max_length=100, blank=True, verbose_name='液体配比')
    temperature = models.FloatField(null=True, blank=True, verbose_name='温度(°C)')
    
    # 磨料信息
    abrasive_type = models.CharField(max_length=100, blank=True, verbose_name='磨料类型')
    abrasive_size = models.CharField(max_length=50, blank=True, verbose_name='磨料粒度')
    abrasive_quantity = models.FloatField(null=True, blank=True, verbose_name='磨料用量(kg)')
    
    # 化学剂信息
    chemical_agents = models.JSONField(default=list, verbose_name='化学剂配方')
    
    # 质量控制
    quality_criteria = models.JSONField(default=dict, verbose_name='质量标准')
    expected_surface_roughness = models.FloatField(null=True, blank=True, verbose_name='预期表面粗糙度(μm)')
    
    # 安全注意事项
    safety_precautions = models.TextField(blank=True, verbose_name='安全注意事项')
    environmental_requirements = models.TextField(blank=True, verbose_name='环境要求')
    
    # 成本信息
    material_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='材料成本')
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='人工成本')
    equipment_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='设备成本')
    
    # 状态管理
    status = models.CharField(max_length=20, choices=PROCESS_STATUS_CHOICES, default='draft', verbose_name='状态')
    version = models.CharField(max_length=10, default='1.0', verbose_name='版本号')
    is_standard = models.BooleanField(default=False, verbose_name='是否为标准工艺')
    
    # 用户关联
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_processes', verbose_name='创建者')
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_processes', verbose_name='审核人')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_processes', verbose_name='批准人')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='审核时间')
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name='批准时间')
    
    class Meta:
        db_table = 'polishing_processes'
        verbose_name = '光整工艺'
        verbose_name_plural = '光整工艺'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.process_id} - {self.process_name}"


class ProcessStep(models.Model):
    """工艺步骤模型"""
    process = models.ForeignKey(PolishingProcess, on_delete=models.CASCADE, related_name='steps', verbose_name='关联工艺')
    step_number = models.IntegerField(verbose_name='步骤序号')
    step_name = models.CharField(max_length=100, verbose_name='步骤名称')
    description = models.TextField(verbose_name='步骤描述')
    duration = models.FloatField(null=True, blank=True, verbose_name='持续时间(分钟)')
    parameters = models.JSONField(default=dict, verbose_name='步骤参数')
    quality_checkpoints = models.JSONField(default=list, verbose_name='质量检查点')
    notes = models.TextField(blank=True, verbose_name='备注')
    
    class Meta:
        db_table = 'process_steps'
        verbose_name = '工艺步骤'
        verbose_name_plural = '工艺步骤'
        ordering = ['process', 'step_number']
        unique_together = ['process', 'step_number']

    def __str__(self):
        return f"{self.process.process_name} - 步骤{self.step_number}"


class ProcessReview(models.Model):
    """工艺审核记录模型"""
    REVIEW_STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '通过'),
        ('rejected', '拒绝'),
        ('needs_revision', '需要修改'),
    ]

    process = models.ForeignKey(PolishingProcess, on_delete=models.CASCADE, related_name='reviews', verbose_name='关联工艺')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='审核人')
    review_status = models.CharField(max_length=20, choices=REVIEW_STATUS_CHOICES, verbose_name='审核状态')
    comments = models.TextField(blank=True, verbose_name='审核意见')
    technical_score = models.IntegerField(null=True, blank=True, verbose_name='技术评分(1-10)')
    safety_score = models.IntegerField(null=True, blank=True, verbose_name='安全评分(1-10)')
    cost_score = models.IntegerField(null=True, blank=True, verbose_name='成本评分(1-10)')
    overall_score = models.FloatField(null=True, blank=True, verbose_name='综合评分')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='审核时间')
    
    class Meta:
        db_table = 'process_reviews'
        verbose_name = '工艺审核记录'
        verbose_name_plural = '工艺审核记录'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.process.process_name} - {self.reviewer.username}"


class ProcessAttachment(models.Model):
    """工艺附件模型"""
    ATTACHMENT_TYPE_CHOICES = [
        ('image', '图片'),
        ('document', '文档'),
        ('video', '视频'),
        ('drawing', '图纸'),
        ('other', '其他'),
    ]

    process = models.ForeignKey(PolishingProcess, on_delete=models.CASCADE, related_name='attachments', verbose_name='关联工艺')
    file = models.FileField(upload_to='processes/attachments/', verbose_name='附件文件')
    file_name = models.CharField(max_length=255, verbose_name='文件名')
    file_type = models.CharField(max_length=20, choices=ATTACHMENT_TYPE_CHOICES, verbose_name='文件类型')
    file_size = models.IntegerField(verbose_name='文件大小(字节)')
    description = models.TextField(blank=True, verbose_name='描述')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='上传者')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    
    class Meta:
        db_table = 'process_attachments'
        verbose_name = '工艺附件'
        verbose_name_plural = '工艺附件'

    def __str__(self):
        return f"{self.process.process_name} - {self.file_name}"


class ProcessUsageRecord(models.Model):
    """工艺使用记录模型"""
    process = models.ForeignKey(PolishingProcess, on_delete=models.CASCADE, related_name='usage_records', verbose_name='使用的工艺')
    used_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='使用者')
    part_name = models.CharField(max_length=100, verbose_name='零件名称')
    part_number = models.CharField(max_length=50, verbose_name='零件编号')
    quantity = models.IntegerField(verbose_name='加工数量')
    actual_processing_time = models.FloatField(null=True, blank=True, verbose_name='实际加工时间(分钟)')
    actual_surface_roughness = models.FloatField(null=True, blank=True, verbose_name='实际表面粗糙度(μm)')
    quality_rating = models.IntegerField(null=True, blank=True, verbose_name='质量评分(1-10)')
    notes = models.TextField(blank=True, verbose_name='使用备注')
    
    # 成本记录
    actual_material_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='实际材料成本')
    actual_labor_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='实际人工成本')
    
    used_at = models.DateTimeField(auto_now_add=True, verbose_name='使用时间')
    
    class Meta:
        db_table = 'process_usage_records'
        verbose_name = '工艺使用记录'
        verbose_name_plural = '工艺使用记录'
        ordering = ['-used_at']

    def __str__(self):
        return f"{self.process.process_name} - {self.part_name} - {self.used_at.strftime('%Y-%m-%d')}"
