# equipment/urls.py
from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    path('', views.EquipmentListView.as_view(), name='list'),
    path('create/', views.EquipmentCreateView.as_view(), name='create'),
    path('<int:pk>/', views.EquipmentDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.EquipmentUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.EquipmentDeleteView.as_view(), name='delete'),
    path('<int:pk>/status/', views.EquipmentStatusView.as_view(), name='status'),
    path('chemicals/', views.ChemicalListView.as_view(), name='chemical-list'),
    path('chemicals/<int:pk>/', views.ChemicalDetailView.as_view(), name='chemical-detail'),
] 