from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import ProcessCase, ProcessTemplate, ExpertKnowledge, ExperimentData
from .serializers import (
    ProcessCaseSerializer, 
    ProcessTemplateSerializer, 
    ExpertKnowledgeSerializer, 
    ExperimentDataSerializer
)


class ProcessCaseViewSet(viewsets.ModelViewSet):
    """工艺实例视图集"""
    queryset = ProcessCase.objects.all()
    serializer_class = ProcessCaseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'part_material', 'created_by']
    search_fields = ['name', 'description', 'part_material']
    ordering_fields = ['created_at', 'updated_at', 'name']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取工艺实例统计信息"""
        total_cases = self.queryset.count()
        active_cases = self.queryset.filter(status='active').count()
        draft_cases = self.queryset.filter(status='draft').count()
        archived_cases = self.queryset.filter(status='archived').count()
        
        return Response({
            'total_cases': total_cases,
            'active_cases': active_cases,
            'draft_cases': draft_cases,
            'archived_cases': archived_cases,
        })


class ProcessTemplateViewSet(viewsets.ModelViewSet):
    """工序模板视图集"""
    queryset = ProcessTemplate.objects.all()
    serializer_class = ProcessTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['template_type', 'is_active', 'created_by']
    search_fields = ['name', 'description', 'applicable_materials']
    ordering_fields = ['created_at', 'updated_at', 'name']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """按类型获取模板"""
        template_type = request.query_params.get('type')
        if template_type:
            templates = self.queryset.filter(template_type=template_type, is_active=True)
            serializer = self.get_serializer(templates, many=True)
            return Response(serializer.data)
        
        return Response({'error': '请提供template_type参数'}, status=status.HTTP_400_BAD_REQUEST)


class ExpertKnowledgeViewSet(viewsets.ModelViewSet):
    """专家知识库视图集"""
    queryset = ExpertKnowledge.objects.all()
    serializer_class = ExpertKnowledgeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['knowledge_type', 'is_published', 'expert_name']
    search_fields = ['title', 'content', 'keywords', 'expert_name']
    ordering_fields = ['created_at', 'updated_at', 'view_count']
    ordering = ['-view_count', '-created_at']
    
    def retrieve(self, request, *args, **kwargs):
        """获取知识详情，增加查看次数"""
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """获取热门知识"""
        popular_knowledge = self.queryset.filter(is_published=True).order_by('-view_count')[:10]
        serializer = self.get_serializer(popular_knowledge, many=True)
        return Response(serializer.data)


class ExperimentDataViewSet(viewsets.ModelViewSet):
    """试验数据视图集"""
    queryset = ExperimentData.objects.all()
    serializer_class = ExperimentDataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'test_material', 'experimenter']
    search_fields = ['experiment_name', 'experiment_purpose', 'test_material']
    ordering_fields = ['created_at', 'updated_at', 'start_date', 'end_date']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'])
    def start_experiment(self, request, pk=None):
        """开始试验"""
        experiment = self.get_object()
        if experiment.status == 'planned':
            experiment.status = 'in_progress'
            experiment.save()
            return Response({'message': '试验已开始'})
        
        return Response({'error': '只有计划中的试验才能开始'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def complete_experiment(self, request, pk=None):
        """完成试验"""
        experiment = self.get_object()
        if experiment.status == 'in_progress':
            experiment.status = 'completed'
            experiment.save()
            return Response({'message': '试验已完成'})
        
        return Response({'error': '只有进行中的试验才能完成'}, status=status.HTTP_400_BAD_REQUEST)
