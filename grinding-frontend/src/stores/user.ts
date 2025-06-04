import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, UserProfile, AuthError } from '@/types/auth'
import type { User as SystemUser, UserCreateData, UserUpdateData, UserListResponse, UserListParams, UserRole, UserStatus } from '@/types/user'
import { useAuth } from '@/composables/useAuth'
import axiosInstance from '@/api/axios'
import type { AxiosError } from 'axios'

export const useUserStore = defineStore('user', () => {
  const { user, isAuthenticated } = useAuth()
  const loading = ref(false)
  const error = ref<string | null>(null)
  const userProfile = ref<UserProfile | null>(null)

  // 获取用户信息
  const fetchUserInfo = async () => {
    try {
      loading.value = true
      error.value = null
      
      const response = await axiosInstance.get<User>('/users/me/')
      return response.data
    } catch (err: unknown) {
      const axiosError = err as AxiosError<AuthError>
      console.error('获取用户信息失败:', axiosError)
      error.value = axiosError.response?.data?.detail || '获取用户信息失败'
      throw axiosError
    } finally {
      loading.value = false
    }
  }

  // 获取用户配置文件
  const fetchUserProfile = async () => {
    try {
      loading.value = true
      error.value = null
      
      const response = await axiosInstance.get<UserProfile>('/users/me/profile/')
      userProfile.value = response.data
      return response.data
    } catch (err: unknown) {
      const axiosError = err as AxiosError<AuthError>
      console.error('获取用户配置文件失败:', axiosError)
      error.value = axiosError.response?.data?.detail || '获取用户配置文件失败'
      throw axiosError
    } finally {
      loading.value = false
    }
  }

  // 获取仪表板数据
  const fetchDashboardData = async () => {
    try {
      loading.value = true
      error.value = null
      
      // 并行请求设备和工艺数据
      const [equipmentResponse, processDataResponse] = await Promise.all([
        axiosInstance.get('/equipment/'),
        axiosInstance.get('/process-data/')
      ])
      
      return {
        equipment: equipmentResponse.data.results || equipmentResponse.data || [],
        processData: processDataResponse.data.results || processDataResponse.data || []
      }
    } catch (err: any) {
      console.error('获取仪表板数据失败:', err)
      error.value = err.response?.data?.detail || '获取仪表板数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 更新用户资料
  const updateProfile = async (data: Partial<User>) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await axiosInstance.patch('/users/me/profile/', data)
      return response.data
    } catch (err: any) {
      console.error('更新用户资料失败:', err)
      error.value = err.response?.data?.detail || '更新用户资料失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 更新用户配置文件（别名方法，兼容ProfileView.vue）
  const updateUserProfile = async (data: Partial<UserProfile>) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await axiosInstance.patch('/users/me/profile/', data)
      userProfile.value = response.data
      return response.data
    } catch (err: any) {
      console.error('更新用户配置文件失败:', err)
      error.value = err.response?.data?.detail || '更新用户配置文件失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 修改密码
  const changePassword = async (data: { old_password: string; new_password: string }) => {
    try {
      loading.value = true
      error.value = null
      
      await axiosInstance.post('/users/me/change-password/', data)
    } catch (err: any) {
      console.error('修改密码失败:', err)
      error.value = err.response?.data?.detail || '修改密码失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 用户管理相关方法
  const fetchUsers = async (params: UserListParams): Promise<UserListResponse> => {
    try {
      loading.value = true
      error.value = null
      const response = await axiosInstance.get<UserListResponse>('/users/', { params })
      return response.data
    } catch (err: any) {
      console.error('获取用户列表失败:', err)
      error.value = err.response?.data?.detail || '获取用户列表失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const createUser = async (data: UserCreateData): Promise<SystemUser> => {
    try {
      loading.value = true
      error.value = null
      const response = await axiosInstance.post<SystemUser>('/users/', data)
      return response.data
    } catch (err: any) {
      console.error('创建用户失败:', err)
      error.value = err.response?.data?.detail || '创建用户失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateUser = async (userId: number, data: UserUpdateData): Promise<SystemUser> => {
    try {
      loading.value = true
      error.value = null
      const response = await axiosInstance.patch<SystemUser>(`/users/${userId}/`, data)
      return response.data
    } catch (err: any) {
      console.error('更新用户失败:', err)
      error.value = err.response?.data?.detail || '更新用户失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteUser = async (userId: number): Promise<void> => {
    try {
      loading.value = true
      error.value = null
      await axiosInstance.delete(`/users/${userId}/`)
    } catch (err: any) {
      console.error('删除用户失败:', err)
      error.value = err.response?.data?.detail || '删除用户失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateUserStatus = async (userId: number, status: UserStatus): Promise<SystemUser> => {
    try {
      loading.value = true
      error.value = null
      const response = await axiosInstance.patch<SystemUser>(`/users/${userId}/status/`, { status })
      return response.data
    } catch (err: any) {
      console.error('更新用户状态失败:', err)
      error.value = err.response?.data?.detail || '更新用户状态失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const resetUserPassword = async (userId: number, newPassword: string): Promise<void> => {
    try {
      loading.value = true
      error.value = null
      await axiosInstance.post(`/users/${userId}/reset-password/`, { password: newPassword })
    } catch (err: any) {
      console.error('重置密码失败:', err)
      error.value = err.response?.data?.detail || '重置密码失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    isAuthenticated,
    loading,
    error,
    userProfile,
    fetchUserInfo,
    fetchUserProfile,
    fetchDashboardData,
    updateProfile,
    updateUserProfile,
    changePassword,
    // 用户管理方法
    fetchUsers,
    createUser,
    updateUser,
    deleteUser,
    updateUserStatus,
    resetUserPassword
  }
}) 