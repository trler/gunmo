import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

// 物料类型定义
export type MaterialType = 'block' | 'chemical' | 'fixture' | 'equipment'

// 通用响应接口
export interface MaterialListResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

// 通用查询参数接口
export interface MaterialListParams {
  type: MaterialType
  page?: number
  page_size?: number
  keyword?: string
  status?: string
}

// 通用物料接口
export interface Material {
  id: number
  code: string
  name: string
  status: string
  created_at: string
  updated_at: string
}

// 磨块接口
export interface Block extends Material {
  type: string
  specification: string
  manufacturer: string
  hardness: number
  grit_size: string
  material: string
  usage_count: number
  max_usage_count: number
  files: MaterialFile[]
}

// 化学剂接口
export interface Chemical extends Material {
  type: string
  specification: string
  manufacturer: string
  safety_level: string
  storage_condition: string
  shelf_life: string
  usage_count: number
  max_usage_count: number
  files: MaterialFile[]
}

// 工装接口
export interface Fixture extends Material {
  type: string
  specification: string
  manufacturer: string
  part_type: string
  size: string
  accuracy: string
  clamping_force: string
  material: string
  usage_count: number
  max_usage_count: number
  files: MaterialFile[]
}

// 设备接口
export interface Equipment extends Material {
  type: string
  model: string
  manufacturer: string
  serial_number: string
  purchase_date: string
  status: string
  maintenance_cycle: string
  last_maintenance_date: string
  next_maintenance_date: string
  files: MaterialFile[]
}

// 物料文件接口
export interface MaterialFile {
  id: number
  file_name: string
  file_url: string
  file_type: string
  file_size: number
  uploaded_at: string
}

// 错误响应接口
export interface ErrorResponse {
  detail: string
  code?: string
}

export const useMaterialStore = defineStore('material', () => {
  // 状态定义
  const loading = ref(false)
  const error = ref<string | null>(null)
  const materialList = ref<Material[]>([])
  const total = ref(0)
  const currentMaterial = ref<Material | null>(null)
  const materialFiles = ref<MaterialFile[]>([])

  // 获取物料列表
  const getMaterialList = async (params: MaterialListParams) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get<MaterialListResponse<Material>>('/api/material/', {
        params
      })
      materialList.value = response.data.results
      total.value = response.data.count
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || '获取物料列表失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 创建物料
  const createMaterial = async (type: MaterialType, data: any) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post<Material>(`/api/material/${type}/`, data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || '创建物料失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 更新物料
  const updateMaterial = async (type: MaterialType, id: number, data: any) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.put<Material>(`/api/material/${type}/${id}/`, data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || '更新物料失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 删除物料
  const deleteMaterial = async (type: MaterialType, id: number) => {
    loading.value = true
    error.value = null
    try {
      await axios.delete(`/api/material/${type}/${id}/`)
    } catch (err: any) {
      error.value = err.response?.data?.detail || '删除物料失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取物料详情
  const getMaterialDetail = async (type: MaterialType, id: number) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get<Material>(`/api/material/${type}/${id}/`)
      currentMaterial.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || '获取物料详情失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 上传物料文件
  const uploadMaterialFile = async (type: MaterialType, id: number, file: File) => {
    loading.value = true
    error.value = null
    const formData = new FormData()
    formData.append('file', file)
    try {
      const response = await axios.post<MaterialFile>(
        `/api/material/${type}/${id}/files/`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      )
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || '上传文件失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 删除物料文件
  const deleteMaterialFile = async (type: MaterialType, id: number, fileId: number) => {
    loading.value = true
    error.value = null
    try {
      await axios.delete(`/api/material/${type}/${id}/files/${fileId}/`)
    } catch (err: any) {
      error.value = err.response?.data?.detail || '删除文件失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取物料文件列表
  const getMaterialFiles = async (type: MaterialType, id: number) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get<MaterialFile[]>(`/api/material/${type}/${id}/files/`)
      materialFiles.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || '获取文件列表失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 导出物料数据
  const exportMaterial = async (type: MaterialType, params: { ids?: number[] }) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get(`/api/material/${type}/export/`, {
        params,
        responseType: 'blob'
      })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${type}_export.xlsx`)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (err: any) {
      error.value = err.response?.data?.detail || '导出数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    materialList,
    total,
    currentMaterial,
    materialFiles,
    getMaterialList,
    createMaterial,
    updateMaterial,
    deleteMaterial,
    getMaterialDetail,
    uploadMaterialFile,
    deleteMaterialFile,
    getMaterialFiles,
    exportMaterial
  }
}) 