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