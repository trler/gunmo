<template>
  <div class="process-template-view">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-th-large"></i>
        工序模板
      </h1>
      <p class="page-description">标准化工序模板管理，提高工艺设计效率</p>
    </div>

    <div class="development-notice">
      <div class="notice-card">
        <div class="notice-icon">
          <i class="fas fa-clipboard-list"></i>
        </div>
        <div class="notice-content">
          <h3>工序模板功能开发中</h3>
          <p>工序模板管理系统正在构建中，将提供标准化的工序设计解决方案！</p>
          <div class="feature-list">
            <h4>即将推出的功能：</h4>
            <ul>
              <li><i class="fas fa-check-circle"></i> 模板库管理</li>
              <li><i class="fas fa-check-circle"></i> 自定义模板设计</li>
              <li><i class="fas fa-check-circle"></i> 模板快速应用</li>
              <li><i class="fas fa-check-circle"></i> 版本控制管理</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="placeholder-content">
      <el-card class="feature-preview" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>工序模板系统</span>
            <el-tag type="primary" size="small">开发中</el-tag>
          </div>
        </template>
        <div class="preview-text">
          <p>工序模板将帮助您快速构建标准化的工艺流程，提升设计效率。</p>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

onMounted(() => {
  console.log('工序模板页面已加载')
})
</script>

<style scoped>
.process-template-view {
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

.feature-list h4 {
  font-size: 16px;
  margin: 0 0 12px 0;
  font-weight: 500;
}

.feature-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 14px;
}

.feature-list li i {
  color: #4CAF50;
  font-size: 12px;
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
  .process-template-view {
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