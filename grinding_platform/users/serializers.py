from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, UserProfile

class UserSerializer(serializers.ModelSerializer):
    """用户序列化器 - 包含所有用户字段"""
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'user_type_display', 'company', 'department', 
            'industry_role', 'phone', 'date_joined', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'date_joined', 'created_at', 'updated_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'password_confirm', 
            'first_name', 'last_name', 'user_type', 'company', 
            'department', 'industry_role', 'phone'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("密码不匹配")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """自定义JWT token序列化器 - 在token中包含用户信息"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # 添加自定义声明到JWT payload
        token['user_type'] = user.user_type
        token['user_type_display'] = user.get_user_type_display()
        token['company'] = user.company
        token['department'] = user.department
        token['industry_role'] = user.industry_role
        token['username'] = user.username
        token['email'] = user.email
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # 添加用户信息到响应中
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'user_type': self.user.user_type,
            'user_type_display': self.user.get_user_type_display(),
            'company': self.user.company,
            'department': self.user.department,
            'industry_role': self.user.industry_role,
        }
        
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    """用户配置文件序列化器"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'avatar', 'bio', 'preferences'] 