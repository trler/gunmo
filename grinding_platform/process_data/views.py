from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ProcessData
from .serializers import ProcessDataSerializer

# Create your views here.

class ProcessDataListView(generics.ListAPIView):
    """工艺数据列表"""
    queryset = ProcessData.objects.all()
    serializer_class = ProcessDataSerializer
    permission_classes = [IsAuthenticated]

class ProcessDataCreateView(generics.CreateAPIView):
    """创建工艺数据"""
    queryset = ProcessData.objects.all()
    serializer_class = ProcessDataSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ProcessDataDetailView(generics.RetrieveAPIView):
    """工艺数据详情"""
    queryset = ProcessData.objects.all()
    serializer_class = ProcessDataSerializer
    permission_classes = [IsAuthenticated]

class ProcessDataUpdateView(generics.UpdateAPIView):
    """更新工艺数据"""
    queryset = ProcessData.objects.all()
    serializer_class = ProcessDataSerializer
    permission_classes = [IsAuthenticated]

class ProcessDataDeleteView(generics.DestroyAPIView):
    """删除工艺数据"""
    queryset = ProcessData.objects.all()
    serializer_class = ProcessDataSerializer
    permission_classes = [IsAuthenticated]
