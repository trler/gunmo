from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg
from django.utils import timezone
from .models import (
    PolishingProcess, ProcessStep, ProcessReview,
    ProcessAttachment, ProcessUsageRecord
)
from .serializers import (
    PolishingProcessSerializer, ProcessStepSerializer, ProcessReviewSerializer,
    ProcessAttachmentSerializer, ProcessUsageRecordSerializer
)
import uuid


class PolishingProcessViewSet(viewsets.ModelViewSet):
    queryset = PolishingProcess.objects.all()
    serializer_class = PolishingProcessSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'process_type', 'is_standard', 'created_by']
    search_fields = ['process_name', 'description', 'abrasive_type']
    ordering_fields = ['created_at', 'updated_at', 'process_name']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        # 自动生成工艺编号
        process_id = f"PROC-{timezone.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        serializer.save(
            created_by=self.request.user,
            process_id=process_id
        )

    @action(detail=False, methods=['get'])
    def my_processes(self, request):
        """获取当前用户创建的工艺"""
        queryset = self.queryset.filter(created_by=request.user)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def standard_processes(self, request):
        """获取标准工艺"""
        queryset = self.queryset.filter(is_standard=True, status='published')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit_for_review(self, request, pk=None):
        """提交审核"""
        process = self.get_object()
        if process.created_by != request.user:
            return Response({'error': '只能提交自己创建的工艺'}, status=status.HTTP_403_FORBIDDEN)
        
        process.status = 'pending_review'
        process.save()
        return Response({'message': '工艺已提交审核'})

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """统计信息"""
        total = self.queryset.count()
        by_status = self.queryset.values('status').annotate(count=Count('status'))
        by_type = self.queryset.values('process_type').annotate(count=Count('process_type'))
        
        return Response({
            'total': total,
            'by_status': list(by_status),
            'by_type': list(by_type),
        })


class ProcessStepViewSet(viewsets.ModelViewSet):
    queryset = ProcessStep.objects.all()
    serializer_class = ProcessStepSerializer
    permission_classes = [IsAuthenticated]


class ProcessReviewViewSet(viewsets.ModelViewSet):
    queryset = ProcessReview.objects.all()
    serializer_class = ProcessReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class ProcessAttachmentViewSet(viewsets.ModelViewSet):
    queryset = ProcessAttachment.objects.all()
    serializer_class = ProcessAttachmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class ProcessUsageRecordViewSet(viewsets.ModelViewSet):
    queryset = ProcessUsageRecord.objects.all()
    serializer_class = ProcessUsageRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(used_by=self.request.user)
