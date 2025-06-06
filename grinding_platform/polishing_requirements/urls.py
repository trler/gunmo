from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PolishingRequirementViewSet, RequirementCommentViewSet,
    RequirementAttachmentViewSet, RequirementTemplateViewSet
)

router = DefaultRouter()
router.register(r'requirements', PolishingRequirementViewSet)
router.register(r'comments', RequirementCommentViewSet)
router.register(r'attachments', RequirementAttachmentViewSet)
router.register(r'templates', RequirementTemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 