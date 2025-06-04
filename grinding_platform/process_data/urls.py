# process_data/urls.py
from django.urls import path
from . import views

app_name = 'process_data'

urlpatterns = [
    path('', views.ProcessDataListView.as_view(), name='list'),
    path('create/', views.ProcessDataCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ProcessDataDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.ProcessDataUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProcessDataDeleteView.as_view(), name='delete'),
] 