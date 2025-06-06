from rest_framework import serializers
from .models import ProcessCase, ProcessTemplate, ExpertKnowledge, ExperimentData


class ProcessCaseSerializer(serializers.ModelSerializer):
    """工艺实例序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ProcessCase
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ProcessTemplateSerializer(serializers.ModelSerializer):
    """工序模板序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    template_type_display = serializers.CharField(source='get_template_type_display', read_only=True)
    
    class Meta:
        model = ProcessTemplate
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ExpertKnowledgeSerializer(serializers.ModelSerializer):
    """专家知识库序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    knowledge_type_display = serializers.CharField(source='get_knowledge_type_display', read_only=True)
    
    class Meta:
        model = ExpertKnowledge
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at', 'view_count')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ExperimentDataSerializer(serializers.ModelSerializer):
    """试验数据序列化器"""
    experimenter_name = serializers.CharField(source='experimenter.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ExperimentData
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def create(self, validated_data):
        if 'experimenter' not in validated_data:
            validated_data['experimenter'] = self.context['request'].user
        return super().create(validated_data) 