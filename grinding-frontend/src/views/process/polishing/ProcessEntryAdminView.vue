<template>
  <div class="process-entry-admin-view">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-user-shield"></i>
        光整工艺录入(管理员)
      </h1>
      <p class="page-description">管理员专用的光整工艺录入界面，拥有完整的系统管理权限</p>
    </div>

    <div class="development-notice">
      <div class="notice-card">
        <div class="notice-icon">
          <i class="fas fa-shield-alt"></i>
        </div>
        <div class="notice-content">
          <h3>管理员录入功能开发中</h3>
          <p>专为管理员设计的工艺录入系统正在开发中，将提供全面的管理功能！</p>
        </div>
      </div>
    </div>

    <div class="placeholder-content">
      <el-card class="feature-preview" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>管理员录入系统</span>
            <el-tag type="danger" size="small">开发中</el-tag>
          </div>
        </template>
        <div class="preview-text">
          <p>管理员工艺录入界面，提供高级权限管理和系统配置功能。</p>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

onMounted(() => {
  console.log('光整工艺录入(管理员)页面已加载')
})
</script>

<style scoped>
.process-entry-admin-view {
  padding: 24px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 24px;
  padding: 24px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title i {
  color: #409eff;
}

.page-description {
  color: #666;
  margin: 0;
  font-size: 14px;
}

.development-notice {
  margin-bottom: 24px;
}

.notice-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 32px;
  border-radius: 12px;
  display: flex;
  align-items: flex-start;
  gap: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.notice-icon {
  font-size: 48px;
  opacity: 0.9;
}

.notice-content h3 {
  font-size: 24px;
  margin: 0 0 12px 0;
  font-weight: 600;
}

.notice-content p {
  font-size: 16px;
  margin: 0 0 24px 0;
  opacity: 0.9;
}

.placeholder-content {
  margin-top: 24px;
}

.feature-preview {
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.preview-text {
  padding: 16px 0;
  text-align: center;
  color: #666;
}

@media (max-width: 768px) {
  .process-entry-admin-view {
    padding: 16px;
  }
  
  .notice-card {
    flex-direction: column;
    text-align: center;
    padding: 24px;
  }
  
  .notice-icon {
    font-size: 36px;
  }
}
</style> 