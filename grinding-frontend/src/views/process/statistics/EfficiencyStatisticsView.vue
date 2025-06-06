<template>
  <div class="efficiency-statistics">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-tachometer-alt"></i>
        效率统计报表
      </h1>
      <p class="page-description">分析设备和工艺的效率指标</p>
    </div>

    <!-- 效率概览 -->
    <div class="stats-overview">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-number">{{ overallEfficiency }}%</div>
              <div class="stats-label">整体效率</div>
            </div>
            <div class="stats-icon">
              <i class="fas fa-gauge-high"></i>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-number">{{ equipmentUtilization }}%</div>
              <div class="stats-label">设备利用率</div>
            </div>
            <div class="stats-icon">
              <i class="fas fa-cogs"></i>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-number">{{ energyEfficiency }}%</div>
              <div class="stats-label">能耗效率</div>
            </div>
            <div class="stats-icon">
              <i class="fas fa-bolt"></i>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-number">{{ timeEfficiency }}%</div>
              <div class="stats-label">时间效率</div>
            </div>
            <div class="stats-icon">
              <i class="fas fa-clock"></i>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 详细数据表格 -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <span>效率详细数据</span>
          <el-button type="primary" @click="refreshData">
            <i class="fas fa-sync-alt"></i>
            刷新数据
          </el-button>
        </div>
      </template>
      <el-table :data="efficiencyData" v-loading="loading" border>
        <el-table-column prop="equipmentName" label="设备名称" width="150" />
        <el-table-column prop="processType" label="工艺类型" width="120" />
        <el-table-column prop="utilization" label="利用率" width="100">
          <template #default="{ row }">
            <el-progress :percentage="row.utilization" :show-text="false" />
            <span style="margin-left: 10px;">{{ row.utilization }}%</span>
          </template>
        </el-table-column>
        <el-table-column prop="throughput" label="产能(件/小时)" width="130" />
        <el-table-column prop="energyConsumption" label="能耗(kWh)" width="120" />
        <el-table-column prop="efficiency" label="综合效率" width="120">
          <template #default="{ row }">
            <el-tag :type="row.efficiency >= 85 ? 'success' : row.efficiency >= 70 ? 'warning' : 'danger'">
              {{ row.efficiency }}%
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="lastMaintenance" label="最后维护" width="150" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 响应式数据
const loading = ref(false)
const overallEfficiency = ref(85)
const equipmentUtilization = ref(78)
const energyEfficiency = ref(82)
const timeEfficiency = ref(88)
const efficiencyData = ref([])

// 方法
const refreshData = async () => {
  loading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    efficiencyData.value = [
      {
        equipmentName: '振动研磨机-01',
        processType: '表面处理',
        utilization: 85,
        throughput: 45,
        energyConsumption: 12.5,
        efficiency: 88,
        lastMaintenance: '2024-01-10'
      },
      {
        equipmentName: '离心研磨机-02',
        processType: '精密加工',
        utilization: 72,
        throughput: 38,
        energyConsumption: 15.2,
        efficiency: 75,
        lastMaintenance: '2024-01-08'
      }
    ]
    
    ElMessage.success('数据刷新成功')
  } catch (error) {
    ElMessage.error('数据刷新失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  refreshData()
})
</script>

<style scoped>
.efficiency-statistics {
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

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

:deep(.el-card__body) {
  padding: 20px;
}
</style> 