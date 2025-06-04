<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h2>滚磨光整加工系统</h2>
        <p class="subtitle">精密加工 · 智能制造</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="loginForm.username"
            :class="{ 'error': errors.username }"
            @input="validateField('username')"
            placeholder="请输入用户名"
            autocomplete="username"
          />
          <span class="error-message" v-if="errors.username">{{ errors.username }}</span>
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="loginForm.password"
            :class="{ 'error': errors.password }"
            @input="validateField('password')"
            placeholder="请输入密码"
            autocomplete="current-password"
          />
          <span class="error-message" v-if="errors.password">{{ errors.password }}</span>
        </div>

        <div class="error-alert" v-if="error">
          <i class="fas fa-exclamation-circle"></i>
          {{ error.message }}
        </div>

        <div class="form-actions">
          <button 
            type="submit" 
            :disabled="loading || !isFormValid"
            :class="{ 'loading': loading }"
          >
            <span v-if="loading" class="loading-spinner"></span>
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </div>

        <div class="form-footer">
          <router-link to="/register" class="register-link">
            还没有账号？立即注册
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import type { LoginCredentials, AuthError } from '@/types/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const { login, loading, error } = useAuth()

const loginForm = reactive<LoginCredentials>({
  username: '',
  password: ''
})

type FormField = 'username' | 'password'
type FormErrors = Record<FormField, string>

const errors = reactive<FormErrors>({
  username: '',
  password: ''
})

const validateField = (field: FormField) => {
  errors[field] = ''
  if (!loginForm[field]) {
    errors[field] = `${field === 'username' ? '用户名' : '密码'}不能为空`
  }
}

const isFormValid = computed(() => {
  return loginForm.username && loginForm.password && !Object.values(errors).some(error => error)
})

const handleLogin = async () => {
  // 验证所有字段
  validateField('username')
  validateField('password')
  
  if (!isFormValid.value) {
    ElMessage.warning('请填写完整的登录信息')
    return
  }

  try {
    await login(loginForm, {
      redirectTo: '/dashboard',
      onSuccess: () => {
        ElMessage.success('登录成功')
      },
      onError: (error: AuthError) => {
        ElMessage.error(error.message || '登录失败，请重试')
      }
    })
  } catch (error) {
    // 错误已经在 onError 回调中处理
    console.error('登录失败:', error)
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
}

.login-box {
  width: 100%;
  max-width: 420px;
  padding: 2.5rem;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid rgba(26, 35, 126, 0.1);
}

h2 {
  color: #1a237e;
  font-size: 2rem;
  margin-bottom: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.subtitle {
  color: #546e7a;
  font-size: 1.1rem;
  margin: 0;
  font-weight: 500;
}

.login-form {
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
  color: #37474f;
  font-size: 0.95rem;
}

input {
  padding: 0.875rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: #f8f9fa;
}

input:focus {
  outline: none;
  border-color: #1a237e;
  background-color: #fff;
  box-shadow: 0 0 0 3px rgba(26, 35, 126, 0.1);
}

input.error {
  border-color: #dc2626;
  background-color: #fef2f2;
}

input.error:focus {
  box-shadow: 0 0 0 2px rgba(220, 38, 38, 0.1);
}

.error-message {
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.error-alert {
  background-color: #fef2f2;
  border: 1px solid #fee2e2;
  color: #dc2626;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.error-alert i {
  font-size: 1rem;
}

.form-actions {
  margin-top: 1rem;
}

button {
  width: 100%;
  padding: 0.875rem;
  background-color: #1a237e;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

button:hover:not(:disabled) {
  background-color: #0d47a1;
  transform: translateY(-1px);
}

button:disabled {
  background-color: #90a4ae;
  cursor: not-allowed;
}

button.loading {
  position: relative;
  color: transparent;
}

button.loading .loading-spinner {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  margin: 0;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #ffffff;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 0.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.form-footer {
  margin-top: 1.5rem;
  text-align: center;
}

.register-link {
  color: #1a237e;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.register-link:hover {
  color: #0d47a1;
  text-decoration: underline;
}
</style> 