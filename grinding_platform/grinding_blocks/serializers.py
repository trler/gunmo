from rest_framework import serializers
from .models import GrindingBlock, BlockHistory
from users.serializers import UserSerializer

class GrindingBlockSerializer(serializers.ModelSerializer):
    """磨块信息序列化器"""
    created_by = UserSerializer(read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = GrindingBlock
        fields = [
            'id', 'block_no', 'block_name', 'block_type', 'block_brand',
            'block_factory', 'block_shape', 'block_spec', 'block_material',
            'block_color', 'weight', 'wear_rate', 'grinding_rate', 'batch',
            'feature1', 'feature2', 'remark', 'images', 'created_by',
            'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

class BlockHistorySerializer(serializers.ModelSerializer):
    """磨块历史记录序列化器"""
    user = UserSerializer(read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    block_name = serializers.CharField(source='block.block_name', read_only=True)
    block_no = serializers.CharField(source='block.block_no', read_only=True)
    
    class Meta:
        model = BlockHistory
        fields = [
            'id', 'block', 'block_name', 'block_no', 'action',
            'action_display', 'changes', 'user', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp'] 