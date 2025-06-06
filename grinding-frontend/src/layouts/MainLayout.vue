<template>
  <div class="main-layout">
    <Navigation class="nav-sidebar" />
    <div class="main-wrapper">
      <!-- 顶部导航栏 -->
      <header class="top-header">
        <div class="header-left">
          <h2 class="page-title">滚磨光整加工数据库</h2>
        </div>
        <div class="header-right">
          <!-- 个人账户下拉菜单 -->
          <el-dropdown @command="handleMenuCommand">
            <span class="user-dropdown">
              <el-icon><User /></el-icon>
              <span class="username">{{ user?.username || 'administrator' }}</span>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="dashboard">
                  <el-icon><Monitor /></el-icon>
                  个人账户
                </el-dropdown-item>
                <el-dropdown-item command="profile">
                  <el-icon><UserFilled /></el-icon>
                  个人资料
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>
      
      <!-- 主内容区域 -->
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { User, ArrowDown, Monitor, UserFilled, SwitchButton } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { useAuthStore } from '@/stores/auth'
import Navigation from '@/components/Navigation.vue'

const router = useRouter()
const userStore = useUserStore()
const authStore = useAuthStore()

// 获取当前用户信息
const user = computed(() => userStore.user)

// 处理下拉菜单命令
const handleMenuCommand = async (command: string) => {
  switch (command) {
    case 'dashboard':
      router.push('/dashboard')
      break
    case 'profile':
      router.push('/profile')
      break
    case 'logout':
      try {
        await authStore.logout()
        router.push('/login')
      } catch (error) {
        console.error('登出失败:', error)
        alert('登出失败，请重试')
      }
      break
  }
}
</script>

<style scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
}

.nav-sidebar {
  flex-shrink: 0;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
}

.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 250px;
  position: relative;
  z-index: 1;
}

.top-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  padding: 0 24px;
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 100;
}

.header-left .page-title {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
  color: #333;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  cursor: pointer;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.user-dropdown:hover {
  background-color: #f5f7fa;
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.dropdown-icon {
  font-size: 12px;
  color: #666;
}

.main-content {
  flex: 1;
  padding: 2rem;
  background-color: #f5f5f5;
  overflow-y: auto;
  position: relative;
  z-index: 1;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .main-layout {
    flex-direction: column;
  }

  .nav-sidebar {
    position: relative;
    z-index: 1001;
  }

  .main-wrapper {
    margin-left: 0;
  }

  .main-content {
    padding: 1rem;
  }

  .top-header {
    padding: 0 16px;
  }

  .page-title {
    font-size: 16px !important;
  }
}
</style> 