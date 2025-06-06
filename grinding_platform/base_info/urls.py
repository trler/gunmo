from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'personnel', views.PersonnelViewSet)
router.register(r'standards', views.StandardViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 