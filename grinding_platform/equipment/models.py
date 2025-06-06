from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class EquipmentType(models.Model):
    """设备类型"""
    name = models.CharField(max_length=100, unique=True, verbose_name='设备类型')
    description = models.TextField(blank=True, verbose_name='描述')
    
    class Meta:
        verbose_name = '设备类型'
        verbose_name_plural = '设备类型'
        
    def __str__(self):
        return self.name

class Equipment(models.Model):
    """设备信息"""
    STATUS_CHOICES = [
        ('running', '运行中'),
        ('idle', '空闲'),
        ('maintenance', '维护中'),
        ('error', '故障'),
        ('offline', '离线'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
        ('critical', '紧急'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='设备名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='设备编号')
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE, verbose_name='设备类型')
    model = models.CharField(max_length=100, verbose_name='设备型号')
    manufacturer = models.CharField(max_length=100, verbose_name='制造商')
    serial_number = models.CharField(max_length=100, blank=True, verbose_name='序列号')
    
    # 状态信息
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline', verbose_name='状态')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name='优先级')
    
    # 位置信息
    location = models.CharField(max_length=200, verbose_name='位置')
    workshop = models.CharField(max_length=100, verbose_name='车间')
    
    # 技术参数
    specifications = models.JSONField(default=dict, verbose_name='技术规格')
    max_speed = models.FloatField(null=True, blank=True, verbose_name='最大转速 (rpm)')
    max_pressure = models.FloatField(null=True, blank=True, verbose_name='最大压力 (bar)')
    power_rating = models.FloatField(null=True, blank=True, verbose_name='额定功率 (kW)')
    
    # 购买和维护信息
    purchase_date = models.DateField(null=True, blank=True, verbose_name='购买日期')
    warranty_expiry = models.DateField(null=True, blank=True, verbose_name='保修到期')
    last_maintenance = models.DateTimeField(null=True, blank=True, verbose_name='上次维护时间')
    next_maintenance = models.DateTimeField(null=True, blank=True, verbose_name='下次维护时间')
    
    # 使用统计
    total_runtime = models.FloatField(default=0, verbose_name='总运行时间 (小时)')
    total_cycles = models.IntegerField(default=0, verbose_name='总运行周期')
    
    # 管理信息
    responsible_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='负责人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '设备'
        verbose_name_plural = '设备'
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.code})"

class EquipmentMaintenance(models.Model):
    """设备维护记录"""
    MAINTENANCE_TYPES = [
        ('routine', '例行维护'),
        ('preventive', '预防性维护'),
        ('corrective', '修正性维护'),
        ('emergency', '紧急维护'),
    ]
    
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenance_records')
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPES, verbose_name='维护类型')
    description = models.TextField(verbose_name='维护描述')
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='执行人')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='维护成本')
    notes = models.TextField(blank=True, verbose_name='备注')
    
    class Meta:
        verbose_name = '维护记录'
        verbose_name_plural = '维护记录'
        ordering = ['-start_time']
        
    def __str__(self):
        return f"{self.equipment.name} - {self.get_maintenance_type_display()}"

class EquipmentAlert(models.Model):
    """设备警告"""
    ALERT_LEVELS = [
        ('info', '信息'),
        ('warning', '警告'),
        ('error', '错误'),
        ('critical', '严重'),
    ]
    
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='alerts')
    level = models.CharField(max_length=10, choices=ALERT_LEVELS, verbose_name='警告级别')
    title = models.CharField(max_length=200, verbose_name='标题')
    message = models.TextField(verbose_name='警告信息')
    is_resolved = models.BooleanField(default=False, verbose_name='已解决')
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='解决人')
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name='解决时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '设备警告'
        verbose_name_plural = '设备警告'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.equipment.name} - {self.title}"

class Chemical(models.Model):
    """化学剂信息"""
    SAFETY_LEVEL_CHOICES = [
        ('low', '低风险'),
        ('medium', '中风险'),
        ('high', '高风险'),
    ]

    TYPE_CHOICES = [
        ('cutting_fluid', '切削液'),
        ('cleaning_agent', '清洗剂'),
        ('rust_preventive', '防锈剂'),
        ('lubricant', '润滑剂'),
        ('passivator', '钝化剂'),
    ]

    code = models.CharField(max_length=50, unique=True, verbose_name='化学剂编号')
    name = models.CharField(max_length=200, verbose_name='化学剂名称')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='类型')
    manufacturer = models.CharField(max_length=200, verbose_name='生产厂家')
    components = models.TextField(verbose_name='主要成分')
    ph_range = models.CharField(max_length=50, verbose_name='PH值范围')
    density = models.FloatField(verbose_name='密度(g/cm³)')
    flash_point = models.CharField(max_length=50, verbose_name='闪点(℃)')
    safety_level = models.CharField(max_length=10, choices=SAFETY_LEVEL_CHOICES, default='low', verbose_name='安全等级')
    expiry_date = models.DateField(verbose_name='有效期')
    msds_file = models.FileField(upload_to='chemicals/msds/', null=True, blank=True, verbose_name='MSDS文件')
    formula_file = models.FileField(upload_to='chemicals/formulas/', null=True, blank=True, verbose_name='配方文件')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '化学剂'
        verbose_name_plural = '化学剂'
        ordering = ['code']

    def __str__(self):
        return f"{self.name} ({self.code})"
