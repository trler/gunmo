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