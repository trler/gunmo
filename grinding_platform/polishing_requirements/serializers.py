from rest_framework import serializers
from .models import PolishingRequirement, RequirementComment, RequirementAttachment, RequirementTemplate


class RequirementCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = RequirementComment
        fields = ['id', 'content', 'is_internal', 'created_at', 'author_name']
        read_only_fields = ['created_at', 'author_name']


class RequirementAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = RequirementAttachment
        fields = ['id', 'file', 'file_name', 'file_size', 'file_type', 
                 'uploaded_by_name', 'uploaded_at']
        read_only_fields = ['uploaded_by_name', 'uploaded_at']


class PolishingRequirementSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(source='requester.username', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    comments = RequirementCommentSerializer(many=True, read_only=True)
    attachments = RequirementAttachmentSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    urgency_level_display = serializers.CharField(source='get_urgency_level_display', read_only=True)
    
    class Meta:
        model = PolishingRequirement
        fields = [
            'id', 'requirement_id', 'title', 'description',
            'part_name', 'part_number', 'material', 'quantity',
            'surface_roughness_before', 'surface_roughness_after',
            'dimensional_tolerance', 'geometric_tolerance',
            'special_requirements', 'technical_drawings',
            'status', 'status_display', 'urgency_level', 'urgency_level_display',
            'required_completion_date', 'requester_name', 'reviewer_name',
            'created_at', 'updated_at', 'reviewed_at',
            'comments', 'attachments'
        ]
        read_only_fields = ['requirement_id', 'requester_name', 'reviewer_name', 
                           'created_at', 'updated_at', 'reviewed_at',
                           'status_display', 'urgency_level_display']


class RequirementTemplateSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = RequirementTemplate
        fields = ['id', 'template_name', 'description', 'template_data',
                 'category', 'is_active', 'created_by_name', 'created_at']
        read_only_fields = ['created_by_name', 'created_at'] 