// 用户类型
export type UserType = 'system_admin' | 'process_engineer' | 'equipment_operator' | 'quality_inspector' | 'fullstack_engineer'

// 用户信息
export interface User {
  id: number
  username: string
  email: string
  first_name?: string
  last_name?: string
  user_type: UserType
  company?: string
  department?: string
  industry_role?: string
  phone?: string
  date_joined: string
  last_login?: string
}

// 登录表单类型
export interface LoginForm {
  username: string
  password: string
}

// 注册表单类型
export interface RegisterCredentials {
  username: string
  email: string
  password: string
  password_confirm: string
  first_name?: string
  last_name?: string
  user_type: UserType
  company?: string
  department?: string
  industry_role?: string
  phone?: string
}

// 设备类型
export interface EquipmentType {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
}

// 设备状态类型
export type EquipmentStatus = 'running' | 'idle' | 'maintenance' | 'error' | 'offline'

// 设备信息
export interface Equipment {
  id: number
  name: string
  type: EquipmentType
  serial_number: string
  location: string
  status: EquipmentStatus
  description?: string
  last_maintenance?: string
  created_at: string
  updated_at: string
}

// 工艺数据状态类型
export type ProcessDataStatus = 'active' | 'inactive'

// 工艺数据类别
export interface ProcessDataCategory {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
}

// 工艺数据
export interface ProcessData {
  id: number
  name: string
  description?: string
  status: ProcessDataStatus
  category?: ProcessDataCategory
  created_at: string
  updated_at: string
}

// JWT Token 类型
export interface TokenResponse {
  access: string
  refresh: string
  user: User
}

// 登录凭证
export interface LoginCredentials extends LoginForm {}

// 认证错误
export interface AuthError {
  message: string
  code?: string
  detail?: string
  non_field_errors?: string[]
}

// 认证状态
export interface AuthState {
  user: User | null
  token: string | null
  loading: boolean
  error: AuthError | null
}

// 用户配置文件类型
export interface UserProfile {
  id: number
  user: number
  full_name: string
  phone: string
  department: string
  position: string
  avatar: string | null
  created_at: string
  updated_at: string
}

// 认证响应
export interface AuthResponse {
  user: User
  access: string
  refresh: string
} 