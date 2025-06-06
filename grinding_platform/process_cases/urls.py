from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cases', views.ProcessCaseViewSet)
router.register(r'templates', views.ProcessTemplateViewSet)
router.register(r'knowledge', views.ExpertKnowledgeViewSet)
router.register(r'experiments', views.ExperimentDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 