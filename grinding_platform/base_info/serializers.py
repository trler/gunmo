from rest_framework import serializers
from .models import Company, Department, Personnel, Standard


class CompanySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by')
        
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class DepartmentSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    parent_department_name = serializers.CharField(source='parent_department.name', read_only=True)
    manager_name = serializers.CharField(source='manager.username', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by')
        
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class PersonnelSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Personnel
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by')
        
    def get_age(self, obj):
        from datetime import date
        if obj.birth_date:
            today = date.today()
            return today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
        return None
        
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class StandardSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Standard
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by')
        
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data) 