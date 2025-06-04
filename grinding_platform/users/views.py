from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from .models import CustomUser, UserProfile
from .serializers import (
    UserRegistrationSerializer, 
    UserProfileSerializer, 
    UserSerializer,
    CustomTokenObtainPairSerializer
)

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    """用户注册 - 处理滚磨光整加工行业用户注册"""
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # 自动创建用户配置文件
        UserProfile.objects.get_or_create(user=user)
        
        return Response({
            'message': '用户注册成功',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class CustomTokenObtainPairView(TokenObtainPairView):
    """自定义JWT登录视图 - 返回包含用户信息的JWT token"""
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    """用户配置文件"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

class UserLogoutView(generics.GenericAPIView):
    """用户登出"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "需要提供refresh token"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "成功登出"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"登出失败: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class UserDetailView(generics.RetrieveUpdateAPIView):
    """用户详情和更新视图"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': '用户信息更新成功',
            'user': serializer.data
        })

# 兼容性视图（保持原有的登录接口）
class UserLoginView(generics.GenericAPIView):
    """用户登录 - 兼容性接口"""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                # 使用自定义序列化器生成token
                serializer = CustomTokenObtainPairSerializer()
                token = serializer.get_token(user)
                
                return Response({
                    'refresh': str(token),
                    'access': str(token.access_token),
                    'user': UserSerializer(user).data
                })
        
        return Response(
            {'error': '用户名或密码错误'},
            status=status.HTTP_401_UNAUTHORIZED
        )

class ChangePasswordView(generics.GenericAPIView):
    """修改密码"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # 验证输入
        if not all([old_password, new_password, confirm_password]):
            return Response(
                {"error": "所有字段都是必需的"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 验证旧密码
        if not user.check_password(old_password):
            return Response(
                {"error": "旧密码不正确"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 验证新密码确认
        if new_password != confirm_password:
            return Response(
                {"error": "新密码与确认密码不匹配"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 验证新密码长度
        if len(new_password) < 6:
            return Response(
                {"error": "新密码长度至少为6个字符"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 设置新密码
        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "密码修改成功"}, 
            status=status.HTTP_200_OK
        )
