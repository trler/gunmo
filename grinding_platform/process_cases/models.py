from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProcessCase(models.Model):
    """工艺实例数据模型"""
    
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('active', '启用'),
        ('archived', '归档'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='案例名称')
    description = models.TextField(blank=True, verbose_name='案例描述')
    part_material = models.CharField(max_length=100, verbose_name='零件材质')
    part_size = models.CharField(max_length=100, verbose_name='零件尺寸')
    surface_requirement = models.CharField(max_length=200, verbose_name='表面要求')
    
    # 工艺参数
    grinding_media = models.CharField(max_length=100, verbose_name='研磨介质')
    grinding_compound = models.CharField(max_length=100, verbose_name='研磨剂')
    rotation_speed = models.FloatField(verbose_name='转速(rpm)')
    processing_time = models.FloatField(verbose_name='加工时间(分钟)')
    vibration_frequency = models.FloatField(null=True, blank=True, verbose_name='振动频率(Hz)')
    
    # 结果数据
    surface_roughness_before = models.FloatField(null=True, blank=True, verbose_name='加工前表面粗糙度(Ra)')
    surface_roughness_after = models.FloatField(null=True, blank=True, verbose_name='加工后表面粗糙度(Ra)')
    removal_amount = models.FloatField(null=True, blank=True, verbose_name='去除量(μm)')
    quality_grade = models.CharField(max_length=10, blank=True, verbose_name='质量等级')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '工艺实例'
        verbose_name_plural = '工艺实例'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class ProcessTemplate(models.Model):
    """工序模板模型"""
    
    TEMPLATE_TYPE_CHOICES = [
        ('deburring', '去毛刺'),
        ('polishing', '抛光'),
        ('cleaning', '清洗'),
        ('surface_treatment', '表面处理'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='模板名称')
    template_type = models.CharField(max_length=30, choices=TEMPLATE_TYPE_CHOICES, verbose_name='模板类型')
    description = models.TextField(blank=True, verbose_name='模板描述')
    
    # 标准参数
    standard_media = models.CharField(max_length=100, verbose_name='标准研磨介质')
    standard_compound = models.CharField(max_length=100, verbose_name='标准研磨剂')
    standard_speed = models.FloatField(verbose_name='标准转速(rpm)')
    standard_time = models.FloatField(verbose_name='标准时间(分钟)')
    
    # 适用范围
    applicable_materials = models.TextField(verbose_name='适用材质')
    applicable_sizes = models.TextField(verbose_name='适用尺寸范围')
    
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '工序模板'
        verbose_name_plural = '工序模板'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"


class ExpertKnowledge(models.Model):
    """专家知识库模型"""
    
    KNOWLEDGE_TYPE_CHOICES = [
        ('best_practice', '最佳实践'),
        ('troubleshooting', '故障排除'),
        ('parameter_optimization', '参数优化'),
        ('material_guide', '材质指南'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='知识标题')
    knowledge_type = models.CharField(max_length=30, choices=KNOWLEDGE_TYPE_CHOICES, verbose_name='知识类型')
    content = models.TextField(verbose_name='知识内容')
    keywords = models.CharField(max_length=500, blank=True, verbose_name='关键词')
    
    # 专家信息
    expert_name = models.CharField(max_length=100, verbose_name='专家姓名')
    expert_title = models.CharField(max_length=100, verbose_name='专家职称')
    
    # 适用条件
    applicable_scenarios = models.TextField(verbose_name='适用场景')
    
    is_published = models.BooleanField(default=False, verbose_name='是否发布')
    view_count = models.PositiveIntegerField(default=0, verbose_name='查看次数')
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='录入人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '专家知识'
        verbose_name_plural = '专家知识库'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class ExperimentData(models.Model):
    """试验数据模型"""
    
    EXPERIMENT_STATUS_CHOICES = [
        ('planned', '计划中'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    experiment_name = models.CharField(max_length=200, verbose_name='试验名称')
    experiment_purpose = models.TextField(verbose_name='试验目的')
    experiment_method = models.TextField(verbose_name='试验方法')
    
    # 试验条件
    test_material = models.CharField(max_length=100, verbose_name='试验材料')
    test_parameters = models.JSONField(default=dict, verbose_name='试验参数')
    
    # 试验结果
    test_results = models.JSONField(default=dict, blank=True, verbose_name='试验结果')
    conclusion = models.TextField(blank=True, verbose_name='试验结论')
    
    status = models.CharField(max_length=20, choices=EXPERIMENT_STATUS_CHOICES, default='planned', verbose_name='试验状态')
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    
    experimenter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='试验人员')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '试验数据'
        verbose_name_plural = '试验数据'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.experiment_name
