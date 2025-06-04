from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
import os
import json
import shutil
from datetime import datetime
import subprocess
from .models import SystemSettings, SystemBackup, SystemLog
from .serializers import (
    SystemSettingsSerializer,
    SystemBackupSerializer,
    SystemLogSerializer,
    SystemSettingsUpdateSerializer,
    BackupCreateSerializer,
    BackupRestoreSerializer
)

class IsSystemAdmin(permissions.BasePermission):
    """系统管理员权限"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'system_admin'

class SystemSettingsViewSet(viewsets.ModelViewSet):
    """系统设置视图集"""
    queryset = SystemSettings.objects.all()
    serializer_class = SystemSettingsSerializer
    permission_classes = [IsSystemAdmin]
    http_method_names = ['get', 'put', 'patch']

    def get_queryset(self):
        """获取设置列表"""
        return SystemSettings.objects.all()

    @action(detail=False, methods=['get'])
    def all_settings(self, request):
        """获取所有设置"""
        settings_data = {
            'basic': self._get_settings_by_prefix('basic_'),
            'security': self._get_settings_by_prefix('security_'),
            'notification': self._get_settings_by_prefix('notification_'),
            'backup': self._get_settings_by_prefix('backup_')
        }
        return Response(settings_data)

    def _get_settings_by_prefix(self, prefix):
        """根据前缀获取设置"""
        settings = {}
        for setting in self.queryset.filter(key__startswith=prefix):
            key = setting.key[len(prefix):]
            settings[key] = setting.value
        return settings

    @action(detail=False, methods=['put'])
    def update_settings(self, request):
        """更新设置"""
        serializer = SystemSettingsUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 更新基本设置
            if 'basic' in serializer.validated_data:
                for key, value in serializer.validated_data['basic'].items():
                    SystemSettings.set_setting(f'basic_{key}', value)

            # 更新安全设置
            if 'security' in serializer.validated_data:
                for key, value in serializer.validated_data['security'].items():
                    SystemSettings.set_setting(f'security_{key}', value)

            # 更新通知设置
            if 'notification' in serializer.validated_data:
                for key, value in serializer.validated_data['notification'].items():
                    SystemSettings.set_setting(f'notification_{key}', value)

            # 更新备份设置
            if 'backup' in serializer.validated_data:
                for key, value in serializer.validated_data['backup'].items():
                    SystemSettings.set_setting(f'backup_{key}', value)

            # 记录日志
            SystemLog.log(
                level='info',
                message='系统设置已更新',
                module='system_settings',
                user=request.user,
                ip_address=request.META.get('REMOTE_ADDR'),
                metadata={'updated_settings': serializer.validated_data}
            )

            return Response({'message': '设置更新成功'})
        except Exception as e:
            SystemLog.log(
                level='error',
                message=f'更新系统设置失败: {str(e)}',
                module='system_settings',
                user=request.user,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return Response(
                {'error': '更新设置失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SystemBackupViewSet(viewsets.ModelViewSet):
    """系统备份视图集"""
    queryset = SystemBackup.objects.all()
    serializer_class = SystemBackupSerializer
    permission_classes = [IsSystemAdmin]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        """获取备份列表"""
        return SystemBackup.objects.all().order_by('-created_at')

    @action(detail=False, methods=['post'])
    def create_backup(self, request):
        """创建备份"""
        serializer = BackupCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 生成备份文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_type = serializer.validated_data['backup_type']
            filename = f'backup_{backup_type}_{timestamp}.zip'

            # 创建备份目录
            backup_dir = os.path.join(settings.MEDIA_ROOT, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            backup_path = os.path.join(backup_dir, filename)

            # 执行备份
            if serializer.validated_data['include_database']:
                self._backup_database(backup_path)

            if serializer.validated_data['include_files']:
                self._backup_files(backup_path)

            if serializer.validated_data['include_settings']:
                self._backup_settings(backup_path)

            # 创建备份记录
            backup = SystemBackup.objects.create(
                filename=filename,
                file_path=f'backups/{filename}',
                backup_type=backup_type,
                created_by=request.user,
                description=serializer.validated_data.get('description', ''),
                is_auto=False
            )

            # 记录日志
            SystemLog.log(
                level='info',
                message=f'创建系统备份: {filename}',
                module='system_backup',
                user=request.user,
                ip_address=request.META.get('REMOTE_ADDR'),
                metadata=serializer.validated_data
            )

            return Response(
                self.get_serializer(backup).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            SystemLog.log(
                level='error',
                message=f'创建备份失败: {str(e)}',
                module='system_backup',
                user=request.user,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return Response(
                {'error': '创建备份失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def restore_backup(self, request, pk=None):
        """恢复备份"""
        backup = self.get_object()
        serializer = BackupRestoreSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            if serializer.validated_data['restore_database']:
                self._restore_database(backup.file_path.path)

            if serializer.validated_data['restore_files']:
                self._restore_files(backup.file_path.path)

            if serializer.validated_data['restore_settings']:
                self._restore_settings(backup.file_path.path)

            # 记录日志
            SystemLog.log(
                level='info',
                message=f'恢复系统备份: {backup.filename}',
                module='system_backup',
                user=request.user,
                ip_address=request.META.get('REMOTE_ADDR'),
                metadata=serializer.validated_data
            )

            return Response({'message': '备份恢复成功'})
        except Exception as e:
            SystemLog.log(
                level='error',
                message=f'恢复备份失败: {str(e)}',
                module='system_backup',
                user=request.user,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return Response(
                {'error': '恢复备份失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _backup_database(self, backup_path):
        """备份数据库"""
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings['PORT']

        # 使用 mysqldump 备份数据库
        dump_file = f'{backup_path}.sql'
        command = [
            'mysqldump',
            f'--user={db_user}',
            f'--password={db_password}',
            f'--host={db_host}',
            f'--port={db_port}',
            db_name,
            f'--result-file={dump_file}'
        ]
        subprocess.run(command, check=True)

    def _backup_files(self, backup_path):
        """备份文件"""
        # 备份媒体文件
        media_dir = settings.MEDIA_ROOT
        shutil.make_archive(backup_path, 'zip', media_dir)

    def _backup_settings(self, backup_path):
        """备份设置"""
        settings_data = {
            'system_settings': list(SystemSettings.objects.values()),
            'timestamp': timezone.now().isoformat()
        }
        settings_file = f'{backup_path}_settings.json'
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings_data, f, ensure_ascii=False, indent=2)

    def _restore_database(self, backup_path):
        """恢复数据库"""
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings['PORT']

        # 从备份文件恢复数据库
        dump_file = f'{backup_path}.sql'
        command = [
            'mysql',
            f'--user={db_user}',
            f'--password={db_password}',
            f'--host={db_host}',
            f'--port={db_port}',
            db_name,
            f'< {dump_file}'
        ]
        subprocess.run(command, shell=True, check=True)

    def _restore_files(self, backup_path):
        """恢复文件"""
        # 恢复媒体文件
        media_dir = settings.MEDIA_ROOT
        shutil.unpack_archive(f'{backup_path}.zip', media_dir, 'zip')

    def _restore_settings(self, backup_path):
        """恢复设置"""
        settings_file = f'{backup_path}_settings.json'
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings_data = json.load(f)

        # 恢复系统设置
        SystemSettings.objects.all().delete()
        for setting in settings_data['system_settings']:
            SystemSettings.objects.create(**setting)

class SystemLogViewSet(viewsets.ReadOnlyModelViewSet):
    """系统日志视图集"""
    queryset = SystemLog.objects.all()
    serializer_class = SystemLogSerializer
    permission_classes = [IsSystemAdmin]
    filterset_fields = ['level', 'module', 'user', 'created_at']
    search_fields = ['message', 'module']
    ordering_fields = ['created_at', 'level']
    ordering = ['-created_at']

    def get_queryset(self):
        """获取日志列表"""
        queryset = SystemLog.objects.all()
        
        # 按时间范围过滤
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
            
        return queryset
