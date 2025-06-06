<template>
  <div class="process-cases-view">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-database"></i>
        工艺实例数据库
      </h1>
      <p class="page-description">管理和查看滚磨光整加工的工艺实例数据</p>
    </div>

    <div class="development-notice">
      <div class="notice-card">
        <div class="notice-icon">
          <i class="fas fa-tools"></i>
        </div>
        <div class="notice-content">
          <h3>功能开发中</h3>
          <p>工艺实例数据库功能正在紧张开发中，敬请期待！</p>
          <div class="feature-list">
            <h4>即将推出的功能：</h4>
            <ul>
              <li><i class="fas fa-check-circle"></i> 工艺实例数据录入与管理</li>
              <li><i class="fas fa-check-circle"></i> 工艺参数智能推荐</li>
              <li><i class="fas fa-check-circle"></i> 实例数据查询与筛选</li>
              <li><i class="fas fa-check-circle"></i> 工艺效果评估分析</li>
              <li><i class="fas fa-check-circle"></i> 历史数据对比功能</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="placeholder-content">
      <el-card class="feature-preview" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>功能预览</span>
            <el-tag type="warning" size="small">开发中</el-tag>
          </div>
        </template>
        <div class="preview-grid">
          <div class="preview-item">
            <i class="fas fa-plus-circle"></i>
            <h4>新建工艺实例</h4>
            <p>快速创建新的工艺实例记录</p>
          </div>
          <div class="preview-item">
            <i class="fas fa-search"></i>
            <h4>智能搜索</h4>
            <p>基于多条件的工艺实例搜索</p>
          </div>
          <div class="preview-item">
            <i class="fas fa-chart-line"></i>
            <h4>数据分析</h4>
            <p>工艺参数趋势分析与优化建议</p>
          </div>
          <div class="preview-item">
            <i class="fas fa-download"></i>
            <h4>数据导出</h4>
            <p>支持多种格式的数据导出功能</p>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

onMounted(() => {
  console.log('工艺实例数据库页面已加载')
})
</script>

<style scoped>
.process-cases-view {
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
  .process-cases-view {
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