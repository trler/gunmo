<template>
  <div class="dashboard">
    <h1 class="page-title">仪表盘</h1>
    
    <!-- 用户欢迎信息 -->
    <div class="welcome-card">
      <h2>欢迎回来，{{ user?.username }}</h2>
      <p class="user-role">{{ userRoleDisplay }}</p>
    </div>

    <!-- 系统概览卡片 -->
    <div class="dashboard-grid">
      <!-- 系统管理员概览 -->
      <template v-if="isSystemAdmin">
        <div class="stat-card">
          <i class="fas fa-users"></i>
          <div class="stat-info">
            <h3>用户总数</h3>
            <p class="stat-value">{{ stats.userCount || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <i class="fas fa-desktop"></i>
          <div class="stat-info">
            <h3>设备总数</h3>
            <p class="stat-value">{{ stats.equipmentCount || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <i class="fas fa-chart-line"></i>
          <div class="stat-info">
            <h3>工艺数据</h3>
            <p class="stat-value">{{ stats.processDataCount || 0 }}</p>
          </div>
        </div>
      </template>

      <!-- 工艺工程师概览 -->
      <template v-if="isProcessEngineer">
        <div class="stat-card">
          <i class="fas fa-book"></i>
          <div class="stat-info">
            <h3>工艺库</h3>
            <p class="stat-value">{{ stats.processLibraryCount || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <i class="fas fa-sliders-h"></i>
          <div class="stat-info">
            <h3>优化方案</h3>
            <p class="stat-value">{{ stats.optimizationCount || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <i class="fas fa-folder"></i>
          <div class="stat-info">
            <h3>案例数量</h3>
            <p class="stat-value">{{ stats.caseCount || 0 }}</p>
          </div>
        </div>
      </template>

      <!-- 设备操作员概览 -->
      <template v-if="isEquipmentOperator">
        <div class="stat-card">
          <i class="fas fa-desktop"></i>
          <div class="stat-info">
            <h3>在线设备</h3>
            <p class="stat-value">{{ stats.onlineEquipmentCount || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <i class="fas fa-history"></i>
          <div class="stat-info">
            <h3>今日运行</h3>
            <p class="stat-value">{{ stats.todayOperationCount || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <i class="fas fa-exclamation-triangle"></i>
          <div class="stat-info">
            <h3>待处理告警</h3>
            <p class="stat-value">{{ stats.pendingAlerts || 0 }}</p>
          </div>
        </div>
      </template>

      <!-- 质量检测员概览 -->
      <template v-if="isQualityInspector">
        <div class="stat-card">
          <i class="fas fa-file-alt"></i>
          <div class="stat-info">
            <h3>质量报告</h3>
            <p class="stat-value">{{ stats.qualityReportCount || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <i class="fas fa-clipboard-check"></i>
          <div class="stat-info">
            <h3>待检批次</h3>
            <p class="stat-value">{{ stats.pendingInspections || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <i class="fas fa-chart-pie"></i>
          <div class="stat-info">
            <h3>合格率</h3>
            <p class="stat-value">{{ stats.qualityRate || '0%' }}</p>
          </div>
        </div>
      </template>
    </div>

    <!-- 最近活动 -->
    <div class="recent-activities">
      <h2>最近活动</h2>
      <div class="activity-list">
        <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
          <i :class="activity.icon"></i>
          <div class="activity-info">
            <p class="activity-text">{{ activity.text }}</p>
            <span class="activity-time">{{ activity.time }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import type { UserType } from '@/types/auth'

const userStore = useUserStore()
const user = computed(() => userStore.user)

// 用户角色显示文本
const userRoleDisplay = computed(() => {
  const typeMap: Record<UserType, string> = {
    system_admin: '系统管理员',
    process_engineer: '工艺工程师',
    equipment_operator: '设备操作员',
    quality_inspector: '质量检测员'
  }
  return user.value ? typeMap[user.value.user_type] : ''
})

// 角色判断
const isSystemAdmin = computed(() => user.value?.user_type === 'system_admin')
const isProcessEngineer = computed(() => user.value?.user_type === 'process_engineer')
const isEquipmentOperator = computed(() => user.value?.user_type === 'equipment_operator')
const isQualityInspector = computed(() => user.value?.user_type === 'quality_inspector')

// 统计数据
const stats = ref({
  // 系统管理员统计
  userCount: 0,
  equipmentCount: 0,
  processDataCount: 0,
  
  // 工艺工程师统计
  processLibraryCount: 0,
  optimizationCount: 0,
  caseCount: 0,
  
  // 设备操作员统计
  onlineEquipmentCount: 0,
  todayOperationCount: 0,
  pendingAlerts: 0,
  
  // 质量检测员统计
  qualityReportCount: 0,
  pendingInspections: 0,
  qualityRate: '0%'
})

// 最近活动
const recentActivities = ref([
  {
    id: 1,
    icon: 'fas fa-sign-in-alt',
    text: '用户登录系统',
    time: '刚刚'
  },
  {
    id: 2,
    icon: 'fas fa-file-alt',
    text: '更新了个人资料',
    time: '10分钟前'
  }
])

// 获取仪表盘数据
const fetchDashboardData = async () => {
  try {
    const data = await userStore.fetchDashboardData()
    // 根据用户角色更新统计数据
    if (isSystemAdmin.value) {
      stats.value = {
        ...stats.value,
        equipmentCount: data.equipment?.length || 0,
        processDataCount: data.processData?.length || 0,
        // 系统管理员需要单独获取用户数据
        userCount: 0 // 暂时设置为0，需要后端提供用户统计接口
      }
    } else if (isProcessEngineer.value) {
      stats.value = {
        ...stats.value,
        processLibraryCount: data.processData?.filter(p => p.type === 'library')?.length || 0,
        optimizationCount: data.processData?.filter(p => p.type === 'optimization')?.length || 0,
        caseCount: data.processData?.filter(p => p.type === 'case')?.length || 0
      }
    } else if (isEquipmentOperator.value) {
      stats.value = {
        ...stats.value,
        onlineEquipmentCount: data.equipment?.filter(e => e.status === 'online')?.length || 0,
        todayOperationCount: data.processData?.filter(p => {
          const today = new Date()
          const processDate = new Date(p.created_at)
          return processDate.toDateString() === today.toDateString()
        })?.length || 0,
        pendingAlerts: data.equipment?.filter(e => e.status === 'alert')?.length || 0
      }
    } else if (isQualityInspector.value) {
      stats.value = {
        ...stats.value,
        qualityReportCount: data.processData?.filter(p => p.type === 'quality_report')?.length || 0,
        pendingInspections: data.processData?.filter(p => p.type === 'inspection' && p.status === 'pending')?.length || 0,
        qualityRate: calculateQualityRate(data.processData || [])
      }
    }
  } catch (error) {
    console.error('获取仪表盘数据失败:', error)
  }
}

// 计算质量合格率
const calculateQualityRate = (processData: any[]): string => {
  const qualityReports = processData.filter(p => p.type === 'quality_report')
  if (qualityReports.length === 0) return '0%'
  
  const passedCount = qualityReports.filter(p => p.result === 'passed').length
  const rate = (passedCount / qualityReports.length) * 100
  return `${rate.toFixed(1)}%`
}

onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
.dashboard {
  padding: 1rem;
}

.page-title {
  font-size: 1.75rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.welcome-card {
  background: linear-gradient(135deg, #42b983 0%, #33a06f 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.welcome-card h2 {
  margin: 0;
  font-size: 1.5rem;
}

.user-role {
  margin: 0.5rem 0 0;
  opacity: 0.9;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-card i {
  font-size: 2rem;
  color: #42b983;
  width: 2.5rem;
  text-align: center;
}

.stat-info h3 {
  margin: 0;
  font-size: 1rem;
  color: #666;
}

.stat-value {
  margin: 0.25rem 0 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.recent-activities {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.recent-activities h2 {
  margin: 0 0 1rem;
  font-size: 1.25rem;
  color: #2c3e50;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: 4px;
  background: #f8f9fa;
}

.activity-item i {
  color: #42b983;
  width: 1.5rem;
  text-align: center;
}

.activity-info {
  flex: 1;
}

.activity-text {
  margin: 0;
  color: #2c3e50;
}

.activity-time {
  font-size: 0.875rem;
  color: #666;
}

@media (max-width: 768px) {
  .dashboard {
    padding: 0.5rem;
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 1rem;
  }
}
</style> 