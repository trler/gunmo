import { defineStore } from 'pinia'
import axiosInstance from '@/api/axios'
import type { AxiosError } from 'axios'

// 工装类型定义
export type FixtureType = '定位工装' | '夹持工装' | '检测工装' | '辅助工装'
export type FixtureMaterial = '45steel' | 'aluminum' | 'plastic'

// 工装信息接口
export interface Fixture {
  id: string
  code: string
  name: string
  type: FixtureType
  manufacturer: string
  partType: string
  size: string
  accuracy: string
  clampingForce: string
  material: FixtureMaterial
  remark?: string
  created_at: string
  updated_at: string
}

// 工装文件接口
export interface FixtureFile {
  id: string
  fixtureId: string
  name: string
  size: number
  uploadTime: string
  url: string
}

// 工装列表响应接口
export interface FixtureListResponse {
  count: number
  next: string | null
  previous: string | null
  results: Fixture[]
}

// 工装列表查询参数接口
export interface FixtureListParams {
  page?: number
  page_size?: number
  code?: string
  name?: string
  type?: FixtureType | ''
}

// 错误响应接口
export interface ErrorResponse {
  detail: string
}

export const useFixtureStore = defineStore('fixture', {
  state: () => ({
    loading: false,
    error: null as string | null,
    fixtureList: [] as Fixture[],
    total: 0,
    currentFixture: null as Fixture | null,
    fixtureFiles: [] as FixtureFile[]
  }),

  actions: {
    // 获取工装列表
    async getFixtureList(params: FixtureListParams) {
      this.loading = true
      this.error = null
      try {
        const response = await axiosInstance.get<FixtureListResponse>('/fixtures/', { params })
        this.fixtureList = response.data.results
        this.total = response.data.count
        return response.data
      } catch (error) {
        const axiosError = error as AxiosError<ErrorResponse>
        this.error = axiosError.response?.data?.detail || '获取工装列表失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    // 创建工装
    async createFixture(fixtureData: FormData) {
      this.loading = true
      this.error = null
      try {
        const response = await axiosInstance.post<Fixture>('/fixtures/', fixtureData)
        return response.data
      } catch (error) {
        const axiosError = error as AxiosError<ErrorResponse>
        this.error = axiosError.response?.data?.detail || '创建工装失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    // 更新工装
    async updateFixture(id: string, fixtureData: FormData) {
      this.loading = true
      this.error = null
      try {
        const response = await axiosInstance.put<Fixture>(`/fixtures/${id}/`, fixtureData)
        return response.data
      } catch (error) {
        const axiosError = error as AxiosError<ErrorResponse>
        this.error = axiosError.response?.data?.detail || '更新工装失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    // 删除工装
    async deleteFixture(id: string) {
      this.loading = true
      this.error = null
      try {
        await axiosInstance.delete(`/fixtures/${id}/`)
      } catch (error) {
        const axiosError = error as AxiosError<ErrorResponse>
        this.error = axiosError.response?.data?.detail || '删除工装失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    // 获取工装文件列表
    async getFixtureFiles(fixtureId: string) {
      this.loading = true
      this.error = null
      try {
        const response = await axiosInstance.get<FixtureFile[]>(`/fixtures/${fixtureId}/files/`)
        this.fixtureFiles = response.data
        return response.data
      } catch (error) {
        const axiosError = error as AxiosError<ErrorResponse>
        this.error = axiosError.response?.data?.detail || '获取工装文件失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    // 上传工装文件
    async uploadFixtureFile(fixtureId: string, file: File) {
      this.loading = true
      this.error = null
      try {
        const formData = new FormData()
        formData.append('file', file)
        formData.append('fixture_id', fixtureId)
        const response = await axiosInstance.post<FixtureFile>('/fixtures/upload/', formData)
        return response.data
      } catch (error) {
        const axiosError = error as AxiosError<ErrorResponse>
        this.error = axiosError.response?.data?.detail || '上传工装文件失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    // 删除工装文件
    async deleteFixtureFile(fileId: string) {
      this.loading = true
      this.error = null
      try {
        await axiosInstance.delete(`/fixtures/files/${fileId}/`)
      } catch (error) {
        const axiosError = error as AxiosError<ErrorResponse>
        this.error = axiosError.response?.data?.detail || '删除工装文件失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    // 下载工装文件
    async downloadFixtureFile(fileId: string) {
      this.loading = true
      this.error = null
      try {
        const response = await axiosInstance.get(`/fixtures/files/${fileId}/download/`, {
          responseType: 'blob'
        })
        return response.data
      } catch (error) {
        const axiosError = error as AxiosError<ErrorResponse>
        this.error = axiosError.response?.data?.detail || '下载工装文件失败'
        throw error
      } finally {
        this.loading = false
      }
    }
  }
}) 