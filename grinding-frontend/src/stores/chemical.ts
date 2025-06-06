import { defineStore } from 'pinia'
import { ref } from 'vue'
import axiosInstance from '@/api/axios'
import type { AxiosError } from 'axios'

// 错误响应接口
interface ErrorResponse {
  detail: string
}

// 化学剂类型
export type ChemicalType = 'cutting_fluid' | 'cleaning_agent' | 'rust_preventive' | 'lubricant' | 'passivator'

// 安全等级类型
export type SafetyLevel = 'low' | 'medium' | 'high'

// 化学剂信息接口
export interface Chemical {
  id: number
  code: string
  name: string
  type: ChemicalType
  type_display: string
  manufacturer: string
  components: string
  ph_range: string
  density: number
  flash_point: string
  safety_level: SafetyLevel
  safety_level_display: string
  expiry_date: string
  msds_file?: string
  msds_file_url?: string
  formula_file?: string
  formula_file_url?: string
  remark?: string
  created_at: string
  updated_at: string
}

// 化学剂列表响应接口
export interface ChemicalListResponse {
  count: number
  next: string | null
  previous: string | null
  results: Chemical[]
}

// 化学剂列表查询参数接口
export interface ChemicalListParams {
  page?: number
  page_size?: number
  code?: string
  name?: string
  type?: ChemicalType | ''  // 允许空字符串
  manufacturer?: string
}

export const useChemicalStore = defineStore('chemical', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 获取化学剂列表
  const getChemicalList = async (params: ChemicalListParams): Promise<ChemicalListResponse> => {
    try {
      loading.value = true
      error.value = null
      const response = await axiosInstance.get<ChemicalListResponse>('/equipment/chemicals/', { params })
      return response.data
    } catch (err) {
      const axiosError = err as AxiosError<ErrorResponse>
      console.error('获取化学剂列表失败:', axiosError)
      error.value = axiosError.response?.data?.detail || '获取化学剂列表失败'
      throw axiosError
    } finally {
      loading.value = false
    }
  }

  // 创建化学剂
  const createChemical = async (data: FormData): Promise<Chemical> => {
    try {
      loading.value = true
      error.value = null
      const response = await axiosInstance.post<Chemical>('/equipment/chemicals/', data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (err) {
      const axiosError = err as AxiosError<ErrorResponse>
      console.error('创建化学剂失败:', axiosError)
      error.value = axiosError.response?.data?.detail || '创建化学剂失败'
      throw axiosError
    } finally {
      loading.value = false
    }
  }

  // 更新化学剂
  const updateChemical = async (id: number, data: FormData): Promise<Chemical> => {
    try {
      loading.value = true
      error.value = null
      const response = await axiosInstance.patch<Chemical>(`/equipment/chemicals/${id}/`, data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (err) {
      const axiosError = err as AxiosError<ErrorResponse>
      console.error('更新化学剂失败:', axiosError)
      error.value = axiosError.response?.data?.detail || '更新化学剂失败'
      throw axiosError
    } finally {
      loading.value = false
    }
  }

  // 删除化学剂
  const deleteChemical = async (id: number): Promise<void> => {
    try {
      loading.value = true
      error.value = null
      await axiosInstance.delete(`/equipment/chemicals/${id}/`)
    } catch (err) {
      const axiosError = err as AxiosError<ErrorResponse>
      console.error('删除化学剂失败:', axiosError)
      error.value = axiosError.response?.data?.detail || '删除化学剂失败'
      throw axiosError
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    getChemicalList,
    createChemical,
    updateChemical,
    deleteChemical
  }
}) 