<template>
  <div class="process-library">
    <div class="page-header">
      <h1>工艺库</h1>
      <el-button type="primary" @click="handleCreateProcess">
        <el-icon><Plus /></el-icon>
        新建工艺
      </el-button>
    </div>

    <!-- 搜索和过滤 -->
    <div class="search-bar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索工艺名称、编号或描述"
        class="search-input"
        clearable
        @clear="handleSearch"
        @keyup.enter="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-select
        v-model="filterType"
        placeholder="工艺类型"
        class="filter-select"
        clearable
        @change="handleSearch"
      >
        <el-option
          v-for="type in processTypes"
          :key="type.id"
          :label="type.name"
          :value="type.id"
        />
      </el-select>

      <el-select
        v-model="filterStatus"
        placeholder="状态"
        class="filter-select"
        clearable
        @change="handleSearch"
      >
        <el-option label="已发布" value="published" />
        <el-option label="草稿" value="draft" />
        <el-option label="已归档" value="archived" />
      </el-select>

      <el-button type="primary" @click="handleSearch">
        <el-icon><Search /></el-icon>
        搜索
      </el-button>
    </div>

    <!-- 工艺列表 -->
    <el-table
      v-loading="loading"
      :data="processList"
      style="width: 100%"
      border
    >
      <el-table-column prop="code" label="工艺编号" width="120" />
      <el-table-column prop="name" label="工艺名称" min-width="150" />
      <el-table-column prop="type" label="工艺类型" width="120">
        <template #default="{ row }">
          {{ getProcessTypeName(row.type) }}
        </template>
      </el-table-column>
      <el-table-column prop="version" label="版本" width="80" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusLabel(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_by" label="创建人" width="120" />
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column prop="updated_at" label="更新时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.updated_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button
              type="primary"
              link
              @click="handleViewProcess(row)"
            >
              查看
            </el-button>
            <el-button
              type="primary"
              link
              @click="handleEditProcess(row)"
              :disabled="row.status === 'archived'"
            >
              编辑
            </el-button>
            <el-button
              type="primary"
              link
              @click="handleCopyProcess(row)"
            >
              复制
            </el-button>
            <el-button
              type="danger"
              link
              @click="handleDeleteProcess(row)"
              :disabled="row.status === 'archived'"
            >
              删除
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

    <!-- 工艺表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '新建工艺' : '编辑工艺'"
      width="60%"
    >
      <el-form
        ref="processFormRef"
        :model="processForm"
        :rules="processRules"
        label-width="100px"
      >
        <el-form-item label="工艺名称" prop="name">
          <el-input v-model="processForm.name" />
        </el-form-item>
        <el-form-item label="工艺类型" prop="type">
          <el-select v-model="processForm.type" placeholder="请选择工艺类型">
            <el-option
              v-for="type in processTypes"
              :key="type.id"
              :label="type.name"
              :value="type.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="工艺描述" prop="description">
          <el-input
            v-model="processForm.description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="工艺参数" prop="parameters">
          <el-table :data="processForm.parameters" border>
            <el-table-column label="参数名称" prop="name" />
            <el-table-column label="参数值" prop="value" />
            <el-table-column label="单位" prop="unit" />
            <el-table-column label="操作" width="120">
              <template #default="{ $index }">
                <el-button
                  type="danger"
                  link
                  @click="handleRemoveParameter($index)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="parameter-actions">
            <el-button type="primary" link @click="handleAddParameter">
              <el-icon><Plus /></el-icon>
              添加参数
            </el-button>
          </div>
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input
            v-model="processForm.remarks"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitProcess">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 工艺详情对话框 -->
    <el-dialog
      v-model="detailsDialogVisible"
      title="工艺详情"
      width="70%"
    >
      <el-descriptions
        v-if="selectedProcess"
        :column="2"
        border
      >
        <el-descriptions-item label="工艺编号" :span="2">
          {{ selectedProcess.code }}
        </el-descriptions-item>
        <el-descriptions-item label="工艺名称" :span="2">
          {{ selectedProcess.name }}
        </el-descriptions-item>
        <el-descriptions-item label="工艺类型">
          {{ getProcessTypeName(selectedProcess.type) }}
        </el-descriptions-item>
        <el-descriptions-item label="版本">
          {{ selectedProcess.version }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(selectedProcess.status)">
            {{ getStatusLabel(selectedProcess.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建人">
          {{ selectedProcess.created_by }}
        </el-descriptions-item>
        <el-descriptions-item label="创建时间" :span="2">
          {{ formatDate(selectedProcess.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="更新时间" :span="2">
          {{ formatDate(selectedProcess.updated_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="工艺描述" :span="2">
          {{ selectedProcess.description }}
        </el-descriptions-item>
        <el-descriptions-item label="工艺参数" :span="2">
          <el-table :data="selectedProcess.parameters" border>
            <el-table-column prop="name" label="参数名称" />
            <el-table-column prop="value" label="参数值" />
            <el-table-column prop="unit" label="单位" />
          </el-table>
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">
          {{ selectedProcess.remarks }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import axiosInstance from '@/api/axios'

// 类型定义
interface ProcessParameter {
  name: string
  value: string
  unit: string
}

interface ProcessType {
  id: number
  name: string
  description?: string
}

interface Process {
  id: number
  code: string
  name: string
  type: number
  version: string
  status: 'draft' | 'published' | 'archived'
  description: string
  parameters: ProcessParameter[]
  remarks?: string
  created_by: string
  created_at: string
  updated_at: string
}

// 状态
const loading = ref(false)
const processList = ref<Process[]>([])
const processTypes = ref<ProcessType[]>([])
const searchQuery = ref('')
const filterType = ref<number | null>(null)
const filterStatus = ref<string | null>(null)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 对话框状态
const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit'>('create')
const detailsDialogVisible = ref(false)
const selectedProcess = ref<Process | null>(null)

// 表单数据
const processFormRef = ref()
const processForm = ref({
  name: '',
  type: null as number | null,
  description: '',
  parameters: [] as ProcessParameter[],
  remarks: ''
})

// 表单验证规则
const processRules = {
  name: [
    { required: true, message: '请输入工艺名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择工艺类型', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入工艺描述', trigger: 'blur' }
  ]
}

// 获取工艺类型列表
const fetchProcessTypes = async () => {
  try {
    const response = await axiosInstance.get('/process-types/')
    processTypes.value = response.data.results || response.data
  } catch (error) {
    console.error('获取工艺类型失败:', error)
    ElMessage.error('获取工艺类型失败')
  }
}

// 获取工艺列表
const fetchProcessList = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value,
      type: filterType.value,
      status: filterStatus.value
    }
    const response = await axiosInstance.get('/processes/', { params })
    processList.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('获取工艺列表失败:', error)
    ElMessage.error('获取工艺列表失败')
  } finally {
    loading.value = false
  }
}

// 创建工艺
const handleCreateProcess = () => {
  dialogType.value = 'create'
  processForm.value = {
    name: '',
    type: null,
    description: '',
    parameters: [],
    remarks: ''
  }
  dialogVisible.value = true
}

// 编辑工艺
const handleEditProcess = (process: Process) => {
  dialogType.value = 'edit'
  processForm.value = {
    name: process.name,
    type: process.type,
    description: process.description,
    parameters: [...process.parameters],
    remarks: process.remarks || ''
  }
  dialogVisible.value = true
}

// 查看工艺详情
const handleViewProcess = (process: Process) => {
  selectedProcess.value = process
  detailsDialogVisible.value = true
}

// 复制工艺
const handleCopyProcess = async (process: Process) => {
  try {
    await ElMessageBox.confirm(
      '确定要复制该工艺吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }
    )
    
    const response = await axiosInstance.post(`/processes/${process.id}/copy/`)
    ElMessage.success('工艺复制成功')
    fetchProcessList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('复制工艺失败:', error)
      ElMessage.error('复制工艺失败')
    }
  }
}

// 删除工艺
const handleDeleteProcess = async (process: Process) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该工艺吗？此操作不可恢复。',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await axiosInstance.delete(`/processes/${process.id}/`)
    ElMessage.success('工艺删除成功')
    fetchProcessList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除工艺失败:', error)
      ElMessage.error('删除工艺失败')
    }
  }
}

// 提交工艺表单
const handleSubmitProcess = async () => {
  if (!processFormRef.value) return
  
  try {
    await processFormRef.value.validate()
    
    if (dialogType.value === 'create') {
      await axiosInstance.post('/processes/', processForm.value)
      ElMessage.success('工艺创建成功')
    } else {
      await axiosInstance.put(`/processes/${selectedProcess.value?.id}/`, processForm.value)
      ElMessage.success('工艺更新成功')
    }
    
    dialogVisible.value = false
    fetchProcessList()
  } catch (error) {
    console.error('提交工艺失败:', error)
    ElMessage.error('提交工艺失败')
  }
}

// 添加参数
const handleAddParameter = () => {
  processForm.value.parameters.push({
    name: '',
    value: '',
    unit: ''
  })
}

// 删除参数
const handleRemoveParameter = (index: number) => {
  processForm.value.parameters.splice(index, 1)
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchProcessList()
}

// 分页处理
const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchProcessList()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchProcessList()
}

// 工具函数
const getProcessTypeName = (typeId: number): string => {
  const type = processTypes.value.find(t => t.id === typeId)
  return type?.name || '未知类型'
}

const getStatusType = (status: string): 'info' | 'success' | 'warning' => {
  const statusMap: Record<string, 'info' | 'success' | 'warning'> = {
    draft: 'info',
    published: 'success',
    archived: 'warning'
  }
  return statusMap[status] || 'info'
}

const getStatusLabel = (status: string): string => {
  const statusMap: Record<string, string> = {
    draft: '草稿',
    published: '已发布',
    archived: '已归档'
  }
  return statusMap[status] || status
}

const formatDate = (date: string): string => {
  return new Date(date).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 初始化
onMounted(() => {
  fetchProcessTypes()
  fetchProcessList()
})
</script>

<style scoped>
.process-library {
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

.search-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.search-input {
  width: 300px;
}

.filter-select {
  width: 150px;
}

.pagination-container {
  margin-top: 1.5rem;
  display: flex;
  justify-content: flex-end;
}

.parameter-actions {
  margin-top: 0.5rem;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style> 