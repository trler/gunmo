<template>
  <div class="process-data-container">
    <div class="header">
      <h2>工艺数据管理</h2>
      <button @click="showCreateModal = true" class="create-btn">
        添加工艺数据
      </button>
    </div>

    <!-- 搜索和过滤 -->
    <div class="filters">
      <input
        v-model="searchQuery"
        @input="handleSearch"
        placeholder="搜索工艺数据..."
        class="search-input"
      />
      <select v-model="statusFilter" @change="handleFilter" class="filter-select">
        <option value="">所有状态</option>
        <option value="active">活跃</option>
        <option value="inactive">非活跃</option>
      </select>
    </div>

    <!-- 数据列表 -->
    <div class="data-list" v-if="!loading">
      <div v-if="processDataList.length === 0" class="empty-state">
        <p>暂无工艺数据</p>
      </div>
      <div v-else>
        <div
          v-for="item in processDataList"
          :key="item.id"
          class="data-item"
        >
          <div class="item-header">
            <h3>{{ item.name || '工艺数据 #' + item.id }}</h3>
            <div class="item-actions">
              <button @click="editItem(item)" class="edit-btn">编辑</button>
              <button @click="deleteItem(item.id)" class="delete-btn">删除</button>
            </div>
          </div>
          <div class="item-content">
            <p><strong>类别:</strong> {{ item.category?.name || '未分类' }}</p>
            <p><strong>状态:</strong> {{ getStatusText(item.status) }}</p>
            <p><strong>创建时间:</strong> {{ formatDate(item.created_at) }}</p>
            <p><strong>更新时间:</strong> {{ formatDate(item.updated_at) }}</p>
            <p v-if="item.description"><strong>描述:</strong> {{ item.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>

    <!-- 创建/编辑模态框 -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ showEditModal ? '编辑工艺数据' : '添加工艺数据' }}</h3>
          <button @click="closeModal" class="close-btn">×</button>
        </div>
        <form @submit.prevent="handleSubmit" class="modal-form">
          <div class="form-group">
            <label for="name">名称</label>
            <input
              type="text"
              id="name"
              v-model="formData.name"
              required
              placeholder="请输入工艺数据名称"
            />
          </div>

          <div class="form-group">
            <label for="description">描述</label>
            <textarea
              id="description"
              v-model="formData.description"
              placeholder="请输入描述"
              rows="3"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="status">状态</label>
            <select id="status" v-model="formData.status" required>
              <option value="active">活跃</option>
              <option value="inactive">非活跃</option>
            </select>
          </div>

          <div class="form-actions">
            <button type="button" @click="closeModal" class="cancel-btn">
              取消
            </button>
            <button type="submit" :disabled="submitting" class="submit-btn">
              {{ submitting ? '提交中...' : (showEditModal ? '更新' : '创建') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import axiosInstance from '@/api/axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { ProcessData, ProcessDataStatus } from '@/types/auth'
import { AxiosError } from 'axios'

// 状态管理
const loading = ref(false)
const submitting = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const processDataList = ref<ProcessData[]>([])
const currentEditItem = ref<ProcessData | null>(null)

// 搜索和过滤
const searchQuery = ref('')
const statusFilter = ref<ProcessDataStatus | ''>('')

// 表单数据
interface ProcessDataForm {
  name: string
  description: string
  status: ProcessDataStatus
}

const formData = reactive<ProcessDataForm>({
  name: '',
  description: '',
  status: 'active'
})

// 获取工艺数据列表
const fetchProcessData = async () => {
  try {
    loading.value = true
    const response = await axiosInstance.get('/')
    processDataList.value = response.data.results || response.data || []
  } catch (error: any) {
    console.error('获取工艺数据失败:', error)
    ElMessage.error(error.response?.data?.detail || '获取工艺数据失败，请重试')
  } finally {
    loading.value = false
  }
}

// 创建工艺数据
const createProcessData = async (data: Omit<ProcessData, 'id' | 'created_at' | 'updated_at'>) => {
  try {
    submitting.value = true
    await axiosInstance.post('/create/', data)
    ElMessage.success('创建成功')
    closeModal()
    await fetchProcessData()
  } catch (error: unknown) {
    console.error('创建工艺数据失败:', error)
    const axiosError = error as AxiosError<{detail?: string}>
    ElMessage.error(axiosError.response?.data?.detail || '创建失败，请重试')
  } finally {
    submitting.value = false
  }
}

// 更新工艺数据
const updateProcessData = async (id: number, data: Partial<Omit<ProcessData, 'id' | 'created_at' | 'updated_at'>>) => {
  try {
    submitting.value = true
    await axiosInstance.put(`/${id}/update/`, data)
    ElMessage.success('更新成功')
    closeModal()
    await fetchProcessData()
  } catch (error: unknown) {
    console.error('更新工艺数据失败:', error)
    const axiosError = error as AxiosError<{detail?: string}>
    ElMessage.error(axiosError.response?.data?.detail || '更新失败，请重试')
  } finally {
    submitting.value = false
  }
}

// 删除工艺数据
const deleteProcessData = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个工艺数据吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axiosInstance.delete(`/${id}/delete/`)
    ElMessage.success('删除成功')
    await fetchProcessData()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除工艺数据失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除失败，请重试')
    }
  }
}

// 事件处理
const handleSubmit = async () => {
  if (showEditModal.value && currentEditItem.value) {
    await updateProcessData(currentEditItem.value.id, formData)
  } else {
    await createProcessData(formData)
  }
}

const editItem = (item: ProcessData) => {
  currentEditItem.value = item
  formData.name = item.name
  formData.description = item.description || ''
  formData.status = item.status
  showEditModal.value = true
}

const deleteItem = async (id: number) => {
  await deleteProcessData(id)
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  currentEditItem.value = null
  // 重置表单
  formData.name = ''
  formData.description = ''
  formData.status = 'active'
}

const handleSearch = () => {
  // 实际项目中应该调用搜索API
  // 这里简单过滤本地数据
  fetchProcessData()
}

const handleFilter = () => {
  // 实际项目中应该调用过滤API
  // 这里简单过滤本地数据
  fetchProcessData()
}

// 辅助函数
const formatDate = (dateString: string) => {
  if (!dateString) return '未知'
  return new Date(dateString).toLocaleString('zh-CN')
}

const getStatusText = (status: ProcessDataStatus) => {
  const statusMap: Record<ProcessDataStatus, string> = {
    active: '活跃',
    inactive: '非活跃'
  }
  return statusMap[status]
}

onMounted(() => {
  fetchProcessData()
})
</script>

<style scoped>
.process-data-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h2 {
  color: #333;
  margin: 0;
}

.create-btn {
  background-color: #4a90e2;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.create-btn:hover {
  background-color: #357abd;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.filter-select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  background-color: white;
}

.data-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.data-item {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.item-header h3 {
  margin: 0;
  color: #333;
}

.item-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-btn, .delete-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.edit-btn {
  background-color: #28a745;
  color: white;
}

.edit-btn:hover {
  background-color: #218838;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
}

.delete-btn:hover {
  background-color: #c82333;
}

.item-content p {
  margin: 0.5rem 0;
  color: #666;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.close-btn:hover {
  color: #333;
}

.modal-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.cancel-btn, .submit-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
}

.cancel-btn:hover {
  background-color: #5a6268;
}

.submit-btn {
  background-color: #4a90e2;
  color: white;
}

.submit-btn:hover {
  background-color: #357abd;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .process-data-container {
    padding: 1rem;
  }

  .header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .filters {
    flex-direction: column;
  }

  .item-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .item-actions {
    justify-content: flex-end;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style> 