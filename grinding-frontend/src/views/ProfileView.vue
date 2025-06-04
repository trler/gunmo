<template>
  <div class="profile-container">
    <div class="profile-box">
      <h2>用户资料</h2>
      <form @submit.prevent="handleUpdateProfile" class="profile-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="profileForm.username"
            disabled
            class="disabled-input"
          />
          <small class="form-text">用户名不可修改</small>
        </div>

        <div class="form-group">
          <label for="email">电子邮箱</label>
          <input
            type="email"
            id="email"
            v-model="profileForm.email"
            required
            placeholder="请输入电子邮箱"
          />
        </div>

        <div class="form-group">
          <label for="fullName">姓名</label>
          <input
            type="text"
            id="fullName"
            v-model="profileForm.full_name"
            placeholder="请输入姓名"
          />
        </div>

        <div class="form-group">
          <label for="phone">电话</label>
          <input
            type="tel"
            id="phone"
            v-model="profileForm.phone"
            placeholder="请输入电话号码"
          />
        </div>

        <div class="form-group">
          <label for="department">部门</label>
          <input
            type="text"
            id="department"
            v-model="profileForm.department"
            placeholder="请输入部门"
          />
        </div>

        <div class="form-group">
          <label for="position">职位</label>
          <input
            type="text"
            id="position"
            v-model="profileForm.position"
            placeholder="请输入职位"
          />
        </div>

        <div class="form-actions">
          <button type="submit" :disabled="loading">
            {{ loading ? '保存中...' : '保存修改' }}
          </button>
        </div>
      </form>

      <div class="password-section">
        <h3>修改密码</h3>
        <form @submit.prevent="handleChangePassword" class="password-form">
          <div class="form-group">
            <label for="currentPassword">当前密码</label>
            <input
              type="password"
              id="currentPassword"
              v-model="passwordForm.currentPassword"
              required
              placeholder="请输入当前密码"
            />
          </div>

          <div class="form-group">
            <label for="newPassword">新密码</label>
            <input
              type="password"
              id="newPassword"
              v-model="passwordForm.newPassword"
              required
              placeholder="请输入新密码"
            />
          </div>

          <div class="form-group">
            <label for="confirmPassword">确认新密码</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="passwordForm.confirmPassword"
              required
              placeholder="请再次输入新密码"
            />
          </div>

          <div class="form-actions">
            <button type="submit" :disabled="passwordLoading || !isPasswordValid">
              {{ passwordLoading ? '修改中...' : '修改密码' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import type { UserProfile } from '@/types/auth'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const passwordLoading = ref(false)

// 用户资料表单
const profileForm = reactive({
  username: userStore.user?.username || '',
  email: userStore.user?.email || '',
  full_name: '',
  phone: '',
  department: '',
  position: ''
})

// 密码修改表单
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 密码表单验证
const isPasswordValid = computed(() => {
  return (
    passwordForm.currentPassword.length >= 6 &&
    passwordForm.newPassword.length >= 6 &&
    passwordForm.newPassword === passwordForm.confirmPassword
  )
})

// 获取用户资料
const fetchUserProfile = async () => {
  try {
    loading.value = true
    
    // 获取最新的用户信息
    await userStore.fetchUserInfo()
    
    // 获取用户资料
    await userStore.fetchUserProfile()
    
    // 更新表单数据
    profileForm.username = userStore.user?.username || ''
    profileForm.email = userStore.user?.email || ''
    
    if (userStore.userProfile) {
      profileForm.full_name = userStore.userProfile.full_name || ''
      profileForm.phone = userStore.userProfile.phone || ''
      profileForm.department = userStore.userProfile.department || ''
      profileForm.position = userStore.userProfile.position || ''
    }
  } catch (error) {
    console.error('获取用户资料失败:', error)
    alert('获取用户资料失败，请刷新页面重试')
  } finally {
    loading.value = false
  }
}

// 更新用户资料
const handleUpdateProfile = async () => {
  try {
    loading.value = true
    
    const profileData = {
      full_name: profileForm.full_name,
      phone: profileForm.phone,
      department: profileForm.department,
      position: profileForm.position
    }
    
    await userStore.updateUserProfile(profileData)
    alert('资料更新成功')
  } catch (error: any) {
    console.error('更新用户资料失败:', error)
    const errorMessage = userStore.error || '更新失败，请重试'
    alert(errorMessage)
  } finally {
    loading.value = false
  }
}

// 修改密码
const handleChangePassword = async () => {
  if (!isPasswordValid.value) {
    alert('请检查密码输入')
    return
  }

  try {
    passwordLoading.value = true
    
    const passwordData = {
      old_password: passwordForm.currentPassword,
      new_password: passwordForm.newPassword,
      confirm_password: passwordForm.confirmPassword
    }
    
    await userStore.changePassword(passwordData)
    alert('密码修改成功')
    
    // 清空密码表单
    passwordForm.currentPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
  } catch (error: any) {
    console.error('修改密码失败:', error)
    const errorMessage = userStore.error || '修改失败，请重试'
    alert(errorMessage)
  } finally {
    passwordLoading.value = false
  }
}

onMounted(() => {
  fetchUserProfile()
})
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  padding: 2rem;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.profile-box {
  width: 100%;
  max-width: 600px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
}

h3 {
  color: #333;
  margin: 2rem 0 1rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.profile-form,
.password-form {
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

input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.disabled-input {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.form-text {
  font-size: 0.875rem;
  color: #666;
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

button:hover {
  background-color: #357abd;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.password-section {
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 1rem;
  }

  .profile-box {
    padding: 1.5rem;
  }
}
</style> 