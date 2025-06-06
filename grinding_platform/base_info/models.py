from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Company(models.Model):
    """企业信息数据库"""
    
    COMPANY_TYPE_CHOICES = [
        ('manufacturer', '制造商'),
        ('supplier', '供应商'),
        ('research', '科研机构'),
        ('service', '服务商'),
        ('other', '其他'),
    ]
    
    SCALE_CHOICES = [
        ('large', '大型企业'),
        ('medium', '中型企业'),
        ('small', '小型企业'),
        ('micro', '微型企业'),
    ]
    
    # 基本信息
    code = models.CharField(max_length=50, unique=True, verbose_name='企业编号')
    name = models.CharField(max_length=200, verbose_name='企业名称')
    short_name = models.CharField(max_length=100, blank=True, verbose_name='企业简称')
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES, verbose_name='企业类型')
    
    # 注册信息
    unified_social_code = models.CharField(max_length=50, unique=True, verbose_name='统一社会信用代码')
    legal_representative = models.CharField(max_length=50, verbose_name='法定代表人')
    registered_capital = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='注册资本(万元)')
    establishment_date = models.DateField(verbose_name='成立日期')
    scale = models.CharField(max_length=20, choices=SCALE_CHOICES, verbose_name='企业规模')
    
    # 联系信息
    address = models.TextField(verbose_name='企业地址')
    postal_code = models.CharField(max_length=10, blank=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    fax = models.CharField(max_length=20, blank=True, verbose_name='传真号码')
    email = models.EmailField(blank=True, verbose_name='企业邮箱')
    website = models.URLField(blank=True, verbose_name='企业网站')
    
    # 业务信息
    business_scope = models.TextField(verbose_name='经营范围')
    main_products = models.TextField(verbose_name='主要产品')
    industry_category = models.CharField(max_length=100, verbose_name='行业类别')
    
    # 资质信息
    certifications = models.TextField(blank=True, verbose_name='企业资质')
    quality_system = models.CharField(max_length=100, blank=True, verbose_name='质量管理体系')
    
    # 状态信息
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    remarks = models.TextField(blank=True, verbose_name='备注信息')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_companies', verbose_name='创建人')
    
    class Meta:
        verbose_name = '企业信息'
        verbose_name_plural = '企业信息'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Department(models.Model):
    """部门信息数据库"""
    
    DEPARTMENT_TYPE_CHOICES = [
        ('production', '生产部门'),
        ('technology', '技术部门'),
        ('quality', '质量部门'),
        ('management', '管理部门'),
        ('sales', '销售部门'),
        ('finance', '财务部门'),
        ('hr', '人力资源'),
        ('logistics', '物流部门'),
        ('other', '其他'),
    ]
    
    # 基本信息
    code = models.CharField(max_length=50, unique=True, verbose_name='部门编号')
    name = models.CharField(max_length=100, verbose_name='部门名称')
    department_type = models.CharField(max_length=20, choices=DEPARTMENT_TYPE_CHOICES, verbose_name='部门类型')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='所属企业')
    parent_department = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='上级部门')
    
    # 部门信息
    level = models.PositiveIntegerField(default=1, verbose_name='部门层级')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_departments', verbose_name='部门负责人')
    description = models.TextField(blank=True, verbose_name='部门描述')
    responsibilities = models.TextField(blank=True, verbose_name='主要职责')
    
    # 联系信息
    office_location = models.CharField(max_length=200, blank=True, verbose_name='办公地点')
    extension = models.CharField(max_length=20, blank=True, verbose_name='分机号码')
    email = models.EmailField(blank=True, verbose_name='部门邮箱')
    
    # 状态信息
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    establishment_date = models.DateField(blank=True, null=True, verbose_name='成立日期')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_departments', verbose_name='创建人')
    
    class Meta:
        verbose_name = '部门信息'
        verbose_name_plural = '部门信息'
        ordering = ['company', 'level', 'code']
    
    def __str__(self):
        return f"{self.company.short_name or self.company.name} - {self.name}"


class Personnel(models.Model):
    """人员信息数据库"""
    
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]
    
    EDUCATION_CHOICES = [
        ('primary', '小学'),
        ('junior', '初中'),
        ('senior', '高中'),
        ('college', '大专'),
        ('bachelor', '本科'),
        ('master', '硕士'),
        ('doctor', '博士'),
    ]
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('fulltime', '全职'),
        ('parttime', '兼职'),
        ('contract', '合同工'),
        ('intern', '实习生'),
        ('consultant', '顾问'),
    ]
    
    STATUS_CHOICES = [
        ('active', '在职'),
        ('leave', '请假'),
        ('resigned', '离职'),
        ('retired', '退休'),
    ]
    
    # 基本信息
    employee_id = models.CharField(max_length=50, unique=True, verbose_name='员工编号')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='关联用户')
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='性别')
    birth_date = models.DateField(verbose_name='出生日期')
    id_card = models.CharField(max_length=20, unique=True, verbose_name='身份证号')
    
    # 组织信息
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='所属企业')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属部门')
    position = models.CharField(max_length=100, verbose_name='职位')
    job_level = models.CharField(max_length=50, blank=True, verbose_name='职级')
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, verbose_name='用工类型')
    
    # 入职信息
    hire_date = models.DateField(verbose_name='入职日期')
    contract_start = models.DateField(verbose_name='合同开始日期')
    contract_end = models.DateField(blank=True, null=True, verbose_name='合同结束日期')
    probation_end = models.DateField(blank=True, null=True, verbose_name='试用期结束日期')
    
    # 教育背景
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, verbose_name='学历')
    major = models.CharField(max_length=100, blank=True, verbose_name='专业')
    graduate_school = models.CharField(max_length=200, blank=True, verbose_name='毕业院校')
    graduation_date = models.DateField(blank=True, null=True, verbose_name='毕业时间')
    
    # 联系信息
    phone = models.CharField(max_length=20, verbose_name='手机号码')
    email = models.EmailField(blank=True, verbose_name='邮箱地址')
    address = models.TextField(blank=True, verbose_name='家庭地址')
    emergency_contact = models.CharField(max_length=50, blank=True, verbose_name='紧急联系人')
    emergency_phone = models.CharField(max_length=20, blank=True, verbose_name='紧急联系电话')
    
    # 工作信息
    skills = models.TextField(blank=True, verbose_name='技能特长')
    certifications = models.TextField(blank=True, verbose_name='职业资格证书')
    work_experience = models.TextField(blank=True, verbose_name='工作经历')
    
    # 状态信息
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='状态')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_personnel', verbose_name='创建人')
    
    class Meta:
        verbose_name = '人员信息'
        verbose_name_plural = '人员信息'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee_id} - {self.name}"


class Standard(models.Model):
    """标准规范数据库"""
    
    STANDARD_TYPE_CHOICES = [
        ('national', '国家标准'),
        ('industry', '行业标准'),
        ('local', '地方标准'),
        ('enterprise', '企业标准'),
        ('international', '国际标准'),
        ('group', '团体标准'),
    ]
    
    STATUS_CHOICES = [
        ('draft', '草案'),
        ('current', '现行'),
        ('abolished', '废止'),
        ('replaced', '被替代'),
        ('revised', '修订中'),
    ]
    
    # 基本信息
    standard_code = models.CharField(max_length=100, unique=True, verbose_name='标准编号')
    title = models.CharField(max_length=500, verbose_name='标准名称')
    english_title = models.CharField(max_length=500, blank=True, verbose_name='英文名称')
    standard_type = models.CharField(max_length=20, choices=STANDARD_TYPE_CHOICES, verbose_name='标准类型')
    
    # 发布信息
    publisher = models.CharField(max_length=200, verbose_name='发布机构')
    publish_date = models.DateField(verbose_name='发布日期')
    implement_date = models.DateField(verbose_name='实施日期')
    revision_date = models.DateField(blank=True, null=True, verbose_name='修订日期')
    
    # 内容信息
    scope = models.TextField(verbose_name='适用范围')
    abstract = models.TextField(verbose_name='标准摘要')
    keywords = models.TextField(blank=True, verbose_name='关键词')
    classification = models.CharField(max_length=100, verbose_name='标准分类')
    
    # 关联信息
    replaced_standards = models.TextField(blank=True, verbose_name='替代标准')
    referenced_standards = models.TextField(blank=True, verbose_name='引用标准')
    related_standards = models.TextField(blank=True, verbose_name='相关标准')
    
    # 文档信息
    file_url = models.URLField(blank=True, verbose_name='文档链接')
    page_count = models.PositiveIntegerField(blank=True, null=True, verbose_name='页数')
    language = models.CharField(max_length=50, default='中文', verbose_name='语言')
    
    # 状态信息
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='current', verbose_name='状态')
    is_mandatory = models.BooleanField(default=False, verbose_name='是否强制性标准')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_standards', verbose_name='创建人')
    
    class Meta:
        verbose_name = '标准规范'
        verbose_name_plural = '标准规范'
        ordering = ['-publish_date']
    
    def __str__(self):
        return f"{self.standard_code} - {self.title}" 