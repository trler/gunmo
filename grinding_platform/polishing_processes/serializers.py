from rest_framework import serializers
from .models import (
    PolishingProcess, ProcessStep, ProcessReview,
    ProcessAttachment, ProcessUsageRecord
)


class ProcessStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStep
        fields = ['id', 'step_number', 'step_name', 'description', 
                 'duration', 'parameters', 'quality_checkpoints', 'notes']


class ProcessReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    review_status_display = serializers.CharField(source='get_review_status_display', read_only=True)
    
    class Meta:
        model = ProcessReview
        fields = ['id', 'reviewer_name', 'review_status', 'review_status_display',
                 'comments', 'technical_score', 'safety_score', 'cost_score',
                 'overall_score', 'created_at']
        read_only_fields = ['reviewer_name', 'created_at', 'review_status_display']


class ProcessAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    file_type_display = serializers.CharField(source='get_file_type_display', read_only=True)
    
    class Meta:
        model = ProcessAttachment
        fields = ['id', 'file', 'file_name', 'file_type', 'file_type_display',
                 'file_size', 'description', 'uploaded_by_name', 'uploaded_at']
        read_only_fields = ['uploaded_by_name', 'uploaded_at', 'file_type_display']


class ProcessUsageRecordSerializer(serializers.ModelSerializer):
    used_by_name = serializers.CharField(source='used_by.username', read_only=True)
    process_name = serializers.CharField(source='process.process_name', read_only=True)
    
    class Meta:
        model = ProcessUsageRecord
        fields = ['id', 'process_name', 'used_by_name', 'part_name', 'part_number',
                 'quantity', 'actual_processing_time', 'actual_surface_roughness',
                 'quality_rating', 'notes', 'actual_material_cost', 'actual_labor_cost',
                 'used_at']
        read_only_fields = ['used_by_name', 'process_name', 'used_at']


class PolishingProcessSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.username', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    process_type_display = serializers.CharField(source='get_process_type_display', read_only=True)
    
    steps = ProcessStepSerializer(many=True, read_only=True)
    reviews = ProcessReviewSerializer(many=True, read_only=True)
    attachments = ProcessAttachmentSerializer(many=True, read_only=True)
    usage_records = ProcessUsageRecordSerializer(many=True, read_only=True)
    
    # 统计字段
    total_usage_count = serializers.SerializerMethodField()
    average_quality_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = PolishingProcess
        fields = [
            'id', 'process_id', 'process_name', 'process_type', 'process_type_display',
            'description', 'applicable_materials', 'applicable_part_types',
            'processing_time', 'rotation_speed', 'vibration_frequency',
            'liquid_ratio', 'temperature', 'abrasive_type', 'abrasive_size',
            'abrasive_quantity', 'chemical_agents', 'quality_criteria',
            'expected_surface_roughness', 'safety_precautions', 'environmental_requirements',
            'material_cost', 'labor_cost', 'equipment_cost', 'status', 'status_display',
            'version', 'is_standard', 'created_by_name', 'reviewed_by_name',
            'approved_by_name', 'created_at', 'updated_at', 'reviewed_at',
            'approved_at', 'steps', 'reviews', 'attachments', 'usage_records',
            'total_usage_count', 'average_quality_rating'
        ]
        read_only_fields = [
            'process_id', 'created_by_name', 'reviewed_by_name', 'approved_by_name',
            'created_at', 'updated_at', 'reviewed_at', 'approved_at',
            'status_display', 'process_type_display', 'total_usage_count',
            'average_quality_rating'
        ]
    
    def get_total_usage_count(self, obj):
        return obj.usage_records.count()
    
    def get_average_quality_rating(self, obj):
        ratings = obj.usage_records.filter(quality_rating__isnull=False).values_list('quality_rating', flat=True)
        if ratings:
            return sum(ratings) / len(ratings)
        return None 