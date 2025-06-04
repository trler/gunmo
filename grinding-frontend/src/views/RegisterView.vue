<template>
  <div class="register-container">
    <div class="register-box">
      <h2>用户注册</h2>
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="registerForm.username"
            required
            placeholder="请输入用户名"
          />
          <span class="error-message" v-if="errors.username">{{ errors.username }}</span>
        </div>

        <div class="form-group">
          <label for="email">电子邮箱</label>
          <input
            type="email"
            id="email"
            v-model="registerForm.email"
            required
            placeholder="请输入电子邮箱"
          />
          <span class="error-message" v-if="errors.email">{{ errors.email }}</span>
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="registerForm.password"
            required
            placeholder="请输入密码"
          />
          <span class="error-message" v-if="errors.password">{{ errors.password }}</span>
        </div>

        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="registerForm.password_confirm"
            required
            placeholder="请再次输入密码"
          />
          <span class="error-message" v-if="errors.password_confirm">{{ errors.password_confirm }}</span>
        </div>

        <div class="form-group">
          <label for="userType">用户类型</label>
          <select
            id="userType"
            v-model="registerForm.user_type"
            required
            class="form-select"
          >
            <option value="">请选择用户类型</option>
            <option value="equipment_operator">设备操作员</option>
            <option value="process_engineer">工艺工程师</option>
            <option value="quality_inspector">质量检测员</option>
            <option value="system_admin">系统管理员</option>
          </select>
          <span class="error-message" v-if="errors.user_type">{{ errors.user_type }}</span>
        </div>

        <div class="form-group">
          <label for="firstName">姓</label>
          <input
            type="text"
            id="firstName"
            v-model="registerForm.first_name"
            placeholder="请输入姓"
          />
        </div>

        <div class="form-group">
          <label for="lastName">名</label>
          <input
            type="text"
            id="lastName"
            v-model="registerForm.last_name"
            placeholder="请输入名"
          />
        </div>

        <div class="form-group">
          <label for="company">公司</label>
          <input
            type="text"
            id="company"
            v-model="registerForm.company"
            placeholder="请输入公司名称"
          />
        </div>

        <div class="form-group">
          <label for="department">部门</label>
          <input
            type="text"
            id="department"
            v-model="registerForm.department"
            placeholder="请输入部门名称"
          />
        </div>

        <div class="form-group">
          <label for="industryRole">行业角色</label>
          <input
            type="text"
            id="industryRole"
            v-model="registerForm.industry_role"
            placeholder="请输入行业角色"
          />
        </div>

        <div class="form-group">
          <label for="phone">电话</label>
          <input
            type="tel"
            id="phone"
            v-model="registerForm.phone"
            placeholder="请输入电话号码"
          />
        </div>

        <div class="form-actions">
          <button type="submit" :disabled="loading || !isFormValid">
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </div>

        <div class="form-footer">
          <router-link to="/login">已有账号？立即登录</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import type { RegisterCredentials } from '@/types/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const { register, loading, error } = useAuth()

const registerForm = reactive<RegisterCredentials>({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
  first_name: '',
  last_name: '',
  user_type: 'equipment_operator',
  company: '',
  department: '',
  industry_role: '',
  phone: ''
})

type FormField = keyof RegisterCredentials
type FormErrors = Partial<Record<FormField, string>>

const errors = reactive<FormErrors>({})

const validateField = (field: FormField) => {
  errors[field] = ''
  
  switch (field) {
    case 'username':
      if (!registerForm.username) {
        errors.username = '用户名不能为空'
      } else if (registerForm.username.length < 3) {
        errors.username = '用户名长度不能小于3个字符'
      }
      break
      
    case 'email':
      if (!registerForm.email) {
        errors.email = '邮箱不能为空'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(registerForm.email)) {
        errors.email = '请输入有效的邮箱地址'
      }
      break
      
    case 'password':
      if (!registerForm.password) {
        errors.password = '密码不能为空'
      } else if (registerForm.password.length < 6) {
        errors.password = '密码长度不能小于6个字符'
      }
      break
      
    case 'password_confirm':
      if (!registerForm.password_confirm) {
        errors.password_confirm = '请确认密码'
      } else if (registerForm.password_confirm !== registerForm.password) {
        errors.password_confirm = '两次输入的密码不一致'
      }
      break
      
    case 'user_type':
      if (!registerForm.user_type) {
        errors.user_type = '请选择用户类型'
      }
      break
  }
}

const validateForm = () => {
  validateField('username')
  validateField('email')
  validateField('password')
  validateField('password_confirm')
  validateField('user_type')
}

const isFormValid = computed(() => {
  return (
    registerForm.username.length >= 3 &&
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(registerForm.email) &&
    registerForm.password.length >= 6 &&
    registerForm.password === registerForm.password_confirm &&
    !!registerForm.user_type &&
    !Object.values(errors).some(error => error)
  )
})

const handleRegister = async () => {
  validateForm()
  
  if (!isFormValid.value) {
    ElMessage.warning('请完善注册信息')
    return
  }

  try {
    await register(registerForm, {
      onSuccess: () => ElMessage.success('注册成功'),
      onError: (error) => ElMessage.error(error.message || '注册失败')
    })
  } catch (err) {
    // 错误已经在 onError 回调中处理
    console.error('注册失败:', err)
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 2rem;
}

.register-box {
  width: 100%;
  max-width: 500px;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 500;
  color: #333;
}

input, .form-select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus, .form-select:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.error-message {
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.form-actions {
  margin-top: 1rem;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover:not(:disabled) {
  background-color: #357abd;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.form-footer {
  margin-top: 1rem;
  text-align: center;
}

.form-footer a {
  color: #4a90e2;
  text-decoration: none;
}

.form-footer a:hover {
  text-decoration: underline;
}

@media (max-width: 640px) {
  .register-container {
    padding: 1rem;
  }
  
  .register-box {
    padding: 1.5rem;
  }
}
</style> 