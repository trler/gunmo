from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone
from .models import PolishingRequirement, RequirementComment, RequirementAttachment, RequirementTemplate
from .serializers import (
    PolishingRequirementSerializer, RequirementCommentSerializer,
    RequirementAttachmentSerializer, RequirementTemplateSerializer
)
import uuid


class PolishingRequirementViewSet(viewsets.ModelViewSet):
    queryset = PolishingRequirement.objects.all()
    serializer_class = PolishingRequirementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'urgency_level', 'requester', 'reviewer']
    search_fields = ['title', 'description', 'part_name', 'part_number', 'material']
    ordering_fields = ['created_at', 'updated_at', 'required_completion_date']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        # 自动生成需求编号
        requirement_id = f"REQ-{timezone.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        serializer.save(
            requester=self.request.user,
            requirement_id=requirement_id
        )

    @action(detail=False, methods=['get'])
    def my_requirements(self, request):
        """获取当前用户的需求"""
        queryset = self.queryset.filter(requester=request.user)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending_review(self, request):
        """获取待审核的需求"""
        queryset = self.queryset.filter(status='submitted')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit_for_review(self, request, pk=None):
        """提交审核"""
        requirement = self.get_object()
        if requirement.requester != request.user:
            return Response({'error': '只能提交自己的需求'}, status=status.HTTP_403_FORBIDDEN)
        
        requirement.status = 'submitted'
        requirement.save()
        return Response({'message': '需求已提交审核'})

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """审核需求"""
        requirement = self.get_object()
        action = request.data.get('action')  # 'approve' or 'reject'
        comments = request.data.get('comments', '')
        
        if action == 'approve':
            requirement.status = 'approved'
        elif action == 'reject':
            requirement.status = 'rejected'
        else:
            return Response({'error': '无效的审核操作'}, status=status.HTTP_400_BAD_REQUEST)
        
        requirement.reviewer = request.user
        requirement.reviewed_at = timezone.now()
        requirement.save()
        
        # 添加审核评论
        if comments:
            RequirementComment.objects.create(
                requirement=requirement,
                author=request.user,
                content=comments,
                is_internal=True
            )
        
        return Response({'message': f'需求已{requirement.get_status_display()}'})

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """统计信息"""
        total = self.queryset.count()
        by_status = self.queryset.values('status').annotate(count=Count('status'))
        by_urgency = self.queryset.values('urgency_level').annotate(count=Count('urgency_level'))
        
        return Response({
            'total': total,
            'by_status': list(by_status),
            'by_urgency': list(by_urgency),
        })


class RequirementCommentViewSet(viewsets.ModelViewSet):
    queryset = RequirementComment.objects.all()
    serializer_class = RequirementCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RequirementAttachmentViewSet(viewsets.ModelViewSet):
    queryset = RequirementAttachment.objects.all()
    serializer_class = RequirementAttachmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class RequirementTemplateViewSet(viewsets.ModelViewSet):
    queryset = RequirementTemplate.objects.all()
    serializer_class = RequirementTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['template_name', 'description']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
