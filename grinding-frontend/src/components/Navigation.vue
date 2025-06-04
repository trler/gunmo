<template>
  <nav class="navigation">
    <div class="nav-header">
      <h1 class="logo">滚磨光整加工平台</h1>
      <div class="user-info" v-if="user">
        <span class="username">{{ user.username }}</span>
        <span class="user-role">{{ userTypeDisplay }}</span>
      </div>
    </div>

    <div class="nav-menu">
      <!-- 系统管理员菜单 -->
      <template v-if="isSystemAdmin">
        <router-link to="/dashboard" class="nav-item">
          <i class="fas fa-tachometer-alt"></i>
          <span>仪表盘</span>
        </router-link>
        <router-link to="/system/settings" class="nav-item">
          <i class="fas fa-cogs"></i>
          <span>系统设置</span>
        </router-link>
        <router-link to="/system/users" class="nav-item">
          <i class="fas fa-users"></i>
          <span>用户管理</span>
        </router-link>
        <router-link to="/system/statistics" class="nav-item">
          <i class="fas fa-chart-bar"></i>
          <span>数据统计</span>
        </router-link>
      </template>

      <!-- 工艺工程师菜单 -->
      <template v-if="isProcessEngineer">
        <router-link to="/dashboard" class="nav-item">
          <i class="fas fa-tachometer-alt"></i>
          <span>仪表盘</span>
        </router-link>
        <router-link to="/process/library" class="nav-item">
          <i class="fas fa-book"></i>
          <span>工艺库</span>
        </router-link>
        <!-- TODO: 待添加的菜单项 -->
        <!-- <router-link to="/process/optimization" class="nav-item">
          <i class="fas fa-sliders-h"></i>
          <span>参数优化</span>
        </router-link>
        <router-link to="/process/cases" class="nav-item">
          <i class="fas fa-folder"></i>
          <span>案例管理</span>
        </router-link> -->
      </template>

      <!-- 设备操作员菜单 -->
      <template v-if="isEquipmentOperator">
        <router-link to="/dashboard" class="nav-item">
          <i class="fas fa-tachometer-alt"></i>
          <span>仪表盘</span>
        </router-link>
        <router-link to="/equipment/operation" class="nav-item">
          <i class="fas fa-cogs"></i>
          <span>设备操作</span>
        </router-link>
        <!-- TODO: 待添加的菜单项 -->
        <!-- <router-link to="/equipment/monitor" class="nav-item">
          <i class="fas fa-desktop"></i>
          <span>设备监控</span>
        </router-link>
        <router-link to="/equipment/records" class="nav-item">
          <i class="fas fa-history"></i>
          <span>运行记录</span>
        </router-link> -->
      </template>

      <!-- 质量检测员菜单 -->
      <template v-if="isQualityInspector">
        <router-link to="/dashboard" class="nav-item">
          <i class="fas fa-tachometer-alt"></i>
          <span>仪表盘</span>
        </router-link>
        <router-link to="/quality/inspection" class="nav-item">
          <i class="fas fa-clipboard-check"></i>
          <span>质量检测</span>
        </router-link>
        <!-- TODO: 待添加的菜单项 -->
        <!-- <router-link to="/quality/reports" class="nav-item">
          <i class="fas fa-file-alt"></i>
          <span>质量报告</span>
        </router-link> -->
      </template>

      <!-- 所有用户通用菜单 -->
      <router-link to="/profile" class="nav-item">
        <i class="fas fa-user"></i>
        <span>个人资料</span>
      </router-link>
      
      <button @click="handleLogout" class="nav-item logout-btn">
        <i class="fas fa-sign-out-alt"></i>
        <span>退出登录</span>
      </button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useAuthStore } from '@/stores/auth'
import type { UserType } from '@/types/auth'

const router = useRouter()
const userStore = useUserStore()
const authStore = useAuthStore()

// 获取当前用户信息
const user = computed(() => userStore.user)

// 用户类型显示文本
const userTypeDisplay = computed(() => {
  const typeMap: Record<UserType, string> = {
    system_admin: '系统管理员',
    process_engineer: '工艺工程师',
    equipment_operator: '设备操作员',
    quality_inspector: '质量检测员'
  }
  return user.value ? typeMap[user.value.user_type] : ''
})

// 角色判断计算属性
const isSystemAdmin = computed(() => user.value?.user_type === 'system_admin')
const isProcessEngineer = computed(() => user.value?.user_type === 'process_engineer')
const isEquipmentOperator = computed(() => user.value?.user_type === 'equipment_operator')
const isQualityInspector = computed(() => user.value?.user_type === 'quality_inspector')

// 处理登出
const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('登出失败:', error)
    alert('登出失败，请重试')
  }
}
</script>

<style scoped>
.navigation {
  width: 250px;
  height: 100vh;
  background-color: #2c3e50;
  color: #fff;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
}

.nav-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 1rem;
  color: #fff;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.username {
  font-weight: 500;
}

.user-role {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
}

.nav-menu {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.2s;
  gap: 0.75rem;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.nav-item.router-link-active {
  background-color: rgba(255, 255, 255, 0.15);
  color: #fff;
  border-left: 4px solid #42b983;
}

.nav-item i {
  width: 1.25rem;
  text-align: center;
}

.logout-btn {
  width: 100%;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.8);
  margin-top: auto;
}

.logout-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}

@media (max-width: 768px) {
  .navigation {
    width: 100%;
    height: auto;
    position: relative;
  }

  .nav-menu {
    display: flex;
    flex-wrap: wrap;
    padding: 0.5rem;
  }

  .nav-item {
    padding: 0.5rem 1rem;
    flex: 1 1 auto;
  }
}
</style> 