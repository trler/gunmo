# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from . import views

app_name = 'users'

# 认证相关URL
auth_urlpatterns = [
    # 用户注册
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    
    # JWT认证
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]

# 用户信息相关URL
user_urlpatterns = [
    # 当前用户信息
    path('me/', views.UserDetailView.as_view(), name='me'),
    path('me/profile/', views.UserProfileView.as_view(), name='profile'),
    path('me/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]

# 兼容性URL（可以逐步废弃）
legacy_urlpatterns = [
    path('auth/login/', views.UserLoginView.as_view(), name='auth_login'),
]

# 合并所有URL模式
urlpatterns = auth_urlpatterns + user_urlpatterns + legacy_urlpatterns 