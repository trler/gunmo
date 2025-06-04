/// <reference types="vite/client" />
/// <reference types="element-plus/global" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module '@/types/user' {
  export type UserRole = 'system_admin' | 'process_engineer' | 'equipment_operator' | 'quality_inspector'
  export type UserStatus = 'active' | 'inactive'

  export interface User {
    id: number
    username: string
    email: string
    full_name: string
    role: UserRole
    status: UserStatus
    last_login: string | null
    date_joined: string
  }

  export interface UserCreateData {
    username: string
    email: string
    full_name: string
    role: UserRole
    password: string
  }

  export interface UserUpdateData {
    email?: string
    full_name?: string
    role?: UserRole
  }

  export interface UserListResponse {
    count: number
    next: string | null
    previous: string | null
    results: User[]
  }

  export interface UserListParams {
    page?: number
    page_size?: number
    search?: string
    role?: UserRole
    status?: UserStatus
  }
}

declare module '@/types/statistics' {
  export interface DateRange {
    start: Date
    end: Date
  }

  export interface OverviewData {
    totalUsers: number
    userGrowth: number
    totalEquipment: number
    equipmentGrowth: number
    totalProcesses: number
    processGrowth: number
    qualityRate: number
    qualityGrowth: number
  }

  export interface TableData {
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

  export interface TableResponse {
    count: number
    next: string | null
    previous: string | null
    results: TableData[]
  }

  export interface ChartData {
    dates: string[]
    values: number[]
  }

  export interface UserChartData {
    dates: string[]
    newUsers: number[]
    activeUsers: number[]
  }

  export interface EquipmentChartData {
    status: Array<{
      name: string
      value: number
    }>
    efficiency: Array<{
      name: string
      value: number
    }>
  }

  export interface ProcessChartData {
    processes: string[]
    values: number[]
  }
}

declare module 'vue-echarts' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
  export const THEME_KEY: symbol
}

declare module 'echarts/core' {
  export * from 'echarts'
  export type ComposeOption<T> = T
}

declare module 'echarts/charts' {
  export interface LineSeriesOption {
    type: 'line'
    data: number[]
    name?: string
  }

  export interface BarSeriesOption {
    type: 'bar'
    data: number[]
    name?: string
  }

  export interface PieSeriesOption {
    type: 'pie'
    data: Array<{
      name: string
      value: number
    }>
    radius?: string | string[]
  }
}

declare module 'echarts/components' {
  export interface TitleComponentOption {
    title?: {
      text?: string
      subtext?: string
    }
  }

  export interface TooltipComponentOption {
    tooltip?: {
      trigger?: 'item' | 'axis'
      formatter?: string | ((params: any) => string)
    }
  }

  export interface GridComponentOption {
    grid?: {
      left?: string | number
      right?: string | number
      top?: string | number
      bottom?: string | number
    }
  }

  export interface LegendComponentOption {
    legend?: {
      data?: string[]
      orient?: 'horizontal' | 'vertical'
      left?: string | number
    }
  }
}

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_APP_TITLE: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
} 