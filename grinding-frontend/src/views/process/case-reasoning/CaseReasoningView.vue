<template>
  <div class="case-reasoning-view">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-brain"></i>
        案例推理系统
      </h1>
      <div class="header-subtitle">
        基于案例的智能推理与决策支持系统
      </div>
    </div>

    <!-- 功能模块导航 -->
    <div class="module-grid">
      <div class="module-card" @click="navigateToFeatureEntry">
        <div class="module-icon">
          <i class="fas fa-edit"></i>
        </div>
        <div class="module-content">
          <h3 class="module-title">案例特征录入</h3>
          <p class="module-description">录入新的案例特征信息，建立案例数据库</p>
          <div class="module-stats">
            <span class="stat-item">
              <i class="fas fa-database"></i>
              案例数: {{ caseStats.totalCases }}
            </span>
          </div>
        </div>
        <div class="module-arrow">
          <i class="fas fa-chevron-right"></i>
        </div>
      </div>

      <div class="module-card" @click="navigateToSimilarityCalculation">
        <div class="module-icon">
          <i class="fas fa-calculator"></i>
        </div>
        <div class="module-content">
          <h3 class="module-title">相似度计算</h3>
          <p class="module-description">计算案例间的相似度，支持多种算法</p>
          <div class="module-stats">
            <span class="stat-item">
              <i class="fas fa-chart-line"></i>
              算法: {{ caseStats.algorithms }}种
            </span>
          </div>
        </div>
        <div class="module-arrow">
          <i class="fas fa-chevron-right"></i>
        </div>
      </div>

      <div class="module-card" @click="navigateToRetrieval">
        <div class="module-icon">
          <i class="fas fa-search"></i>
        </div>
        <div class="module-content">
          <h3 class="module-title">案例检索</h3>
          <p class="module-description">快速检索相似案例，支持多维度搜索</p>
          <div class="module-stats">
            <span class="stat-item">
              <i class="fas fa-clock"></i>
              平均检索时间: {{ caseStats.avgSearchTime }}ms
            </span>
          </div>
        </div>
        <div class="module-arrow">
          <i class="fas fa-chevron-right"></i>
        </div>
      </div>

      <div class="module-card" @click="navigateToRecommendation">
        <div class="module-icon">
          <i class="fas fa-lightbulb"></i>
        </div>
        <div class="module-content">
          <h3 class="module-title">推理推荐</h3>
          <p class="module-description">基于相似案例进行智能推理和推荐</p>
          <div class="module-stats">
            <span class="stat-item">
              <i class="fas fa-thumbs-up"></i>
              推荐准确率: {{ caseStats.accuracy }}%
            </span>
          </div>
        </div>
        <div class="module-arrow">
          <i class="fas fa-chevron-right"></i>
        </div>
      </div>
    </div>

    <!-- 系统状态概览 -->
    <div class="system-overview">
      <h2 class="overview-title">系统概览</h2>
      <div class="overview-grid">
        <div class="overview-card">
          <div class="overview-icon">
            <i class="fas fa-database"></i>
          </div>
          <div class="overview-content">
            <div class="overview-number">{{ caseStats.totalCases }}</div>
            <div class="overview-label">总案例数</div>
          </div>
        </div>

        <div class="overview-card">
          <div class="overview-icon">
            <i class="fas fa-search"></i>
          </div>
          <div class="overview-content">
            <div class="overview-number">{{ caseStats.todaySearches }}</div>
            <div class="overview-label">今日检索次数</div>
          </div>
        </div>

        <div class="overview-card">
          <div class="overview-icon">
            <i class="fas fa-chart-line"></i>
          </div>
          <div class="overview-content">
            <div class="overview-number">{{ caseStats.accuracy }}%</div>
            <div class="overview-label">推荐准确率</div>
          </div>
        </div>

        <div class="overview-card">
          <div class="overview-icon">
            <i class="fas fa-clock"></i>
          </div>
          <div class="overview-content">
            <div class="overview-number">{{ caseStats.avgSearchTime }}</div>
            <div class="overview-label">平均响应时间(ms)</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 最近案例活动 -->
    <div class="recent-activities">
      <h2 class="activities-title">最近案例活动</h2>
      <div class="activities-list">
        <div 
          v-for="activity in recentActivities" 
          :key="activity.id"
          class="activity-item"
        >
          <div class="activity-icon">
            <i :class="activity.icon"></i>
          </div>
          <div class="activity-content">
            <div class="activity-action">{{ activity.action }}</div>
            <div class="activity-description">{{ activity.description }}</div>
            <div class="activity-time">{{ activity.time }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 系统统计数据
const caseStats = reactive({
  totalCases: 1247,
  algorithms: 5,
  avgSearchTime: 180,
  accuracy: 92,
  todaySearches: 68
})

// 最近活动数据
const recentActivities = ref([
  {
    id: 1,
    icon: 'fas fa-plus-circle text-success',
    action: '新增案例',
    description: '添加了钛合金齿轮件的加工案例',
    time: '2分钟前'
  },
  {
    id: 2,
    icon: 'fas fa-search text-primary',
    action: '案例检索',
    description: '搜索了轴承件相关的加工案例',
    time: '5分钟前'
  },
  {
    id: 3,
    icon: 'fas fa-lightbulb text-warning',
    action: '推理推荐',
    description: '为叶片件推荐了最佳加工参数',
    time: '10分钟前'
  },
  {
    id: 4,
    icon: 'fas fa-edit text-info',
    action: '案例修改',
    description: '更新了不锈钢材质的加工参数',
    time: '15分钟前'
  }
])

// 导航方法
const navigateToFeatureEntry = () => {
  router.push('/process/case-reasoning/feature-entry')
  ElMessage.success('进入案例特征录入')
}

const navigateToSimilarityCalculation = () => {
  ElMessage.info('相似度计算模块开发中...')
}

const navigateToRetrieval = () => {
  ElMessage.info('案例检索模块开发中...')
}

const navigateToRecommendation = () => {
  ElMessage.info('推理推荐模块开发中...')
}

// 更新统计数据
const updateStats = () => {
  // 模拟实时数据更新
  const randomVariation = () => Math.floor(Math.random() * 5) - 2
  
  caseStats.todaySearches += Math.max(0, randomVariation())
  caseStats.avgSearchTime += randomVariation() * 10
  caseStats.accuracy = Math.min(100, Math.max(80, caseStats.accuracy + randomVariation() * 0.1))
}

onMounted(() => {
  console.log('案例推理系统主页已加载')
  
  // 定期更新统计数据
  setInterval(updateStats, 30000) // 每30秒更新一次
})
</script>

<style scoped>
.case-reasoning-view {
  padding: 24px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 40px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 12px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.header-subtitle {
  font-size: 16px;
  opacity: 0.9;
  font-weight: 300;
}

.module-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.module-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 20px;
  position: relative;
  overflow: hidden;
}

.module-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.module-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.module-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  flex-shrink: 0;
}

.module-content {
  flex: 1;
}

.module-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.module-description {
  color: #64748b;
  margin: 0 0 12px 0;
  line-height: 1.5;
}

.module-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #8b5cf6;
  font-weight: 500;
}

.module-arrow {
  color: #cbd5e1;
  font-size: 18px;
  flex-shrink: 0;
}

.system-overview {
  margin-bottom: 40px;
}

.overview-title {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 24px 0;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.overview-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 16px;
}

.overview-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
}

.overview-number {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1;
}

.overview-label {
  font-size: 14px;
  color: #64748b;
  margin-top: 4px;
}

.recent-activities {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.activities-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 20px 0;
}

.activities-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.activity-item:hover {
  background: #f1f5f9;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.activity-action {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
}

.activity-description {
  color: #64748b;
  font-size: 14px;
  margin-bottom: 4px;
}

.activity-time {
  color: #94a3b8;
  font-size: 12px;
}

.text-success {
  color: #10b981 !important;
}

.text-primary {
  color: #3b82f6 !important;
}

.text-warning {
  color: #f59e0b !important;
}

.text-info {
  color: #06b6d4 !important;
}

@media (max-width: 768px) {
  .case-reasoning-view {
    padding: 16px;
  }
  
  .module-grid {
    grid-template-columns: 1fr;
  }
  
  .overview-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .module-card {
    padding: 20px;
  }
  
  .page-title {
    font-size: 24px;
  }
}
</style> 