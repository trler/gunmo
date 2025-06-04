import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import type { LoginCredentials, RegisterCredentials, AuthError } from '@/types/auth';
import type { AxiosError } from 'axios';

interface AuthOptions {
  redirectTo?: string;
  onSuccess?: () => void;
  onError?: (error: AuthError) => void;
}

export function useAuth() {
  const router = useRouter();
  const authStore = useAuthStore();

  const user = computed(() => authStore.user);
  const token = computed(() => authStore.token);
  const loading = computed(() => authStore.loading);
  const error = computed(() => authStore.error);
  const isAuthenticated = computed(() => authStore.isAuthenticated);

  const login = async (credentials: LoginCredentials, options: AuthOptions = {}) => {
    const { redirectTo = '/', onSuccess, onError } = options;
    try {
      await authStore.login(credentials);
      if (onSuccess) {
        onSuccess();
      }
      router.push(redirectTo);
    } catch (err: unknown) {
      const error = err as AxiosError<AuthError>;
      if (onError) {
        onError({
          message: error.response?.data?.detail || '登录失败',
          code: error.response?.data?.code
        });
      }
      throw error;
    }
  };

  const register = async (credentials: RegisterCredentials, options: AuthOptions = {}) => {
    const { redirectTo = '/dashboard', onSuccess, onError } = options;
    try {
      await authStore.register(credentials);
      if (onSuccess) {
        onSuccess();
      }
      router.push(redirectTo);
    } catch (err: any) {
      if (onError) {
        onError(err);
      }
      throw err;
    }
  };

  const logout = async (options: AuthOptions = {}) => {
    const { redirectTo = '/login', onSuccess, onError } = options;
    try {
      await authStore.logout();
      if (onSuccess) {
        onSuccess();
      }
      router.push(redirectTo);
    } catch (err: any) {
      if (onError) {
        onError(err);
      }
      throw err;
    }
  };

  const fetchUserInfo = async () => {
    try {
      return await authStore.fetchUserInfo();
    } catch (err: any) {
      throw err;
    }
  };

  return {
    // 状态
    user,
    token,
    loading,
    error,
    isAuthenticated,
    
    // 方法
    login,
    register,
    logout,
    fetchUserInfo,
  };
} 