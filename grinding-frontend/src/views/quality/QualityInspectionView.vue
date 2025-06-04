<template>
  <div class="quality-inspection">
    <div class="page-header">
      <h1>质量检测管理</h1>
      <div class="header-actions">
        <el-button type="primary" @click="handleCreateInspection">
          <i class="fas fa-plus"></i> 新建检测
        </el-button>
        <el-button type="success" @click="handleExportReport">
          <i class="fas fa-file-export"></i> 导出报告
        </el-button>
      </div>
    </div>

    <!-- 质量概览 -->
    <div class="quality-overview">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="overview-card">
            <template #header>
              <div class="card-header">
                <span>今日检测</span>
                <el-tag type="primary">{{ todayInspectionCount }}</el-tag>
              </div>
            </template>
            <div class="card-content">
              <p>待检批次：{{ pendingInspectionCount }}</p>
              <p>已检批次：{{ completedInspectionCount }}</p>
              <p>合格率：{{ todayQualityRate }}</p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <template #header>
              <div class="card-header">
                <span>本周统计</span>
                <el-tag type="success">{{ weekInspectionCount }}</el-tag>
              </div>
            </template>
            <div class="card-content">
              <p>检测总数：{{ weekTotalCount }}</p>
              <p>合格数：{{ weekPassedCount }}</p>
              <p>合格率：{{ weekQualityRate }}</p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <template #header>
              <div class="card-header">
                <span>本月统计</span>
                <el-tag type="warning">{{ monthInspectionCount }}</el-tag>
              </div>
            </template>
            <div class="card-content">
              <p>检测总数：{{ monthTotalCount }}</p>
              <p>合格数：{{ monthPassedCount }}</p>
              <p>合格率：{{ monthQualityRate }}</p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <template #header>
              <div class="card-header">
                <span>质量趋势</span>
                <el-tag :type="getTrendTag(qualityTrend)">
                  {{ getTrendLabel(qualityTrend) }}
                </el-tag>
              </div>
            </template>
            <div class="card-content">
              <p>较上周：{{ weekTrend }}</p>
              <p>较上月：{{ monthTrend }}</p>
              <p>年度目标：{{ yearlyTarget }}</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 检测列表 -->
    <el-card class="inspection-list">
      <template #header>
        <div class="list-header">
          <h2>检测列表</h2>
          <div class="list-actions">
            <el-input
              v-model="searchQuery"
              placeholder="搜索批次号或产品名称"
              class="search-input"
              clearable
              @clear="handleSearch"
              @input="handleSearch"
            >
              <template #prefix>
                <i class="fas fa-search"></i>
              </template>
            </el-input>
            <el-select v-model="filterStatus" placeholder="检测状态" @change="handleSearch">
              <el-option label="全部" value="" />
              <el-option label="待检测" value="pending" />
              <el-option label="检测中" value="in_progress" />
              <el-option label="已完成" value="completed" />
            </el-select>
            <el-select v-model="filterResult" placeholder="检测结果" @change="handleSearch">
              <el-option label="全部" value="" />
              <el-option label="合格" value="passed" />
              <el-option label="不合格" value="failed" />
            </el-select>
          </div>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="filteredInspections"
        style="width: 100%"
        border
      >
        <el-table-column prop="batch_number" label="批次号" width="120" />
        <el-table-column prop="product_name" label="产品名称" min-width="150" />
        <el-table-column prop="process_name" label="工艺名称" min-width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="result" label="检测结果" width="100">
          <template #default="{ row }">
            <el-tag
              v-if="row.result"
              :type="row.result === 'passed' ? 'success' : 'danger'"
            >
              {{ row.result === 'passed' ? '合格' : '不合格' }}
            </el-tag>
            <el-tag v-else type="info">未检测</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="inspector" label="检测员" width="120" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="completed_at" label="完成时间" width="180">
          <template #default="{ row }">
            {{ row.completed_at ? formatDate(row.completed_at) : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button
                type="primary"
                size="small"
                :disabled="!canStartInspection(row)"
                @click="handleStartInspection(row)"
              >
                开始检测
              </el-button>
              <el-button
                type="success"
                size="small"
                :disabled="!canCompleteInspection(row)"
                @click="handleCompleteInspection(row)"
              >
                完成检测
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

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 检测表单对话框 -->
    <el-dialog
      v-model="inspectionDialogVisible"
      :title="dialogType === 'create' ? '新建检测' : '完成检测'"
      width="60%"
    >
      <el-form
        ref="inspectionForm"
        :model="inspectionForm"
        :rules="formRules"
        label-width="100px"
      >
        <template v-if="dialogType === 'create'">
          <el-form-item label="批次号" prop="batch_number">
            <el-input v-model="inspectionForm.batch_number" />
          </el-form-item>
          <el-form-item label="产品名称" prop="product_name">
            <el-input v-model="inspectionForm.product_name" />
          </el-form-item>
          <el-form-item label="工艺名称" prop="process_name">
            <el-select v-model="inspectionForm.process_name">
              <el-option
                v-for="process in processList"
                :key="process.id"
                :label="process.name"
                :value="process.name"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="检测项目">
            <div v-for="(item, index) in inspectionForm.items" :key="index" class="inspection-item">
              <el-input v-model="item.name" placeholder="项目名称" class="item-name" />
              <el-input v-model="item.standard" placeholder="检测标准" class="item-standard" />
              <el-input v-model="item.unit" placeholder="单位" class="item-unit" />
              <el-button type="danger" @click="removeInspectionItem(index)">
                <i class="fas fa-trash"></i>
              </el-button>
            </div>
            <el-button type="primary" @click="addInspectionItem">
              <i class="fas fa-plus"></i> 添加检测项目
            </el-button>
          </el-form-item>
        </template>
        <template v-else>
          <el-form-item label="检测结果" prop="result">
            <el-radio-group v-model="inspectionForm.result">
              <el-radio label="passed">合格</el-radio>
              <el-radio label="failed">不合格</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="检测数据">
            <div v-for="(item, index) in inspectionForm.items" :key="index" class="inspection-data">
              <span class="item-label">{{ item.name }}</span>
              <el-input v-model="item.value" :placeholder="`输入${item.name}检测值`" />
              <span class="item-unit">{{ item.unit }}</span>
              <el-tag
                :type="getItemResultTag(item)"
                class="item-result"
              >
                {{ getItemResultLabel(item) }}
              </el-tag>
            </div>
          </el-form-item>
          <el-form-item label="不合格原因" prop="failure_reason" v-if="inspectionForm.result === 'failed'">
            <el-input
              v-model="inspectionForm.failure_reason"
              type="textarea"
              :rows="3"
              placeholder="请详细描述不合格原因"
            />
          </el-form-item>
          <el-form-item label="备注" prop="notes">
            <el-input
              v-model="inspectionForm.notes"
              type="textarea"
              :rows="3"
              placeholder="其他需要说明的情况"
            />
          </el-form-item>
        </template>
      </el-form>
      <template #footer>
        <el-button @click="inspectionDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>

    <!-- 检测详情对话框 -->
    <el-dialog
      v-model="detailsDialogVisible"
      title="检测详情"
      width="70%"
    >
      <div v-if="selectedInspection" class="inspection-details">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="批次号">
            {{ selectedInspection.batch_number }}
          </el-descriptions-item>
          <el-descriptions-item label="产品名称">
            {{ selectedInspection.product_name }}
          </el-descriptions-item>
          <el-descriptions-item label="工艺名称">
            {{ selectedInspection.process_name }}
          </el-descriptions-item>
          <el-descriptions-item label="检测状态">
            <el-tag :type="getStatusTag(selectedInspection.status)">
              {{ getStatusLabel(selectedInspection.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="检测结果" :span="2">
            <div v-if="selectedInspection.result">
              <el-tag
                :type="selectedInspection.result === 'passed' ? 'success' : 'danger'"
                class="result-tag"
              >
                {{ selectedInspection.result === 'passed' ? '合格' : '不合格' }}
              </el-tag>
              <p v-if="selectedInspection.failure_reason" class="failure-reason">
                不合格原因：{{ selectedInspection.failure_reason }}
              </p>
            </div>
            <el-tag v-else type="info">未检测</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="检测数据" :span="2">
            <el-table :data="selectedInspection.items" border>
              <el-table-column prop="name" label="检测项目" />
              <el-table-column prop="standard" label="检测标准" />
              <el-table-column prop="value" label="检测值" />
              <el-table-column prop="unit" label="单位" />
              <el-table-column label="结果">
                <template #default="{ row }">
                  <el-tag :type="getItemResultTag(row)">
                    {{ getItemResultLabel(row) }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
          </el-descriptions-item>
          <el-descriptions-item label="检测员">
            {{ selectedInspection.inspector }}
          </el-descriptions-item>
          <el-descriptions-item label="检测时间">
            {{ formatDate(selectedInspection.completed_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">
            {{ selectedInspection.notes || '无' }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import axiosInstance from '@/api/axios'

// 类型定义
interface InspectionItem {
  name: string
  standard: string
  value?: string
  unit: string
}

interface Inspection {
  id: number
  batch_number: string
  product_name: string
  process_name: string
  status: string
  result?: 'passed' | 'failed'
  items: InspectionItem[]
  inspector: string
  failure_reason?: string
  notes?: string
  created_at: string
  completed_at?: string
}

interface Process {
  id: number
  name: string
}

// 状态
const loading = ref(false)
const inspections = ref<Inspection[]>([])
const processList = ref<Process[]>([])
const searchQuery = ref('')
const filterStatus = ref('')
const filterResult = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const inspectionDialogVisible = ref(false)
const detailsDialogVisible = ref(false)
const dialogType = ref<'create' | 'complete'>('create')
const selectedInspection = ref<Inspection | null>(null)
const inspectionForm = ref<Partial<Inspection>>({
  batch_number: '',
  product_name: '',
  process_name: '',
  items: [],
  result: undefined,
  failure_reason: '',
  notes: ''
})
const inspectionFormRef = ref<FormInstance>()

// 统计数据
const todayInspectionCount = ref(0)
const pendingInspectionCount = ref(0)
const completedInspectionCount = ref(0)
const todayQualityRate = ref('0%')
const weekInspectionCount = ref(0)
const weekTotalCount = ref(0)
const weekPassedCount = ref(0)
const weekQualityRate = ref('0%')
const monthInspectionCount = ref(0)
const monthTotalCount = ref(0)
const monthPassedCount = ref(0)
const monthQualityRate = ref('0%')
const qualityTrend = ref('stable')
const weekTrend = ref('0%')
const monthTrend = ref('0%')
const yearlyTarget = ref('98%')

// 表单验证规则
const formRules: FormRules = {
  batch_number: [
    { required: true, message: '请输入批次号', trigger: 'blur' },
    { pattern: /^[A-Z0-9-]+$/, message: '批次号格式不正确', trigger: 'blur' }
  ],
  product_name: [
    { required: true, message: '请输入产品名称', trigger: 'blur' }
  ],
  process_name: [
    { required: true, message: '请选择工艺名称', trigger: 'change' }
  ],
  result: [
    { required: true, message: '请选择检测结果', trigger: 'change' }
  ],
  failure_reason: [
    { required: true, message: '请填写不合格原因', trigger: 'blur' }
  ]
}

// 计算属性
const filteredInspections = computed(() => {
  return inspections.value.filter(inspection => {
    const matchesSearch = !searchQuery.value ||
      inspection.batch_number.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      inspection.product_name.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesStatus = !filterStatus.value || inspection.status === filterStatus.value
    const matchesResult = !filterResult.value || inspection.result === filterResult.value
    
    return matchesSearch && matchesStatus && matchesResult
  })
})

// 方法
const fetchInspections = async () => {
  try {
    loading.value = true
    const response = await axiosInstance.get('/quality/inspections/', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value
      }
    })
    inspections.value = response.data.results
    total.value = response.data.count
    
    // 更新统计数据
    updateStatistics()
  } catch (error) {
    console.error('获取检测列表失败:', error)
    ElMessage.error('获取检测列表失败')
  } finally {
    loading.value = false
  }
}

const fetchProcessList = async () => {
  try {
    const response = await axiosInstance.get('/process-library/')
    processList.value = response.data.results || response.data
  } catch (error) {
    console.error('获取工艺列表失败:', error)
    ElMessage.error('获取工艺列表失败')
  }
}

const updateStatistics = () => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  const weekStart = new Date(today)
  weekStart.setDate(today.getDate() - today.getDay())
  
  const monthStart = new Date(today.getFullYear(), today.getMonth(), 1)
  
  // 今日统计
  const todayInspections = inspections.value.filter(i => new Date(i.created_at) >= today)
  todayInspectionCount.value = todayInspections.length
  pendingInspectionCount.value = todayInspections.filter(i => i.status === 'pending').length
  completedInspectionCount.value = todayInspections.filter(i => i.status === 'completed').length
  
  const todayPassed = todayInspections.filter(i => i.result === 'passed').length
  todayQualityRate.value = todayInspections.length > 0
    ? `${((todayPassed / todayInspections.length) * 100).toFixed(1)}%`
    : '0%'
  
  // 本周统计
  const weekInspections = inspections.value.filter(i => new Date(i.created_at) >= weekStart)
  weekInspectionCount.value = weekInspections.length
  weekTotalCount.value = weekInspections.length
  weekPassedCount.value = weekInspections.filter(i => i.result === 'passed').length
  weekQualityRate.value = weekInspections.length > 0
    ? `${((weekPassedCount.value / weekInspections.length) * 100).toFixed(1)}%`
    : '0%'
  
  // 本月统计
  const monthInspections = inspections.value.filter(i => new Date(i.created_at) >= monthStart)
  monthInspectionCount.value = monthInspections.length
  monthTotalCount.value = monthInspections.length
  monthPassedCount.value = monthInspections.filter(i => i.result === 'passed').length
  monthQualityRate.value = monthInspections.length > 0
    ? `${((monthPassedCount.value / monthInspections.length) * 100).toFixed(1)}%`
    : '0%'
  
  // 计算趋势
  const lastWeekRate = 95.5 // 这里应该从后端获取上周数据
  const lastMonthRate = 96.2 // 这里应该从后端获取上月数据
  
  const weekDiff = parseFloat(weekQualityRate.value) - lastWeekRate
  const monthDiff = parseFloat(monthQualityRate.value) - lastMonthRate
  
  weekTrend.value = `${weekDiff >= 0 ? '+' : ''}${weekDiff.toFixed(1)}%`
  monthTrend.value = `${monthDiff >= 0 ? '+' : ''}${monthDiff.toFixed(1)}%`
  
  if (weekDiff > 1) {
    qualityTrend.value = 'up'
  } else if (weekDiff < -1) {
    qualityTrend.value = 'down'
  } else {
    qualityTrend.value = 'stable'
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchInspections()
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchInspections()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchInspections()
}

const handleCreateInspection = () => {
  dialogType.value = 'create'
  inspectionForm.value = {
    batch_number: '',
    product_name: '',
    process_name: '',
    items: [],
    result: undefined,
    failure_reason: '',
    notes: ''
  }
  inspectionDialogVisible.value = true
}

const handleStartInspection = (inspection: Inspection) => {
  dialogType.value = 'complete'
  inspectionForm.value = { ...inspection }
  inspectionDialogVisible.value = true
}

const handleCompleteInspection = (inspection: Inspection) => {
  dialogType.value = 'complete'
  inspectionForm.value = { ...inspection }
  inspectionDialogVisible.value = true
}

const handleViewDetails = (inspection: Inspection) => {
  selectedInspection.value = inspection
  detailsDialogVisible.value = true
}

const handleExportReport = async () => {
  try {
    const response = await axiosInstance.get('/quality/export-report/', {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `质量检测报告_${new Date().toLocaleDateString()}.xlsx`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('报告导出成功')
  } catch (error) {
    console.error('导出报告失败:', error)
    ElMessage.error('导出报告失败')
  }
}

const addInspectionItem = () => {
  if (!inspectionForm.value.items) {
    inspectionForm.value.items = []
  }
  inspectionForm.value.items.push({
    name: '',
    standard: '',
    unit: ''
  })
}

const removeInspectionItem = (index: number) => {
  inspectionForm.value.items?.splice(index, 1)
}

const canStartInspection = (inspection: Inspection) => {
  return inspection.status === 'pending'
}

const canCompleteInspection = (inspection: Inspection) => {
  return inspection.status === 'in_progress'
}

const getItemResultTag = (item: InspectionItem): 'primary' | 'success' | 'warning' | 'info' | 'danger' => {
  if (!item.value || !item.standard) return 'info'
  
  const value = parseFloat(item.value)
  const standard = parseFloat(item.standard)
  
  if (isNaN(value) || isNaN(standard)) return 'info'
  
  const tolerance = standard * 0.05 // 假设允许5%的误差
  if (Math.abs(value - standard) <= tolerance) {
    return 'success'
  } else if (Math.abs(value - standard) <= tolerance * 2) {
    return 'warning'
  } else {
    return 'danger'
  }
}

const getItemResultLabel = (item: InspectionItem): string => {
  if (!item.value || !item.standard) return '未检测'
  
  const value = parseFloat(item.value)
  const standard = parseFloat(item.standard)
  
  if (isNaN(value) || isNaN(standard)) return '数据无效'
  
  const tolerance = standard * 0.05
  if (Math.abs(value - standard) <= tolerance) {
    return '合格'
  } else if (Math.abs(value - standard) <= tolerance * 2) {
    return '警告'
  } else {
    return '不合格'
  }
}

const submitForm = async () => {
  if (!inspectionFormRef.value) return
  
  try {
    await inspectionFormRef.value.validate()
    
    if (dialogType.value === 'create') {
      await axiosInstance.post('/quality/inspections/', inspectionForm.value)
      ElMessage.success('创建检测任务成功')
    } else {
      await axiosInstance.put(`/quality/inspections/${inspectionForm.value.id}/`, inspectionForm.value)
      ElMessage.success('完成检测成功')
    }
    
    inspectionDialogVisible.value = false
    fetchInspections()
  } catch (error) {
    console.error('提交表单失败:', error)
    ElMessage.error('提交失败，请检查表单')
  }
}

// 工具函数
const getStatusTag = (status: string): 'primary' | 'success' | 'warning' | 'info' | 'danger' => {
  const statusMap: Record<string, 'primary' | 'success' | 'warning' | 'info' | 'danger'> = {
    pending: 'info',
    in_progress: 'warning',
    completed: 'success'
  }
  return statusMap[status] || 'info'
}

const getStatusLabel = (status: string): string => {
  const statusMap: Record<string, string> = {
    pending: '待检测',
    in_progress: '检测中',
    completed: '已完成'
  }
  return statusMap[status] || status
}

const getTrendTag = (trend: string): 'primary' | 'success' | 'warning' | 'info' | 'danger' => {
  const trendMap: Record<string, 'primary' | 'success' | 'warning' | 'info' | 'danger'> = {
    up: 'success',
    down: 'danger',
    stable: 'info'
  }
  return trendMap[trend] || 'info'
}

const getTrendLabel = (trend: string): string => {
  const trendMap: Record<string, string> = {
    up: '上升',
    down: '下降',
    stable: '稳定'
  }
  return trendMap[trend] || trend
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

// 生命周期钩子
onMounted(() => {
  fetchInspections()
  fetchProcessList()
})
</script>

<style scoped>
.quality-inspection {
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

.quality-overview {
  margin-bottom: 1.5rem;
}

.overview-card {
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

.inspection-list {
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

.inspection-item {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.item-name {
  width: 200px;
}

.item-standard {
  width: 150px;
}

.item-unit {
  width: 100px;
}

.inspection-data {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.item-label {
  width: 120px;
  color: #666;
}

.item-result {
  min-width: 80px;
  text-align: center;
}

.failure-reason {
  margin-top: 0.5rem;
  color: #f56c6c;
}

.pagination-container {
  margin-top: 1.5rem;
  display: flex;
  justify-content: flex-end;
}

.inspection-details {
  .el-descriptions {
    margin-bottom: 1rem;
  }
  
  .result-tag {
    font-size: 1.1rem;
    padding: 0.5rem 1rem;
  }
}

@media (max-width: 768px) {
  .quality-inspection {
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

  .inspection-item {
    flex-direction: column;
  }

  .item-name,
  .item-standard,
  .item-unit {
    width: 100%;
  }

  .inspection-data {
    flex-direction: column;
    align-items: flex-start;
  }

  .item-label {
    width: 100%;
  }
}
</style> 