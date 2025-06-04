import { defineStore } from 'pinia'
import { ref } from 'vue'
import axiosInstance from '@/api/axios'

interface DateRange {
  start: Date
  end: Date
}

interface OverviewData {
  totalUsers: number
  userGrowth: number
  totalEquipment: number
  equipmentGrowth: number
  totalProcesses: number
  processGrowth: number
  qualityRate: number
  qualityGrowth: number
}

interface TableData {
  date: string
  newUsers: number
  activeUsers: number
  onlineEquipment: number
  runningEquipment: number
  processCount: number
  qualityRate: number
  avgEfficiency: number
  remarks: string
}

interface TableResponse {
  count: number
  next: string | null
  previous: string | null
  results: TableData[]
}

interface ChartData {
  dates: string[]
  values: number[]
}

interface UserChartData {
  dates: string[]
  newUsers: number[]
  activeUsers: number[]
}

interface EquipmentChartData {
  status?: Array<{
    name: string
    value: number
  }>
  efficiency?: Array<{
    name: string
    value: number
  }>
}

interface ProcessChartData {
  processes: string[]
  values: number[]
}

export const useStatisticsStore = defineStore('statistics', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 获取概览数据
  const fetchOverview = async (dateRange: DateRange | null): Promise<OverviewData> => {
    try {
      loading.value = true
      error.value = null
      const params = dateRange ? {
        start_date: dateRange.start.toISOString().split('T')[0],
        end_date: dateRange.end.toISOString().split('T')[0]
      } : {}
      const response = await axiosInstance.get<OverviewData>('/statistics/overview/', { params })
      return response.data
    } catch (err: any) {
      console.error('获取概览数据失败:', err)
      error.value = err.response?.data?.detail || '获取概览数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取表格数据
  const fetchTableData = async (params: {
    page: number
    page_size: number
    date_range: DateRange | null
  }): Promise<TableResponse> => {
    try {
      loading.value = true
      error.value = null
      const requestParams = {
        ...params,
        start_date: params.date_range?.start.toISOString().split('T')[0],
        end_date: params.date_range?.end.toISOString().split('T')[0]
      }
      delete requestParams.date_range
      const response = await axiosInstance.get<TableResponse>('/statistics/table/', { params: requestParams })
      return response.data
    } catch (err: any) {
      console.error('获取表格数据失败:', err)
      error.value = err.response?.data?.detail || '获取表格数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取用户图表数据
  const fetchUserChartData = async (
    type: 'week' | 'month' | 'year',
    dateRange: DateRange | null
  ): Promise<UserChartData> => {
    try {
      loading.value = true
      error.value = null
      const params = {
        type,
        ...(dateRange ? {
          start_date: dateRange.start.toISOString().split('T')[0],
          end_date: dateRange.end.toISOString().split('T')[0]
        } : {})
      }
      const response = await axiosInstance.get<UserChartData>('/statistics/charts/users/', { params })
      return response.data
    } catch (err: any) {
      console.error('获取用户图表数据失败:', err)
      error.value = err.response?.data?.detail || '获取用户图表数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取设备图表数据
  const fetchEquipmentChartData = async (
    type: 'status' | 'efficiency',
    dateRange: DateRange | null
  ): Promise<EquipmentChartData> => {
    try {
      loading.value = true
      error.value = null
      const params = {
        type,
        ...(dateRange ? {
          start_date: dateRange.start.toISOString().split('T')[0],
          end_date: dateRange.end.toISOString().split('T')[0]
        } : {})
      }
      const response = await axiosInstance.get<EquipmentChartData>('/statistics/charts/equipment/', { params })
      return response.data
    } catch (err: any) {
      console.error('获取设备图表数据失败:', err)
      error.value = err.response?.data?.detail || '获取设备图表数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取质量图表数据
  const fetchQualityChartData = async (
    metric: 'pass_rate' | 'defect_rate' | 'rework_rate',
    dateRange: DateRange | null
  ): Promise<ChartData> => {
    try {
      loading.value = true
      error.value = null
      const params = {
        metric,
        ...(dateRange ? {
          start_date: dateRange.start.toISOString().split('T')[0],
          end_date: dateRange.end.toISOString().split('T')[0]
        } : {})
      }
      const response = await axiosInstance.get<ChartData>('/statistics/charts/quality/', { params })
      return response.data
    } catch (err: any) {
      console.error('获取质量图表数据失败:', err)
      error.value = err.response?.data?.detail || '获取质量图表数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取工艺图表数据
  const fetchProcessChartData = async (
    metric: 'efficiency' | 'quality' | 'cost',
    dateRange: DateRange | null
  ): Promise<ProcessChartData> => {
    try {
      loading.value = true
      error.value = null
      const params = {
        metric,
        ...(dateRange ? {
          start_date: dateRange.start.toISOString().split('T')[0],
          end_date: dateRange.end.toISOString().split('T')[0]
        } : {})
      }
      const response = await axiosInstance.get<ProcessChartData>('/statistics/charts/process/', { params })
      return response.data
    } catch (err: any) {
      console.error('获取工艺图表数据失败:', err)
      error.value = err.response?.data?.detail || '获取工艺图表数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 导出统计数据
  const exportStatistics = async (dateRange: DateRange | null): Promise<Blob> => {
    try {
      loading.value = true
      error.value = null
      const params = dateRange ? {
        start_date: dateRange.start.toISOString().split('T')[0],
        end_date: dateRange.end.toISOString().split('T')[0]
      } : {}
      const response = await axiosInstance.get('/statistics/export/', {
        params,
        responseType: 'blob'
      })
      return response.data
    } catch (err: any) {
      console.error('导出统计数据失败:', err)
      error.value = err.response?.data?.detail || '导出统计数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    fetchOverview,
    fetchTableData,
    fetchUserChartData,
    fetchEquipmentChartData,
    fetchQualityChartData,
    fetchProcessChartData,
    exportStatistics
  }
}) 