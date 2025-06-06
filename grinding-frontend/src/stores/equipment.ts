import { defineStore } from 'pinia'
import { ref } from 'vue'
import axiosInstance from '@/api/axios'
import type { AxiosError } from 'axios'

// 错误响应接口
interface ErrorResponse {
  detail: string
}

// 设备状态类型
export type EquipmentStatus = 'running' | 'idle' | 'maintenance' | 'error' | 'offline'

// 设备优先级类型
export type EquipmentPriority = 'low' | 'medium' | 'high' | 'critical'

// 设备信息接口
export interface Equipment {
  id: number
  code: string
  name: string
  equipment_type: number
  equipment_type_name: string
  model: string
  manufacturer: string
  serial_number?: string
  status: EquipmentStatus
  status_display: string
  priority: EquipmentPriority
  location: string
  workshop: string
  specifications: Record<string, any>
  max_speed?: number
  max_pressure?: number
  power_rating?: number
  purchase_date?: string
  warranty_expiry?: string
  last_maintenance?: string
  next_maintenance?: string
  total_runtime: number
  total_cycles: number
  responsible_person?: number
  responsible_person_name?: string
  created_at: string
  updated_at: string
  maintenance_records?: MaintenanceRecord[]
}

// 维护记录类型
export type MaintenanceType = 'routine' | 'preventive' | 'corrective' | 'emergency'

// 维护记录接口
export interface MaintenanceRecord {
  id: number
  equipment: number
  equipment_name: string
  maintenance_type: MaintenanceType
  description: string
  performed_by: number
  performed_by_name: string
  start_time: string
  end_time?: string
  cost?: number
  notes?: string
}

// 设备列表响应接口
export interface EquipmentListResponse {
  count: number
  next: string | null
  previous: string | null
  results: Equipment[]
}

// 设备列表查询参数接口
export interface EquipmentListParams {
  page?: number
  page_size?: number
  equipment_code?: string
  name?: string
  status?: EquipmentStatus
}

export const useEquipmentStore = defineStore('equipment', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 获取设备列表
  const getEquipmentList = async (params: EquipmentListParams): Promise<EquipmentListResponse> => {
    try {
      loading.value = true
      error.value = null
      const response = await axiosInstance.get<EquipmentListResponse>('/equipment/', { params })
      return response.data
    } catch (err) {
      const axiosError = err as AxiosError<ErrorResponse>
      console.error('获取设备列表失败:', axiosError)
      error.value = axiosError.response?.data?.detail || '获取设备列表失败'
      throw axiosError
    } finally {
      loading.value = false
    }
  }

  // 创建设备
  const createEquipment = async (data: Omit<Equipment, 'id'>): Promise<Equipment> => {
    try {
      loading.value = true
      error.value = null
      const response = await axiosInstance.post<Equipment>('/equipment/', data)
      return response.data
    } catch (err) {
      const axiosError = err as AxiosError<ErrorResponse>
      console.error('创建设备失败:', axiosError)
      error.value = axiosError.response?.data?.detail || '创建设备失败'
      throw axiosError
    } finally {
      loading.value = false
    }
  }

  // 更新设备
  const updateEquipment = async (id: number, data: Partial<Equipment>): Promise<Equipment> => {
    try {
      loading.value = true
      error.value = null
      const response = await axiosInstance.patch<Equipment>(`/equipment/${id}/`, data)
      return response.data
    } catch (err) {
      const axiosError = err as AxiosError<ErrorResponse>
      console.error('更新设备失败:', axiosError)
      error.value = axiosError.response?.data?.detail || '更新设备失败'
      throw axiosError
    } finally {
      loading.value = false
    }
  }

  // 删除设备
  const deleteEquipment = async (id: number): Promise<void> => {
    try {
      loading.value = true
      error.value = null
      await axiosInstance.delete(`/equipment/${id}/`)
    } catch (err) {
      const axiosError = err as AxiosError<ErrorResponse>
      console.error('删除设备失败:', axiosError)
      error.value = axiosError.response?.data?.detail || '删除设备失败'
      throw axiosError
    } finally {
      loading.value = false
    }
  }

  // 获取设备维护记录
  const getMaintenanceRecords = async (equipmentId: number): Promise<MaintenanceRecord[]> => {
    try {
      loading.value = true
      error.value = null
      const response = await axiosInstance.get<Equipment>(`/equipment/${equipmentId}/`)
      // 从设备详情中获取维护记录
      return response.data.maintenance_records || []
    } catch (err) {
      const axiosError = err as AxiosError<ErrorResponse>
      console.error('获取维护记录失败:', axiosError)
      error.value = axiosError.response?.data?.detail || '获取维护记录失败'
      throw axiosError
    } finally {
      loading.value = false
    }
  }

  // 添加维护记录
  const addMaintenanceRecord = async (equipmentId: number, data: Omit<MaintenanceRecord, 'id' | 'equipment' | 'equipment_name' | 'performed_by_name'>): Promise<MaintenanceRecord> => {
    try {
      loading.value = true
      error.value = null
      const response = await axiosInstance.post<MaintenanceRecord>(`/equipment/${equipmentId}/maintenance/`, {
        ...data,
        equipment: equipmentId
      })
      return response.data
    } catch (err) {
      const axiosError = err as AxiosError<ErrorResponse>
      console.error('添加维护记录失败:', axiosError)
      error.value = axiosError.response?.data?.detail || '添加维护记录失败'
      throw axiosError
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    getEquipmentList,
    createEquipment,
    updateEquipment,
    deleteEquipment,
    getMaintenanceRecords,
    addMaintenanceRecord
  }
}) 