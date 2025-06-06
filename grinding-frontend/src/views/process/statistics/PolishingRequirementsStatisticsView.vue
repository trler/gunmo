<template>
  <div class="polishing-requirements-statistics">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-chart-bar"></i>
        光整需求统计
      </h1>
      <p class="page-description">分析和统计光整需求的相关数据</p>
    </div>

    <!-- 统计概览卡片 -->
    <div class="stats-overview">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-number">{{ totalRequirements }}</div>
              <div class="stats-label">总需求数</div>
            </div>
            <div class="stats-icon">
              <i class="fas fa-clipboard-list"></i>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-number">{{ pendingRequirements }}</div>
              <div class="stats-label">待处理</div>
            </div>
            <div class="stats-icon">
              <i class="fas fa-clock"></i>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-number">{{ completedRequirements }}</div>
              <div class="stats-label">已完成</div>
            </div>
            <div class="stats-icon">
              <i class="fas fa-check-circle"></i>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-number">{{ completionRate }}%</div>
              <div class="stats-label">完成率</div>
            </div>
            <div class="stats-icon">
              <i class="fas fa-percentage"></i>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 筛选条件 -->
    <el-card class="filter-card" shadow="never">
      <el-form :model="filterForm" :inline="true" class="filter-form">
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            @change="loadStatistics"
          />
        </el-form-item>
        <el-form-item label="需求类型">
          <el-select v-model="filterForm.type" placeholder="选择类型" clearable @change="loadStatistics">
            <el-option label="表面光整" value="surface" />
            <el-option label="边缘去毛刺" value="deburring" />
            <el-option label="精度提升" value="precision" />
            <el-option label="表面纹理" value="texture" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filterForm.status" placeholder="选择状态" clearable @change="loadStatistics">
            <el-option label="待处理" value="pending" />
            <el-option label="处理中" value="processing" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadStatistics">
            <i class="fas fa-search"></i>
            查询
          </el-button>
          <el-button @click="resetFilter">
            <i class="fas fa-undo"></i>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 图表区域 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <span>需求类型分布</span>
          </template>
          <div id="typeChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <span>月度需求趋势</span>
          </template>
          <div id="trendChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <span>需求处理状态统计</span>
          </template>
          <div id="statusChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 详细数据表格 -->
    <el-card class="table-card" style="margin-top: 20px;">
      <template #header>
        <div class="table-header">
          <span>统计详情</span>
          <el-button type="primary" @click="exportData">
            <i class="fas fa-download"></i>
            导出数据
          </el-button>
        </div>
      </template>
      <el-table :data="statisticsData" v-loading="loading" border>
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="type" label="需求类型" width="120" />
        <el-table-column prop="total" label="总数" width="80" />
        <el-table-column prop="pending" label="待处理" width="80" />
        <el-table-column prop="processing" label="处理中" width="80" />
        <el-table-column prop="completed" label="已完成" width="80" />
        <el-table-column prop="cancelled" label="已取消" width="80" />
        <el-table-column prop="completionRate" label="完成率" width="100">
          <template #default="{ row }">
            <el-progress :percentage="row.completionRate" :show-text="false" />
            <span style="margin-left: 10px;">{{ row.completionRate }}%</span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'

// 响应式数据
const loading = ref(false)
const totalRequirements = ref(156)
const pendingRequirements = ref(23)
const completedRequirements = ref(120)
const statisticsData = ref([])

// 筛选表单
const filterForm = ref({
  dateRange: null,
  type: '',
  status: ''
})

// 计算属性
const completionRate = computed(() => {
  if (totalRequirements.value === 0) return 0
  return Math.round((completedRequirements.value / totalRequirements.value) * 100)
})

// 方法
const loadStatistics = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 模拟数据
    statisticsData.value = [
      {
        date: '2024-01-01',
        type: '表面光整',
        total: 45,
        pending: 5,
        processing: 8,
        completed: 30,
        cancelled: 2,
        completionRate: 67
      },
      {
        date: '2024-01-02',
        type: '边缘去毛刺',
        total: 38,
        pending: 3,
        processing: 6,
        completed: 27,
        cancelled: 2,
        completionRate: 71
      },
      {
        date: '2024-01-03',
        type: '精度提升',
        total: 52,
        pending: 8,
        processing: 12,
        completed: 30,
        cancelled: 2,
        completionRate: 58
      },
      {
        date: '2024-01-04',
        type: '表面纹理',
        total: 21,
        pending: 7,
        processing: 4,
        completed: 33,
        cancelled: 1,
        completionRate: 76
      }
    ]
    
    ElMessage.success('统计数据加载成功')
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.error('加载统计数据失败')
  } finally {
    loading.value = false
  }
}

const resetFilter = () => {
  filterForm.value = {
    dateRange: null,
    type: '',
    status: ''
  }
  loadStatistics()
}

const exportData = () => {
  ElMessage.success('数据导出功能开发中')
}

const initCharts = () => {
  // 这里可以初始化ECharts图表
  console.log('初始化图表...')
}

// 生命周期
onMounted(() => {
  loadStatistics()
  initCharts()
})
</script>

<style scoped>
.polishing-requirements-statistics {
  padding: 24px;
  background-color: #f5f7fa;
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

.stats-overview {
  margin-bottom: 24px;
}

.stats-card {
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.stats-content {
  position: relative;
  z-index: 2;
}

.stats-number {
  font-size: 32px;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 8px;
}

.stats-label {
  font-size: 14px;
  color: #666;
}

.stats-icon {
  position: absolute;
  right: 20px;
  top: 20px;
  font-size: 48px;
  color: rgba(64, 158, 255, 0.1);
}

.filter-card {
  margin-bottom: 24px;
}

.filter-form {
  margin: 0;
}

.chart-card {
  margin-bottom: 20px;
}

.table-card {
  background: white;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

:deep(.el-card__body) {
  padding: 20px;
}
</style> 