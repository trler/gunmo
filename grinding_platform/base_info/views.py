from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Company, Department, Personnel, Standard
from .serializers import CompanySerializer, DepartmentSerializer, PersonnelSerializer, StandardSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """企业信息视图集"""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company_type', 'scale', 'is_active']
    search_fields = ['name', 'short_name', 'code', 'unified_social_code']
    ordering_fields = ['created_at', 'name', 'establishment_date']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取企业统计信息"""
        total = self.queryset.count()
        active = self.queryset.filter(is_active=True).count()
        
        # 按类型统计
        type_stats = {}
        for choice in Company.COMPANY_TYPE_CHOICES:
            type_stats[choice[1]] = self.queryset.filter(company_type=choice[0]).count()
            
        # 按规模统计
        scale_stats = {}
        for choice in Company.SCALE_CHOICES:
            scale_stats[choice[1]] = self.queryset.filter(scale=choice[0]).count()
        
        return Response({
            'total': total,
            'active': active,
            'inactive': total - active,
            'type_stats': type_stats,
            'scale_stats': scale_stats
        })


class DepartmentViewSet(viewsets.ModelViewSet):
    """部门信息视图集"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'department_type', 'level', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['created_at', 'name', 'level']
    ordering = ['company', 'level', 'code']

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """获取部门树形结构"""
        company_id = request.query_params.get('company_id')
        if not company_id:
            return Response({'error': '请提供企业ID'}, status=status.HTTP_400_BAD_REQUEST)
            
        departments = self.queryset.filter(company_id=company_id, is_active=True)
        
        def build_tree(parent_id=None):
            children = []
            for dept in departments.filter(parent_department_id=parent_id):
                children.append({
                    'id': dept.id,
                    'code': dept.code,
                    'name': dept.name,
                    'department_type': dept.get_department_type_display(),
                    'level': dept.level,
                    'manager': dept.manager.username if dept.manager else None,
                    'children': build_tree(dept.id)
                })
            return children
            
        return Response(build_tree())


class PersonnelViewSet(viewsets.ModelViewSet):
    """人员信息视图集"""
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'department', 'gender', 'education', 'employment_type', 'status', 'is_active']
    search_fields = ['name', 'employee_id', 'phone', 'position']
    ordering_fields = ['created_at', 'name', 'hire_date']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取人员统计信息"""
        total = self.queryset.count()
        active = self.queryset.filter(status='active').count()
        
        # 按性别统计
        gender_stats = {}
        for choice in Personnel.GENDER_CHOICES:
            gender_stats[choice[1]] = self.queryset.filter(gender=choice[0]).count()
            
        # 按学历统计
        education_stats = {}
        for choice in Personnel.EDUCATION_CHOICES:
            education_stats[choice[1]] = self.queryset.filter(education=choice[0]).count()
            
        # 按状态统计
        status_stats = {}
        for choice in Personnel.STATUS_CHOICES:
            status_stats[choice[1]] = self.queryset.filter(status=choice[0]).count()
        
        return Response({
            'total': total,
            'active': active,
            'gender_stats': gender_stats,
            'education_stats': education_stats,
            'status_stats': status_stats
        })

    @action(detail=False, methods=['get'])
    def by_department(self, request):
        """按部门统计人员"""
        department_id = request.query_params.get('department_id')
        if department_id:
            personnel = self.queryset.filter(department_id=department_id, is_active=True)
        else:
            personnel = self.queryset.filter(is_active=True)
            
        serializer = self.get_serializer(personnel, many=True)
        return Response(serializer.data)


class StandardViewSet(viewsets.ModelViewSet):
    """标准规范视图集"""
    queryset = Standard.objects.all()
    serializer_class = StandardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['standard_type', 'status', 'is_mandatory', 'is_active']
    search_fields = ['title', 'standard_code', 'keywords', 'publisher']
    ordering_fields = ['created_at', 'publish_date', 'implement_date']
    ordering = ['-publish_date']

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取标准统计信息"""
        total = self.queryset.count()
        current = self.queryset.filter(status='current').count()
        mandatory = self.queryset.filter(is_mandatory=True).count()
        
        # 按类型统计
        type_stats = {}
        for choice in Standard.STANDARD_TYPE_CHOICES:
            type_stats[choice[1]] = self.queryset.filter(standard_type=choice[0]).count()
            
        # 按状态统计
        status_stats = {}
        for choice in Standard.STATUS_CHOICES:
            status_stats[choice[1]] = self.queryset.filter(status=choice[0]).count()
        
        return Response({
            'total': total,
            'current': current,
            'mandatory': mandatory,
            'type_stats': type_stats,
            'status_stats': status_stats
        })

    @action(detail=False, methods=['get'])
    def search_by_classification(self, request):
        """按分类搜索标准"""
        classification = request.query_params.get('classification')
        if not classification:
            return Response({'error': '请提供分类名称'}, status=status.HTTP_400_BAD_REQUEST)
            
        standards = self.queryset.filter(
            Q(classification__icontains=classification) | 
            Q(keywords__icontains=classification)
        ).filter(is_active=True)
        
        serializer = self.get_serializer(standards, many=True)
        return Response(serializer.data) 