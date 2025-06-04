<template>
  <div class="users-view">
    <div class="header">
      <h2>用户管理</h2>
      <el-button type="primary" @click="handleAddUser">
        <el-icon><Plus /></el-icon>添加用户
      </el-button>
    </div>

    <!-- 搜索和筛选 -->
    <div class="search-bar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索用户名、邮箱或姓名"
        class="search-input"
        clearable
        @clear="handleSearch"
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-select v-model="roleFilter" placeholder="角色筛选" clearable @change="handleSearch">
        <el-option
          v-for="role in roles"
          :key="role.value"
          :label="role.label"
          :value="role.value"
        />
      </el-select>

      <el-select v-model="statusFilter" placeholder="状态筛选" clearable @change="handleSearch">
        <el-option label="启用" value="active" />
        <el-option label="禁用" value="inactive" />
      </el-select>
    </div>

    <!-- 用户列表 -->
    <el-card class="user-list">
      <el-table
        v-loading="loading"
        :data="filteredUsers"
        style="width: 100%"
        border
      >
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="full_name" label="姓名" min-width="120" />
        <el-table-column prop="role" label="角色" min-width="120">
          <template #default="{ row }">
            <el-tag :type="getRoleTagType(row.role)">
              {{ getRoleLabel(row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_login" label="最后登录" min-width="180">
          <template #default="{ row }">
            {{ formatDate(row.last_login) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button
                type="primary"
                link
                @click="handleEditUser(row)"
              >
                编辑
              </el-button>
              <el-button
                type="primary"
                link
                @click="handleResetPassword(row)"
              >
                重置密码
              </el-button>
              <el-button
                :type="row.status === 'active' ? 'danger' : 'success'"
                link
                @click="handleToggleStatus(row)"
              >
                {{ row.status === 'active' ? '禁用' : '启用' }}
              </el-button>
              <el-button
                type="danger"
                link
                @click="handleDeleteUser(row)"
              >
                删除
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="totalUsers"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 用户表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加用户' : '编辑用户'"
      width="500px"
    >
      <el-form
        ref="userFormRef"
        :model="userForm"
        :rules="userFormRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" :disabled="dialogType === 'edit'" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" />
        </el-form-item>
        <el-form-item label="姓名" prop="full_name">
          <el-input v-model="userForm.full_name" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" placeholder="请选择角色">
            <el-option
              v-for="role in roles"
              :key="role.value"
              :label="role.label"
              :value="role.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="dialogType === 'add'">
          <el-input v-model="userForm.password" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword" v-if="dialogType === 'add'">
          <el-input v-model="userForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitUser">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 重置密码对话框 -->
    <el-dialog
      v-model="resetPasswordDialogVisible"
      title="重置密码"
      width="400px"
    >
      <el-form
        ref="resetPasswordFormRef"
        :model="resetPasswordForm"
        :rules="resetPasswordRules"
        label-width="100px"
      >
        <el-form-item label="新密码" prop="password">
          <el-input v-model="resetPasswordForm.password" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="resetPasswordForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="resetPasswordDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitResetPassword">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'
import type { User, UserRole, UserCreateData, UserUpdateData } from '@/types/user'

const userStore = useUserStore()

// 状态定义
const loading = ref(false)
const users = ref<User[]>([])
const searchQuery = ref('')
const roleFilter = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const totalUsers = ref(0)
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const resetPasswordDialogVisible = ref(false)
const currentUserId = ref<number | null>(null)

// 表单引用
const userFormRef = ref<FormInstance>()
const resetPasswordFormRef = ref<FormInstance>()

// 角色选项
const roles: { label: string; value: UserRole }[] = [
  { label: '系统管理员', value: 'system_admin' },
  { label: '工艺工程师', value: 'process_engineer' },
  { label: '设备操作员', value: 'equipment_operator' },
  { label: '质量检验员', value: 'quality_inspector' }
]

// 用户表单
const userForm = ref({
  username: '',
  email: '',
  full_name: '',
  role: '',
  password: '',
  confirmPassword: ''
})

// 重置密码表单
const resetPasswordForm = ref({
  password: '',
  confirmPassword: ''
})

// 表单验证规则
const userFormRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  full_name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== userForm.value.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const resetPasswordRules: FormRules = {
  password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== resetPasswordForm.value.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 计算属性
const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const matchesSearch = !searchQuery.value ||
      user.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      user.email.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      user.full_name.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesRole = !roleFilter.value || user.role === roleFilter.value
    const matchesStatus = !statusFilter.value || user.status === statusFilter.value
    
    return matchesSearch && matchesRole && matchesStatus
  })
})

// 方法定义
const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await userStore.fetchUsers({
      page: currentPage.value,
      page_size: pageSize.value
    })
    users.value = response.results
    totalUsers.value = response.count
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchUsers()
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchUsers()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchUsers()
}

const handleAddUser = () => {
  dialogType.value = 'add'
  userForm.value = {
    username: '',
    email: '',
    full_name: '',
    role: '',
    password: '',
    confirmPassword: ''
  }
  dialogVisible.value = true
}

const handleEditUser = (user: User) => {
  dialogType.value = 'edit'
  userForm.value = {
    username: user.username,
    email: user.email,
    full_name: user.full_name,
    role: user.role,
    password: '',
    confirmPassword: ''
  }
  currentUserId.value = user.id
  dialogVisible.value = true
}

const handleSubmitUser = async () => {
  if (!userFormRef.value) return
  
  await userFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (dialogType.value === 'add') {
          const createData: UserCreateData = {
            username: userForm.value.username,
            email: userForm.value.email,
            full_name: userForm.value.full_name,
            role: userForm.value.role as UserRole,
            password: userForm.value.password
          }
          await userStore.createUser(createData)
          ElMessage.success('用户创建成功')
        } else {
          if (!currentUserId.value) return
          const updateData: UserUpdateData = {
            email: userForm.value.email,
            full_name: userForm.value.full_name,
            role: userForm.value.role as UserRole
          }
          await userStore.updateUser(currentUserId.value, updateData)
          ElMessage.success('用户更新成功')
        }
        dialogVisible.value = false
        fetchUsers()
      } catch (error) {
        ElMessage.error(dialogType.value === 'add' ? '创建用户失败' : '更新用户失败')
      }
    }
  })
}

const handleDeleteUser = async (user: User) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 ${user.username} 吗？`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await userStore.deleteUser(user.id)
    ElMessage.success('用户删除成功')
    fetchUsers()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除用户失败')
    }
  }
}

const handleToggleStatus = async (user: User) => {
  try {
    await userStore.updateUserStatus(user.id, user.status === 'active' ? 'inactive' : 'active')
    ElMessage.success(`用户已${user.status === 'active' ? '禁用' : '启用'}`)
    fetchUsers()
  } catch (error) {
    ElMessage.error('更新用户状态失败')
  }
}

const handleResetPassword = (user: User) => {
  currentUserId.value = user.id
  resetPasswordForm.value = {
    password: '',
    confirmPassword: ''
  }
  resetPasswordDialogVisible.value = true
}

const handleSubmitResetPassword = async () => {
  if (!resetPasswordFormRef.value || !currentUserId.value) return
  
  await resetPasswordFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await userStore.resetUserPassword(currentUserId.value, resetPasswordForm.value.password)
        ElMessage.success('密码重置成功')
        resetPasswordDialogVisible.value = false
      } catch (error) {
        ElMessage.error('密码重置失败')
      }
    }
  })
}

const getRoleLabel = (role: string) => {
  return roles.find(r => r.value === role)?.label || role
}

const getRoleTagType = (role: string): 'primary' | 'success' | 'warning' | 'info' | 'danger' => {
  const typeMap: Record<string, 'primary' | 'success' | 'warning' | 'info' | 'danger'> = {
    system_admin: 'danger',
    process_engineer: 'primary',
    equipment_operator: 'success',
    quality_inspector: 'warning'
  }
  return typeMap[role] || 'info'
}

const formatDate = (date: string | null) => {
  if (!date) return '从未登录'
  return new Date(date).toLocaleString()
}

// 生命周期钩子
onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.users-view {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.search-input {
  width: 300px;
}

.user-list {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

:deep(.el-tag) {
  text-transform: capitalize;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style> 