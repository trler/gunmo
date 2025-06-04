# equipment/serializers.py
from rest_framework import serializers
from .models import Equipment, EquipmentType, EquipmentMaintenance, EquipmentAlert

class EquipmentTypeSerializer(serializers.ModelSerializer):
    """设备类型序列化器"""
    class Meta:
        model = EquipmentType
        fields = '__all__'

class EquipmentSerializer(serializers.ModelSerializer):
    """设备序列化器"""
    equipment_type_name = serializers.CharField(source='equipment_type.name', read_only=True)
    responsible_person_name = serializers.CharField(source='responsible_person.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Equipment
        fields = [
            'id', 'name', 'code', 'equipment_type', 'equipment_type_name',
            'model', 'manufacturer', 'serial_number', 'status', 'status_display',
            'priority', 'location', 'workshop', 'specifications', 'max_speed',
            'max_pressure', 'power_rating', 'purchase_date', 'warranty_expiry',
            'last_maintenance', 'next_maintenance', 'total_runtime', 'total_cycles',
            'responsible_person', 'responsible_person_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class EquipmentMaintenanceSerializer(serializers.ModelSerializer):
    """设备维护序列化器"""
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    performed_by_name = serializers.CharField(source='performed_by.username', read_only=True)

    class Meta:
        model = EquipmentMaintenance
        fields = [
            'id', 'equipment', 'equipment_name', 'maintenance_type',
            'description', 'performed_by', 'performed_by_name',
            'start_time', 'end_time', 'cost', 'notes'
        ]
        read_only_fields = ['id']

class EquipmentAlertSerializer(serializers.ModelSerializer):
    """设备警告序列化器"""
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    resolved_by_name = serializers.CharField(source='resolved_by.username', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)

    class Meta:
        model = EquipmentAlert
        fields = [
            'id', 'equipment', 'equipment_name', 'level', 'level_display',
            'title', 'message', 'is_resolved', 'resolved_by', 'resolved_by_name',
            'resolved_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at'] 