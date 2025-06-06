from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import GrindingBlock, BlockHistory
from .serializers import GrindingBlockSerializer, BlockHistorySerializer

# Create your views here.

class IsProcessEngineerOrFullstack(permissions.BasePermission):
    """工艺工程师或全栈工程师权限"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.user_type in ['process_engineer', 'fullstack_engineer']
        )

class GrindingBlockViewSet(viewsets.ModelViewSet):
    """磨块信息视图集"""
    queryset = GrindingBlock.objects.all()
    serializer_class = GrindingBlockSerializer
    permission_classes = [IsProcessEngineerOrFullstack]
    
    def get_queryset(self):
        """自定义查询集"""
        queryset = super().get_queryset()
        
        # 搜索功能
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(block_no__icontains=search) |
                Q(block_name__icontains=search) |
                Q(block_type__icontains=search) |
                Q(block_brand__icontains=search) |
                Q(block_factory__icontains=search)
            )
        
        # 按类型筛选
        block_type = self.request.query_params.get('block_type')
        if block_type:
            queryset = queryset.filter(block_type=block_type)
        
        # 按厂家筛选
        factory = self.request.query_params.get('factory')
        if factory:
            queryset = queryset.filter(block_factory=factory)
        
        return queryset
    
    def perform_create(self, serializer):
        """创建时记录创建者"""
        instance = serializer.save(created_by=self.request.user)
        # 记录历史
        BlockHistory.objects.create(
            block=instance,
            action='create',
            changes={'created': True},
            user=self.request.user
        )
    
    def perform_update(self, serializer):
        """更新时记录变更"""
        old_instance = self.get_object()
        instance = serializer.save()
        # 记录历史
        changes = {
            field: {
                'old': getattr(old_instance, field),
                'new': getattr(instance, field)
            }
            for field in serializer.validated_data.keys()
            if getattr(old_instance, field) != getattr(instance, field)
        }
        if changes:
            BlockHistory.objects.create(
                block=instance,
                action='update',
                changes=changes,
                user=self.request.user
            )
    
    def perform_destroy(self, instance):
        """删除时记录历史"""
        BlockHistory.objects.create(
            block=instance,
            action='delete',
            changes={'deleted': True},
            user=self.request.user
        )
        instance.delete()
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """获取磨块历史记录"""
        block = self.get_object()
        history = block.history.all()
        serializer = BlockHistorySerializer(history, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def block_types(self, request):
        """获取所有磨块类型"""
        types = GrindingBlock.objects.values_list('block_type', flat=True).distinct()
        return Response(list(types))
    
    @action(detail=False, methods=['get'])
    def factories(self, request):
        """获取所有磨块厂家"""
        factories = GrindingBlock.objects.values_list('block_factory', flat=True).distinct()
        return Response(list(factories))
