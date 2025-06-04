<template>
  <div class="equipment-operation">
    <div class="page-header">
      <h1>设备运行管理</h1>
      <div class="header-actions">
        <el-button type="primary" @click="handleStartOperation" :disabled="!canStartOperation">
          <i class="fas fa-play"></i> 开始运行
        </el-button>
        <el-button type="warning" @click="handlePauseOperation" :disabled="!canPauseOperation">
          <i class="fas fa-pause"></i> 暂停运行
        </el-button>
        <el-button type="danger" @click="handleStopOperation" :disabled="!canStopOperation">
          <i class="fas fa-stop"></i> 停止运行
        </el-button>
      </div>
    </div>

    <!-- 设备状态概览 -->
    <div class="status-overview">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="status-card">
            <template #header>
              <div class="card-header">
                <span>在线设备</span>
                <el-tag type="success">{{ onlineCount }}</el-tag>
              </div>
            </template>
            <div class="card-content">
              <p>总设备数：{{ totalCount }}</p>
              <p>运行中：{{ runningCount }}</p>
              <p>待机中：{{ idleCount }}</p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="status-card">
            <template #header>
              <div class="card-header">
                <span>今日运行</span>
                <el-tag type="primary">{{ todayOperationCount }}</el-tag>
              </div>
            </template>
            <div class="card-content">
              <p>运行时长：{{ todayOperationTime }}</p>
              <p>完成批次：{{ todayCompletedBatches }}</p>
              <p>待处理批次：{{ todayPendingBatches }}</p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="status-card">
            <template #header>
              <div class="card-header">
                <span>告警信息</span>
                <el-tag type="danger">{{ alertCount }}</el-tag>
              </div>
            </template>
            <div class="card-content">
              <p>严重告警：{{ criticalAlerts }}</p>
              <p>一般告警：{{ normalAlerts }}</p>
              <p>已处理：{{ resolvedAlerts }}</p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="status-card">
            <template #header>
              <div class="card-header">
                <span>设备状态</span>
                <el-tag :type="getStatusTag(overallStatus)">
                  {{ getStatusLabel(overallStatus) }}
                </el-tag>
              </div>
            </template>
            <div class="card-content">
              <p>运行状态：{{ getStatusLabel(operationStatus) }}</p>
              <p>维护状态：{{ getStatusLabel(maintenanceStatus) }}</p>
              <p>更新时间：{{ lastUpdateTime }}</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 设备列表 -->
    <el-card class="equipment-list">
      <template #header>
        <div class="list-header">
          <h2>设备列表</h2>
          <div class="list-actions">
            <el-input
              v-model="searchQuery"
              placeholder="搜索设备名称或编号"
              class="search-input"
              clearable
              @clear="handleSearch"
              @input="handleSearch"
            >
              <template #prefix>
                <i class="fas fa-search"></i>
              </template>
            </el-input>
            <el-select v-model="filterStatus" placeholder="设备状态" @change="handleSearch">
              <el-option label="全部" value="" />
              <el-option label="运行中" value="running" />
              <el-option label="待机" value="idle" />
              <el-option label="维护中" value="maintenance" />
              <el-option label="故障" value="error" />
            </el-select>
          </div>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="filteredEquipment"
        style="width: 100%"
        border
      >
        <el-table-column prop="code" label="设备编号" width="120" />
        <el-table-column prop="name" label="设备名称" min-width="150" />
        <el-table-column prop="status" label="运行状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="current_process" label="当前工艺" min-width="150">
          <template #default="{ row }">
            <span v-if="row.current_process">{{ row.current_process.name }}</span>
            <el-tag v-else type="info">无</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="batch_info" label="批次信息" min-width="150">
          <template #default="{ row }">
            <div v-if="row.batch_info">
              <p>批次号：{{ row.batch_info.batch_number }}</p>
              <p>进度：{{ row.batch_info.progress }}%</p>
            </div>
            <el-tag v-else type="info">无</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_maintenance" label="最近维护" width="180">
          <template #default="{ row }">
            {{ formatDate(row.last_maintenance) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button
                type="primary"
                size="small"
                :disabled="!canOperate(row)"
                @click="handleStartEquipment(row)"
              >
                启动
              </el-button>
              <el-button
                type="warning"
                size="small"
                :disabled="!canPause(row)"
                @click="handlePauseEquipment(row)"
              >
                暂停
              </el-button>
              <el-button
                type="danger"
                size="small"
                :disabled="!canStop(row)"
                @click="handleStopEquipment(row)"
              >
                停止
              </el-button>
              <el-button
                type="info"
                size="small"
                @click="handleViewDetails(row)"
              >
                详情
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 运行详情对话框 -->
    <el-dialog
      v-model="detailsDialogVisible"
      title="设备运行详情"
      width="70%"
    >
      <div v-if="selectedEquipment" class="equipment-details">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="设备编号">
            {{ selectedEquipment.code }}
          </el-descriptions-item>
          <el-descriptions-item label="设备名称">
            {{ selectedEquipment.name }}
          </el-descriptions-item>
          <el-descriptions-item label="运行状态">
            <el-tag :type="getStatusTag(selectedEquipment.status)">
              {{ getStatusLabel(selectedEquipment.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="当前工艺">
            {{ selectedEquipment.current_process?.name || '无' }}
          </el-descriptions-item>
          <el-descriptions-item label="批次信息" :span="2">
            <div v-if="selectedEquipment.batch_info">
              <p>批次号：{{ selectedEquipment.batch_info.batch_number }}</p>
              <p>开始时间：{{ formatDate(selectedEquipment.batch_info.start_time) }}</p>
              <p>预计完成：{{ formatDate(selectedEquipment.batch_info.estimated_end_time) }}</p>
              <p>进度：{{ selectedEquipment.batch_info.progress }}%</p>
            </div>
            <el-tag v-else type="info">无批次信息</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="运行参数" :span="2">
            <el-table :data="selectedEquipment.parameters || []" border>
              <el-table-column prop="name" label="参数名称" />
              <el-table-column prop="value" label="当前值" />
              <el-table-column prop="unit" label="单位" />
              <el-table-column prop="status" label="状态">
                <template #default="{ row }">
                  <el-tag :type="getParameterStatusTag(row.status)">
                    {{ getParameterStatusLabel(row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
          </el-descriptions-item>
          <el-descriptions-item label="告警信息" :span="2">
            <el-timeline>
              <el-timeline-item
                v-for="alert in selectedEquipment.alerts"
                :key="alert.id"
                :type="getAlertTypeTag(alert.level)"
                :timestamp="formatDate(alert.time)"
              >
                {{ alert.message }}
              </el-timeline-item>
            </el-timeline>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axiosInstance from '@/api/axios'

// 类型定义
interface EquipmentParameter {
  name: string
  value: string
  unit: string
  status: string
}

interface BatchInfo {
  batch_number: string
  start_time: string
  estimated_end_time: string
  progress: number
}

interface Alert {
  id: number
  level: string
  message: string
  time: string
  is_resolved: boolean
  resolved_at?: string
  resolved_by?: string
}

interface Equipment {
  id: number
  code: string
  name: string
  status: string
  current_process?: {
    id: number
    name: string
  }
  batch_info?: BatchInfo
  parameters?: EquipmentParameter[]
  alerts?: Alert[]
  last_maintenance: string
}

// 状态
const loading = ref(false)
const equipment = ref<Equipment[]>([])
const searchQuery = ref('')
const filterStatus = ref('')
const detailsDialogVisible = ref(false)
const selectedEquipment = ref<Equipment | null>(null)

// 统计数据
const totalCount = ref(0)
const onlineCount = ref(0)
const runningCount = ref(0)
const idleCount = ref(0)
const todayOperationCount = ref(0)
const todayOperationTime = ref('0小时')
const todayCompletedBatches = ref(0)
const todayPendingBatches = ref(0)
const alertCount = ref(0)
const criticalAlerts = ref(0)
const normalAlerts = ref(0)
const resolvedAlerts = ref(0)
const overallStatus = ref('normal')
const operationStatus = ref('idle')
const maintenanceStatus = ref('normal')
const lastUpdateTime = ref('')

// 计算属性
const filteredEquipment = computed(() => {
  return equipment.value.filter(eq => {
    const matchesSearch = !searchQuery.value ||
      eq.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      eq.code.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesStatus = !filterStatus.value || eq.status === filterStatus.value
    
    return matchesSearch && matchesStatus
  })
})

const canStartOperation = computed(() => {
  return equipment.value.some(eq => eq.status === 'idle')
})

const canPauseOperation = computed(() => {
  return equipment.value.some(eq => eq.status === 'running')
})

const canStopOperation = computed(() => {
  return equipment.value.some(eq => ['running', 'paused'].includes(eq.status))
})

// 方法
const fetchEquipmentData = async () => {
  try {
    loading.value = true
    const response = await axiosInstance.get('/equipment/')
    equipment.value = response.data.results || response.data
    
    // 更新统计数据
    updateStatistics()
  } catch (error) {
    console.error('获取设备数据失败:', error)
    ElMessage.error('获取设备数据失败')
  } finally {
    loading.value = false
  }
}

const updateStatistics = () => {
  totalCount.value = equipment.value.length
  onlineCount.value = equipment.value.filter(eq => eq.status !== 'offline').length
  runningCount.value = equipment.value.filter(eq => eq.status === 'running').length
  idleCount.value = equipment.value.filter(eq => eq.status === 'idle').length
  
  // 更新告警统计
  const alerts = equipment.value.flatMap(eq => eq.alerts || [])
  alertCount.value = alerts.length
  criticalAlerts.value = alerts.filter(a => a.level === 'critical').length
  normalAlerts.value = alerts.filter(a => a.level === 'normal').length
  resolvedAlerts.value = alerts.filter(a => a.is_resolved).length
  
  // 更新状态
  if (criticalAlerts.value > 0) {
    overallStatus.value = 'error'
  } else if (normalAlerts.value > 0) {
    overallStatus.value = 'warning'
  } else {
    overallStatus.value = 'normal'
  }
  
  // 更新运行状态
  if (runningCount.value > 0) {
    operationStatus.value = 'running'
  } else if (idleCount.value > 0) {
    operationStatus.value = 'idle'
  } else {
    operationStatus.value = 'stopped'
  }
  
  lastUpdateTime.value = new Date().toLocaleString('zh-CN')
}

const handleSearch = () => {
  // 本地搜索，不需要重新请求数据
}

const handleStartOperation = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要启动所有待机设备吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await axiosInstance.post('/equipment/start-all/')
    ElMessage.success('已启动所有待机设备')
    fetchEquipmentData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('启动设备失败:', error)
      ElMessage.error('启动设备失败')
    }
  }
}

const handlePauseOperation = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要暂停所有运行中的设备吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await axiosInstance.post('/equipment/pause-all/')
    ElMessage.success('已暂停所有运行中的设备')
    fetchEquipmentData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('暂停设备失败:', error)
      ElMessage.error('暂停设备失败')
    }
  }
}

const handleStopOperation = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要停止所有设备运行吗？此操作将中断当前所有工艺。',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await axiosInstance.post('/equipment/stop-all/')
    ElMessage.success('已停止所有设备运行')
    fetchEquipmentData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('停止设备失败:', error)
      ElMessage.error('停止设备失败')
    }
  }
}

const canOperate = (equipment: Equipment) => {
  return equipment.status === 'idle'
}

const canPause = (equipment: Equipment) => {
  return equipment.status === 'running'
}

const canStop = (equipment: Equipment) => {
  return ['running', 'paused'].includes(equipment.status)
}

const handleStartEquipment = async (equipment: Equipment) => {
  try {
    await axiosInstance.post(`/equipment/${equipment.id}/start/`)
    ElMessage.success('设备启动成功')
    fetchEquipmentData()
  } catch (error) {
    console.error('启动设备失败:', error)
    ElMessage.error('启动设备失败')
  }
}

const handlePauseEquipment = async (equipment: Equipment) => {
  try {
    await axiosInstance.post(`/equipment/${equipment.id}/pause/`)
    ElMessage.success('设备已暂停')
    fetchEquipmentData()
  } catch (error) {
    console.error('暂停设备失败:', error)
    ElMessage.error('暂停设备失败')
  }
}

const handleStopEquipment = async (equipment: Equipment) => {
  try {
    await ElMessageBox.confirm(
      '确定要停止该设备运行吗？此操作将中断当前工艺。',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await axiosInstance.post(`/equipment/${equipment.id}/stop/`)
    ElMessage.success('设备已停止')
    fetchEquipmentData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('停止设备失败:', error)
      ElMessage.error('停止设备失败')
    }
  }
}

const handleViewDetails = (equipment: Equipment) => {
  selectedEquipment.value = equipment
  detailsDialogVisible.value = true
}

// 工具函数
const getStatusTag = (status: string): 'primary' | 'success' | 'warning' | 'info' | 'danger' => {
  const statusMap: Record<string, 'primary' | 'success' | 'warning' | 'info' | 'danger'> = {
    running: 'success',
    idle: 'info',
    paused: 'warning',
    maintenance: 'warning',
    error: 'danger',
    offline: 'info'
  }
  return statusMap[status] || 'info'
}

const getStatusLabel = (status: string): string => {
  const statusMap: Record<string, string> = {
    running: '运行中',
    idle: '待机',
    paused: '已暂停',
    maintenance: '维护中',
    error: '故障',
    offline: '离线',
    normal: '正常',
    warning: '警告'
  }
  return statusMap[status] || status
}

const getParameterStatusTag = (status: string): 'primary' | 'success' | 'warning' | 'info' | 'danger' => {
  const statusMap: Record<string, 'primary' | 'success' | 'warning' | 'info' | 'danger'> = {
    normal: 'success',
    warning: 'warning',
    error: 'danger'
  }
  return statusMap[status] || 'info'
}

const getParameterStatusLabel = (status: string): string => {
  const statusMap: Record<string, string> = {
    normal: '正常',
    warning: '警告',
    error: '异常'
  }
  return statusMap[status] || status
}

const getAlertTypeTag = (level: string): 'primary' | 'success' | 'warning' | 'info' | 'danger' => {
  const levelMap: Record<string, 'primary' | 'success' | 'warning' | 'info' | 'danger'> = {
    critical: 'danger',
    warning: 'warning',
    info: 'info'
  }
  return levelMap[level] || 'info'
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 定时刷新数据
let refreshInterval: number

onMounted(() => {
  fetchEquipmentData()
  // 每30秒刷新一次数据
  refreshInterval = window.setInterval(fetchEquipmentData, 30000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
.equipment-operation {
  padding: 1rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.page-header h1 {
  margin: 0;
  font-size: 1.75rem;
  color: #2c3e50;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.status-overview {
  margin-bottom: 1.5rem;
}

.status-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  p {
    margin: 0.5rem 0;
    color: #666;
  }
}

.equipment-list {
  margin-bottom: 1.5rem;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.list-header h2 {
  margin: 0;
  font-size: 1.25rem;
  color: #2c3e50;
}

.list-actions {
  display: flex;
  gap: 1rem;
}

.search-input {
  width: 250px;
}

.equipment-details {
  .el-descriptions {
    margin-bottom: 1rem;
  }
}

@media (max-width: 768px) {
  .equipment-operation {
    padding: 0.5rem;
  }

  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    flex-wrap: wrap;
  }

  .list-header {
    flex-direction: column;
    gap: 1rem;
  }

  .list-actions {
    width: 100%;
    flex-direction: column;
  }

  .search-input {
    width: 100%;
  }
}
</style> 