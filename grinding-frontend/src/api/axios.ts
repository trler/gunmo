import axios from 'axios';
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import router from '@/router';

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// 创建axios实例
const axiosInstance: AxiosInstance = axios.create({
  baseURL: baseURL + '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
axiosInstance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 从 localStorage 获取 token
    const auth = localStorage.getItem('auth');
    if (auth) {
      try {
        const { token } = JSON.parse(auth);
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        }
      } catch (error) {
        console.error('解析认证信息失败:', error);
      }
    }
    return config;
  },
  (error: AxiosError) => {
    console.error('请求拦截器错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      // 清除认证信息
      localStorage.removeItem('auth');
      localStorage.removeItem('refresh_token');
      
      // 重定向到登录页
      router.push('/login');
    }
    return Promise.reject(error);
  }
);

export default axiosInstance; 