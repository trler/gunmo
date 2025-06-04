from rest_framework import serializers
from .models import SystemSettings, SystemBackup, SystemLog
from users.serializers import UserSerializer

class SystemSettingsSerializer(serializers.ModelSerializer):
    """系统设置序列化器"""
    class Meta:
        model = SystemSettings
        fields = ['key', 'value', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class SystemBackupSerializer(serializers.ModelSerializer):
    """系统备份序列化器"""
    created_by = UserSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()
    size_display = serializers.SerializerMethodField()

    class Meta:
        model = SystemBackup
        fields = [
            'id', 'filename', 'file_path', 'file_url', 'backup_type',
            'size', 'size_display', 'created_at', 'created_by',
            'description', 'is_auto'
        ]
        read_only_fields = ['id', 'created_at', 'size']

    def get_file_url(self, obj):
        """获取文件URL"""
        if obj.file_path:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file_path.url)
        return None

    def get_size_display(self, obj):
        """格式化文件大小显示"""
        if obj.size is None:
            return '0 B'
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if obj.size < 1024.0:
                return f"{obj.size:.1f} {unit}"
            obj.size /= 1024.0
        return f"{obj.size:.1f} PB"

class SystemLogSerializer(serializers.ModelSerializer):
    """系统日志序列化器"""
    user = UserSerializer(read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)

    class Meta:
        model = SystemLog
        fields = [
            'id', 'level', 'level_display', 'message', 'module',
            'user', 'ip_address', 'created_at', 'metadata'
        ]
        read_only_fields = ['id', 'created_at']

class SystemSettingsUpdateSerializer(serializers.Serializer):
    """系统设置更新序列化器"""
    basic = serializers.JSONField(required=False)
    security = serializers.JSONField(required=False)
    notification = serializers.JSONField(required=False)
    backup = serializers.JSONField(required=False)

    def validate_basic(self, value):
        """验证基本设置"""
        required_fields = ['systemName', 'theme']
        for field in required_fields:
            if field not in value:
                raise serializers.ValidationError(f'缺少必要字段: {field}')
        return value

    def validate_security(self, value):
        """验证安全设置"""
        required_fields = ['passwordPolicy', 'minPasswordLength', 'sessionTimeout']
        for field in required_fields:
            if field not in value:
                raise serializers.ValidationError(f'缺少必要字段: {field}')
        return value

    def validate_notification(self, value):
        """验证通知设置"""
        if value.get('emailEnabled'):
            required_fields = ['smtpServer', 'smtpPort', 'senderEmail']
            for field in required_fields:
                if not value.get(field):
                    raise serializers.ValidationError(f'启用邮件通知时，{field} 是必需的')
        return value

    def validate_backup(self, value):
        """验证备份设置"""
        if value.get('autoBackupEnabled'):
            required_fields = ['backupFrequency', 'backupTime', 'backupRetention']
            for field in required_fields:
                if field not in value:
                    raise serializers.ValidationError(f'启用自动备份时，{field} 是必需的')
        return value

class BackupCreateSerializer(serializers.Serializer):
    """创建备份序列化器"""
    backup_type = serializers.ChoiceField(
        choices=SystemBackup.backup_type.field.choices,
        required=True
    )
    description = serializers.CharField(required=False, allow_blank=True)
    include_database = serializers.BooleanField(default=True)
    include_files = serializers.BooleanField(default=True)
    include_settings = serializers.BooleanField(default=True)

class BackupRestoreSerializer(serializers.Serializer):
    """恢复备份序列化器"""
    backup_id = serializers.IntegerField(required=True)
    confirm = serializers.BooleanField(required=True)
    restore_database = serializers.BooleanField(default=True)
    restore_files = serializers.BooleanField(default=True)
    restore_settings = serializers.BooleanField(default=True)

    def validate(self, data):
        """验证恢复确认"""
        if not data['confirm']:
            raise serializers.ValidationError('必须确认恢复操作')
        return data 