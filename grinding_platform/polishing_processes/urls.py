from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PolishingProcessViewSet, ProcessStepViewSet, ProcessReviewViewSet,
    ProcessAttachmentViewSet, ProcessUsageRecordViewSet
)

router = DefaultRouter()
router.register(r'processes', PolishingProcessViewSet)
router.register(r'steps', ProcessStepViewSet)
router.register(r'reviews', ProcessReviewViewSet)
router.register(r'attachments', ProcessAttachmentViewSet)
router.register(r'usage-records', ProcessUsageRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 