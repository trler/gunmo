<template>
  <div class="process-analysis-statistics">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-chart-line"></i>
        工艺分析报表
      </h1>
      <p class="page-description">分析工艺执行效果和性能指标</p>
    </div>

    <!-- 快速筛选 -->
    <el-card class="filter-card" shadow="never">
      <el-form :model="filterForm" :inline="true" class="filter-form">
        <el-form-item label="分析周期">
          <el-select v-model="filterForm.period" @change="loadData">
            <el-option label="本周" value="week" />
            <el-option label="本月" value="month" />
            <el-option label="本季度" value="quarter" />
            <el-option label="本年" value="year" />
          </el-select>
        </el-form-item>
        <el-form-item label="工艺类型">
          <el-select v-model="filterForm.processType" clearable @change="loadData">
            <el-option label="表面处理" value="surface" />
            <el-option label="精度加工" value="precision" />
            <el-option label="去毛刺" value="deburring" />
            <el-option label="抛光" value="polishing" />
          </el-select>
        </el-form-item>
        <el-form-item label="设备类型">
          <el-select v-model="filterForm.equipmentType" clearable @change="loadData">
            <el-option label="振动研磨机" value="vibration" />
            <el-option label="离心研磨机" value="centrifugal" />
            <el-option label="流动研磨机" value="flow" />
          </el-select>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 关键指标 -->
    <div class="stats-overview">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stats-card primary">
            <div class="stats-content">
              <div class="stats-number">{{ processCount }}</div>
              <div class="stats-label">工艺执行次数</div>
            </div>
            <div class="stats-icon">
              <i class="fas fa-cogs"></i>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stats-card success">
            <div class="stats-content">
              <div class="stats-number">{{ successRate }}%</div>
              <div class="stats-label">成功率</div>
            </div>
            <div class="stats-icon">
              <i class="fas fa-check-circle"></i>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stats-card warning">
            <div class="stats-content">
              <div class="stats-number">{{ avgTime }}h</div>
              <div class="stats-label">平均处理时间</div>
            </div>
            <div class="stats-icon">
              <i class="fas fa-clock"></i>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stats-card info">
            <div class="stats-content">
              <div class="stats-number">{{ qualityScore }}</div>
              <div class="stats-label">质量评分</div>
            </div>
            <div class="stats-icon">
              <i class="fas fa-star"></i>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 图表分析 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <span>工艺效率趋势</span>
          </template>
          <div id="efficiencyChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <span>质量分布</span>
          </template>
          <div id="qualityChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <span>设备使用率分析</span>
          </template>
          <div id="equipmentChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 详细分析表 -->
    <el-card class="table-card" style="margin-top: 20px;">
      <template #header>
        <div class="table-header">
          <span>工艺分析详情</span>
          <div>
            <el-button type="primary" @click="generateReport">
              <i class="fas fa-file-alt"></i>
              生成报告
            </el-button>
            <el-button @click="exportData">
              <i class="fas fa-download"></i>
              导出数据
            </el-button>
          </div>
        </div>
      </template>
      <el-table :data="analysisData" v-loading="loading" border>
        <el-table-column prop="processName" label="工艺名称" width="150" />
        <el-table-column prop="executionCount" label="执行次数" width="100" />
        <el-table-column prop="successRate" label="成功率" width="100">
          <template #default="{ row }">
            <el-tag :type="row.successRate >= 90 ? 'success' : row.successRate >= 70 ? 'warning' : 'danger'">
              {{ row.successRate }}%
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="avgProcessTime" label="平均时间(h)" width="120" />
                 <el-table-column prop="qualityScore" label="质量评分" width="100">
           <template #default="{ row }">
             <el-rate :model-value="row.qualityScore" disabled show-score :max="5" />
           </template>
         </el-table-column>
        <el-table-column prop="efficiency" label="效率指标" width="100">
          <template #default="{ row }">
            <el-progress :percentage="row.efficiency" :show-text="false" />
            <span style="margin-left: 10px;">{{ row.efficiency }}%</span>
          </template>
        </el-table-column>
        <el-table-column prop="costPerUnit" label="单位成本" width="100" />
        <el-table-column prop="lastUpdate" label="最后更新" width="150" />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewDetails(row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 响应式数据
const loading = ref(false)
const processCount = ref(234)
const successRate = ref(92)
const avgTime = ref(2.5)
const qualityScore = ref(4.3)
const analysisData = ref([])

// 筛选表单
const filterForm = ref({
  period: 'month',
  processType: '',
  equipmentType: ''
})

// 方法
const loadData = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 模拟数据
    analysisData.value = [
      {
        processName: '表面抛光工艺A',
        executionCount: 45,
        successRate: 95,
        avgProcessTime: 2.3,
        qualityScore: 4.5,
        efficiency: 89,
        costPerUnit: '¥12.50',
        lastUpdate: '2024-01-15 14:30'
      },
      {
        processName: '精密去毛刺B',
        executionCount: 38,
        successRate: 88,
        avgProcessTime: 1.8,
        qualityScore: 4.2,
        efficiency: 76,
        costPerUnit: '¥8.30',
        lastUpdate: '2024-01-14 16:45'
      },
      {
        processName: '表面纹理处理C',
        executionCount: 52,
        successRate: 92,
        avgProcessTime: 3.1,
        qualityScore: 4.1,
        efficiency: 82,
        costPerUnit: '¥15.20',
        lastUpdate: '2024-01-13 09:15'
      }
    ]
    
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const generateReport = () => {
  ElMessage.success('报告生成功能开发中')
}

const exportData = () => {
  ElMessage.success('数据导出功能开发中')
}

const viewDetails = (row: any) => {
  ElMessage.info(`查看 ${row.processName} 的详细信息`)
}

const initCharts = () => {
  console.log('初始化工艺分析图表...')
}

// 生命周期
onMounted(() => {
  loadData()
  initCharts()
})
</script>

<style scoped>
.process-analysis-statistics {
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

.filter-card {
  margin-bottom: 24px;
}

.stats-overview {
  margin-bottom: 24px;
}

.stats-card {
  padding: 20px;
  position: relative;
  overflow: hidden;
  border-left: 4px solid #409eff;
}

.stats-card.primary {
  border-left-color: #409eff;
}

.stats-card.success {
  border-left-color: #67c23a;
}

.stats-card.warning {
  border-left-color: #e6a23c;
}

.stats-card.info {
  border-left-color: #909399;
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

.chart-card {
  margin-bottom: 20px;
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