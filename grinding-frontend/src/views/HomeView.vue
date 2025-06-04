<template>
  <div class="home">
    <div class="hero">
      <div class="hero-content">
        <h1>磨削平台管理系统</h1>
        <p class="hero-subtitle">滚磨光整加工行业的智能化管理解决方案</p>
        <div class="hero-actions">
          <RouterLink to="/dashboard" class="btn btn-primary" v-if="userStore.isAuthenticated">
            进入控制台
          </RouterLink>
          <template v-else>
            <RouterLink to="/login" class="btn btn-primary">登录</RouterLink>
            <RouterLink to="/register" class="btn btn-secondary">注册</RouterLink>
          </template>
        </div>
      </div>
    </div>

    <section class="features">
      <div class="container">
        <h2>系统特色</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">👥</div>
            <h3>用户管理</h3>
            <p>支持多种用户类型，包括系统管理员、工艺工程师、设备操作员、质量检测员和企业管理员</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">⚙️</div>
            <h3>设备管理</h3>
            <p>全面的设备信息管理，包括设备状态监控、维护记录和性能分析</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>工艺数据</h3>
            <p>详细的工艺参数记录和分析，帮助优化生产流程和提高产品质量</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3>安全认证</h3>
            <p>基于JWT的安全认证机制，确保数据安全和用户权限管理</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
</script>

<style scoped>
.home {
  width: 100%;
}

.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 2rem;
  text-align: center;
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero-subtitle {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.features {
  padding: 4rem 0;
  background-color: #f8f9fa;
}

.features h2 {
  text-align: center;
  margin-bottom: 3rem;
  font-size: 2.5rem;
  color: #2c3e50;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.feature-card p {
  color: #7f8c8d;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style> 