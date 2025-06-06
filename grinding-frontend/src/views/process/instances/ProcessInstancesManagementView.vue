<template>
  <div class="process-instances-management-view">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-tasks"></i>
        工艺案例管理
      </h1>
      <p class="page-description">管理和维护工艺案例数据，支持案例的创建、编辑和分析</p>
    </div>

    <div class="development-notice">
      <div class="notice-card">
        <div class="notice-icon">
          <i class="fas fa-clipboard-check"></i>
        </div>
        <div class="notice-content">
          <h3>工艺案例管理功能开发中</h3>
          <p>工艺案例管理系统正在开发中，将为您提供完整的案例管理解决方案！</p>
          <div class="feature-list">
            <h4>即将推出的功能：</h4>
            <ul>
              <li><i class="fas fa-check-circle"></i> 案例数据全生命周期管理</li>
              <li><i class="fas fa-check-circle"></i> 案例分类和标签管理</li>
              <li><i class="fas fa-check-circle"></i> 案例效果评估和对比</li>
              <li><i class="fas fa-check-circle"></i> 案例知识提取和重用</li>
              <li><i class="fas fa-check-circle"></i> 智能案例推荐系统</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="placeholder-content">
      <el-card class="feature-preview" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>案例管理系统</span>
            <el-tag type="primary" size="small">开发中</el-tag>
          </div>
        </template>
        <div class="preview-grid">
          <div class="preview-item">
            <i class="fas fa-plus"></i>
            <h4>新建案例</h4>
            <p>创建新的工艺案例记录</p>
          </div>
          <div class="preview-item">
            <i class="fas fa-edit"></i>
            <h4>编辑案例</h4>
            <p>修改和完善现有案例</p>
          </div>
          <div class="preview-item">
            <i class="fas fa-chart-pie"></i>
            <h4>案例分析</h4>
            <p>深度分析案例效果</p>
          </div>
          <div class="preview-item">
            <i class="fas fa-share-alt"></i>
            <h4>案例共享</h4>
            <p>团队间案例知识共享</p>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

onMounted(() => {
  console.log('工艺案例管理页面已加载')
})
</script>

<style scoped>
.process-instances-management-view {
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

.preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  margin-top: 16px;
}

.preview-item {
  text-align: center;
  padding: 24px;
  border: 2px dashed #e1e8ed;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.preview-item:hover {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.preview-item i {
  font-size: 32px;
  color: #409eff;
  margin-bottom: 12px;
  display: block;
}

.preview-item h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #2c3e50;
}

.preview-item p {
  margin: 0;
  font-size: 14px;
  color: #666;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .process-instances-management-view {
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
  
  .preview-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}
</style> 