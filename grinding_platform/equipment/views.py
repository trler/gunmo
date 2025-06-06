from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Equipment, Chemical
from .serializers import EquipmentSerializer, ChemicalSerializer

# Create your views here.

class EquipmentListView(generics.ListAPIView):
    """设备列表"""
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]

class EquipmentCreateView(generics.CreateAPIView):
    """创建设备"""
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]

class EquipmentDetailView(generics.RetrieveAPIView):
    """设备详情"""
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]

class EquipmentUpdateView(generics.UpdateAPIView):
    """更新设备"""
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]

class EquipmentDeleteView(generics.DestroyAPIView):
    """删除设备"""
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]

class EquipmentStatusView(generics.GenericAPIView):
    """设备状态管理"""
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        """更新设备状态"""
        try:
            equipment = self.get_object()
            new_status = request.data.get('status')
            if new_status and new_status in dict(Equipment.STATUS_CHOICES):
                equipment.status = new_status
                equipment.save()
                return Response({'message': f'设备状态已更新为: {equipment.get_status_display()}'})
            else:
                return Response({'error': '无效的状态值'}, status=status.HTTP_400_BAD_REQUEST)
        except Equipment.DoesNotExist:
            return Response({'error': '设备不存在'}, status=status.HTTP_404_NOT_FOUND)

class ChemicalListView(generics.ListCreateAPIView):
    """化学剂列表和创建"""
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Chemical.objects.all()
        code = self.request.query_params.get('code', None)
        name = self.request.query_params.get('name', None)
        type = self.request.query_params.get('type', None)
        manufacturer = self.request.query_params.get('manufacturer', None)
        
        if code:
            queryset = queryset.filter(code__icontains=code)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if type:
            queryset = queryset.filter(type=type)
        if manufacturer:
            queryset = queryset.filter(manufacturer__icontains=manufacturer)
            
        return queryset

class ChemicalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """化学剂详情、更新和删除"""
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSerializer
    permission_classes = [IsAuthenticated]
