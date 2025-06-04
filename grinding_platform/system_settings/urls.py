from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'settings', views.SystemSettingsViewSet, basename='system-settings')
router.register(r'backups', views.SystemBackupViewSet, basename='system-backups')
router.register(r'logs', views.SystemLogViewSet, basename='system-logs')

urlpatterns = [
    path('', include(router.urls)),
] 