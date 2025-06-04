import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { User, AuthState, LoginCredentials, RegisterCredentials, AuthError } from '@/types/auth';
import axiosInstance from '@/api/axios';
import type { AxiosError } from 'axios';

interface AuthResponse {
  user: User;
  access: string;
  refresh: string;
}

interface ApiError {
  detail?: string;
  code?: string;
  [key: string]: unknown;
}

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const state = ref<AuthState>({
    user: null,
    token: null,
    loading: false,
    error: null
  });

  // 计算属性
  const isAuthenticated = computed(() => !!state.value.token);
  const user = computed(() => state.value.user);
  const token = computed(() => state.value.token);
  const loading = computed(() => state.value.loading);
  const error = computed(() => state.value.error);

  // 从localStorage初始化状态
  const initializeAuth = () => {
    console.log('初始化认证状态');
    const storedAuth = localStorage.getItem('auth');
    if (storedAuth) {
      try {
        const { user: storedUser, token: storedToken } = JSON.parse(storedAuth);
        console.log('从localStorage恢复认证状态:', { 
          hasUser: !!storedUser, 
          hasToken: !!storedToken
        });
        
        state.value.user = storedUser;
        state.value.token = storedToken;
      } catch (error) {
        console.error('解析存储的认证状态失败:', error);
        clearAuth();
      }
    } else {
      console.log('没有找到存储的认证状态');
    }
  };

  // 保存状态到localStorage
  const persistAuth = (data: AuthResponse) => {
    console.log('保存认证信息');
    state.value.token = data.access;
    state.value.user = data.user;
    try {
      localStorage.setItem('auth', JSON.stringify({
        user: data.user,
        token: data.access
      }));
      if (data.refresh) {
        localStorage.setItem('refresh_token', data.refresh);
      }
    } catch (error) {
      console.error('保存认证信息失败:', error);
    }
  };

  // 清除认证状态
  const clearAuth = () => {
    console.log('清除认证信息');
    state.value.token = null;
    state.value.user = null;
    try {
      localStorage.removeItem('auth');
      localStorage.removeItem('refresh_token');
    } catch (error) {
      console.error('清除认证信息失败:', error);
    }
  };

  // 登录
  const login = async (credentials: LoginCredentials) => {
    console.log('尝试登录:', { username: credentials.username });
    state.value.loading = true;
    state.value.error = null;
    try {
      const response = await axiosInstance.post<AuthResponse>('/users/login/', credentials);
      console.log('登录成功');
      persistAuth(response.data);
      return response.data;
    } catch (error) {
      console.error('登录失败:', error);
      const axiosError = error as AxiosError<ApiError>;
      state.value.error = {
        message: axiosError.response?.data?.detail || axiosError.message || '登录失败',
        code: axiosError.response?.data?.code
      };
      clearAuth();
      throw error;
    } finally {
      state.value.loading = false;
    }
  };

  // 注册
  const register = async (credentials: RegisterCredentials) => {
    console.log('尝试注册:', { username: credentials.username, email: credentials.email });
    state.value.loading = true;
    state.value.error = null;
    try {
      const response = await axiosInstance.post<AuthResponse>('/users/register/', credentials);
      console.log('注册成功');
      persistAuth(response.data);
      return response.data;
    } catch (error) {
      console.error('注册失败:', error);
      const axiosError = error as AxiosError<ApiError>;
      state.value.error = {
        message: axiosError.response?.data?.detail || axiosError.message || '注册失败',
        code: axiosError.response?.data?.code
      };
      clearAuth();
      throw error;
    } finally {
      state.value.loading = false;
    }
  };

  // 登出
  const logout = async () => {
    console.log('尝试登出');
    state.value.loading = true;
    state.value.error = null;
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        console.log('没有找到refresh token，直接清除本地状态');
        clearAuth();
        return;
      }

      await axiosInstance.post('/users/logout/', { refresh: refreshToken });
      console.log('登出成功');
      clearAuth();
    } catch (error) {
      console.error('登出失败:', error);
      const axiosError = error as AxiosError<ApiError>;
      state.value.error = {
        message: axiosError.response?.data?.detail || axiosError.message || '登出失败',
        code: axiosError.response?.data?.code
      };
      // 即使登出请求失败，也清除本地状态
      clearAuth();
    } finally {
      state.value.loading = false;
    }
  };

  // 获取用户信息
  const fetchUserInfo = async () => {
    console.log('获取用户信息');
    state.value.loading = true;
    state.value.error = null;
    try {
      const response = await axiosInstance.get<User>('/users/me/');
      console.log('获取用户信息成功');
      state.value.user = response.data;
      return response.data;
    } catch (error) {
      console.error('获取用户信息失败:', error);
      const axiosError = error as AxiosError<ApiError>;
      state.value.error = {
        message: axiosError.response?.data?.detail || axiosError.message || '获取用户信息失败',
        code: axiosError.response?.data?.code
      };
      throw error;
    } finally {
      state.value.loading = false;
    }
  };

  // 初始化
  initializeAuth();

  return {
    // 状态
    user,
    token,
    loading,
    error,
    isAuthenticated,
    
    // 方法
    initializeAuth,
    login,
    register,
    logout,
    fetchUserInfo,
  };
}); 