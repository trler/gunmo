from rest_framework import serializers
from .models import ProcessData, ProcessCategory, ProcessHistory

class ProcessCategorySerializer(serializers.ModelSerializer):
    """工艺类别序列化器"""
    class Meta:
        model = ProcessCategory
        fields = '__all__'

class ProcessDataSerializer(serializers.ModelSerializer):
    """工艺数据序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = ProcessData
        fields = [
            'id', 'name', 'category', 'category_name', 'description', 
            'parameters', 'status', 'grinding_speed', 'pressure', 
            'temperature', 'processing_time', 'created_by', 
            'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

class ProcessHistorySerializer(serializers.ModelSerializer):
    """工艺历史序列化器"""
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ProcessHistory
        fields = ['id', 'process_data', 'action', 'changes', 'user', 'user_name', 'timestamp']
        read_only_fields = ['id', 'user', 'timestamp'] 