<template>
  <div class="equipment-container">
    <div class="header">
      <h2>设备管理</h2>
      <button @click="showCreateModal = true" class="create-btn">
        添加设备
      </button>
    </div>

    <!-- 搜索和过滤 -->
    <div class="filters">
      <input
        v-model="searchQuery"
        @input="handleSearch"
        placeholder="搜索设备..."
        class="search-input"
      />
      <select v-model="statusFilter" @change="handleFilter" class="filter-select">
        <option value="">所有状态</option>
        <option value="running">运行中</option>
        <option value="idle">空闲</option>
        <option value="maintenance">维护中</option>
        <option value="error">故障</option>
        <option value="offline">离线</option>
      </select>
      <select v-model="typeFilter" @change="handleFilter" class="filter-select">
        <option value="">所有类型</option>
        <option v-for="type in equipmentTypes" :key="type.id" :value="type.id">
          {{ type.name }}
        </option>
      </select>
    </div>

    <!-- 设备列表 -->
    <div class="equipment-list" v-if="!loading">
      <div v-if="equipmentList.length === 0" class="empty-state">
        <p>暂无设备数据</p>
      </div>
      <div v-else class="equipment-grid">
        <div
          v-for="item in equipmentList"
          :key="item.id"
          class="equipment-card"
          :class="item.status"
        >
          <div class="card-header">
            <h3>{{ item.name }}</h3>
            <div class="status-badge" :class="item.status">
              {{ getStatusText(item.status) }}
            </div>
          </div>
          <div class="card-content">
            <p><strong>设备类型:</strong> {{ item.type?.name || '未分类' }}</p>
            <p><strong>设备编号:</strong> {{ item.serial_number || '未知' }}</p>
            <p><strong>位置:</strong> {{ item.location || '未知' }}</p>
            <p><strong>最后维护:</strong> {{ formatDate(item.last_maintenance) }}</p>
            <p v-if="item.description"><strong>描述:</strong> {{ item.description }}</p>
          </div>
          <div class="card-actions">
            <button @click="editItem(item)" class="edit-btn">编辑</button>
            <button @click="updateStatus(item)" class="status-btn">
              更新状态
            </button>
            <button @click="deleteItem(item.id)" class="delete-btn">删除</button>
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
          <h3>{{ showEditModal ? '编辑设备' : '添加设备' }}</h3>
          <button @click="closeModal" class="close-btn">×</button>
        </div>
        <form @submit.prevent="handleSubmit" class="modal-form">
          <div class="form-group">
            <label for="name">设备名称</label>
            <input
              type="text"
              id="name"
              v-model="formData.name"
              required
              placeholder="请输入设备名称"
            />
          </div>

          <div class="form-group">
            <label for="type">设备类型</label>
            <select id="type" v-model="formData.type" required>
              <option value="">请选择设备类型</option>
              <option v-for="type in equipmentTypes" :key="type.id" :value="type.id">
                {{ type.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="serialNumber">设备编号</label>
            <input
              type="text"
              id="serialNumber"
              v-model="formData.serial_number"
              required
              placeholder="请输入设备编号"
            />
          </div>

          <div class="form-group">
            <label for="location">位置</label>
            <input
              type="text"
              id="location"
              v-model="formData.location"
              placeholder="请输入设备位置"
            />
          </div>

          <div class="form-group">
            <label for="status">状态</label>
            <select id="status" v-model="formData.status" required>
              <option value="running">运行中</option>
              <option value="idle">空闲</option>
              <option value="maintenance">维护中</option>
              <option value="error">故障</option>
              <option value="offline">离线</option>
            </select>
          </div>

          <div class="form-group">
            <label for="description">描述</label>
            <textarea
              id="description"
              v-model="formData.description"
              placeholder="请输入设备描述"
              rows="3"
            ></textarea>
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

    <!-- 状态更新模态框 -->
    <div v-if="showStatusModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>更新设备状态</h3>
          <button @click="closeStatusModal" class="close-btn">×</button>
        </div>
        <form @submit.prevent="handleStatusUpdate" class="modal-form">
          <div class="form-group">
            <label for="newStatus">新状态</label>
            <select id="newStatus" v-model="statusForm.status" required>
              <option value="running">运行中</option>
              <option value="idle">空闲</option>
              <option value="maintenance">维护中</option>
              <option value="error">故障</option>
              <option value="offline">离线</option>
            </select>
          </div>

          <div class="form-group">
            <label for="statusNote">备注</label>
            <textarea
              id="statusNote"
              v-model="statusForm.note"
              placeholder="请输入状态更新备注"
              rows="3"
            ></textarea>
          </div>

          <div class="form-actions">
            <button type="button" @click="closeStatusModal" class="cancel-btn">
              取消
            </button>
            <button type="submit" :disabled="submitting" class="submit-btn">
              {{ submitting ? '更新中...' : '更新状态' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axiosInstance from '@/api/axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Equipment, EquipmentType, EquipmentStatus } from '@/types/auth'
import type { AxiosError } from 'axios'
import type { AuthError } from '@/types/auth'

// 状态管理
const loading = ref(false)
const submitting = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showStatusModal = ref(false)
const equipmentList = ref<Equipment[]>([])
const equipmentTypes = ref<EquipmentType[]>([])
const currentEditItem = ref<Equipment | null>(null)
const currentStatusItem = ref<Equipment | null>(null)

// 搜索和过滤
const searchQuery = ref('')
const statusFilter = ref<EquipmentStatus | ''>('')
const typeFilter = ref<number | ''>('')

// 表单数据
interface EquipmentForm {
  name: string
  type: string
  serial_number: string
  location: string
  status: EquipmentStatus
  description: string
}

const formData = reactive<EquipmentForm>({
  name: '',
  type: '',
  serial_number: '',
  location: '',
  status: 'running',
  description: ''
})

// 状态更新表单
interface StatusForm {
  status: EquipmentStatus
  note: string
}

const statusForm = reactive<StatusForm>({
  status: 'running',
  note: ''
})

// 获取设备类型列表
const fetchEquipmentTypes = async () => {
  try {
    const response = await axiosInstance.get('/equipment-types/')
    equipmentTypes.value = response.data.results || response.data || []
  } catch (err: unknown) {
    const error = err as AxiosError<AuthError>
    console.error('获取设备类型失败:', error)
    ElMessage.error(error.response?.data?.detail || '获取设备类型失败，请重试')
  }
}

// 获取设备列表
const fetchEquipment = async () => {
  try {
    loading.value = true
    const response = await axiosInstance.get('/')
    equipmentList.value = response.data.results || response.data || []
  } catch (err: unknown) {
    const error = err as AxiosError<AuthError>
    console.error('获取设备列表失败:', error)
    ElMessage.error(error.response?.data?.detail || '获取设备列表失败，请重试')
  } finally {
    loading.value = false
  }
}

// 创建设备
const createEquipment = async (data: Record<string, any>) => {
  try {
    submitting.value = true
    await axiosInstance.post('/create/', data)
    ElMessage.success('创建成功')
    closeModal()
    await fetchEquipment()
  } catch (error: unknown) {
    console.error('创建设备失败:', error)
    const axiosError = error as AxiosError<{detail?: string}>
    ElMessage.error(axiosError.response?.data?.detail || '创建失败，请重试')
  } finally {
    submitting.value = false
  }
}

// 更新设备
const updateEquipment = async (id: number, data: Record<string, any>) => {
  try {
    submitting.value = true
    await axiosInstance.put(`/${id}/update/`, data)
    ElMessage.success('更新成功')
    closeModal()
    await fetchEquipment()
  } catch (error: unknown) {
    console.error('更新设备失败:', error)
    const axiosError = error as AxiosError<{detail?: string}>
    ElMessage.error(axiosError.response?.data?.detail || '更新失败，请重试')
  } finally {
    submitting.value = false
  }
}

// 更新设备状态
const updateEquipmentStatus = async (id: number, data: Record<string, any>) => {
  try {
    submitting.value = true
    await axiosInstance.patch(`/${id}/status/`, data)
    ElMessage.success('状态更新成功')
    closeStatusModal()
    await fetchEquipment()
  } catch (error: unknown) {
    console.error('更新设备状态失败:', error)
    const axiosError = error as AxiosError<{detail?: string}>
    ElMessage.error(axiosError.response?.data?.detail || '更新失败，请重试')
  } finally {
    submitting.value = false
  }
}

// 删除设备
const deleteEquipment = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个设备吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axiosInstance.delete(`/${id}/delete/`)
    ElMessage.success('删除成功')
    await fetchEquipment()
  } catch (error: unknown) {
    if (error !== 'cancel') {
      console.error('删除设备失败:', error)
      const axiosError = error as AxiosError<{detail?: string}>
      ElMessage.error(axiosError.response?.data?.detail || '删除失败，请重试')
    }
  }
}

// 事件处理
const handleSubmit = async () => {
  if (showEditModal.value && currentEditItem.value) {
    await updateEquipment(currentEditItem.value.id, formData)
  } else {
    await createEquipment(formData)
  }
}

const handleStatusUpdate = async () => {
  if (currentStatusItem.value) {
    await updateEquipmentStatus(currentStatusItem.value.id, statusForm)
  }
}

const editItem = (item: Equipment) => {
  currentEditItem.value = item
  formData.name = item.name
  formData.type = item.type.id.toString()
  formData.serial_number = item.serial_number
  formData.location = item.location
  formData.status = item.status
  formData.description = item.description || ''
  showEditModal.value = true
}

const updateStatus = (item: Equipment) => {
  currentStatusItem.value = item
  statusForm.status = item.status
  statusForm.note = ''
  showStatusModal.value = true
}

const deleteItem = async (id: number) => {
  if (confirm('确定要删除这个设备吗？')) {
    await deleteEquipment(id)
  }
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  currentEditItem.value = null
  // 重置表单
  formData.name = ''
  formData.type = ''
  formData.serial_number = ''
  formData.location = ''
  formData.status = 'running'
  formData.description = ''
}

const closeStatusModal = () => {
  showStatusModal.value = false
  currentStatusItem.value = null
  // 重置状态表单
  statusForm.status = 'running'
  statusForm.note = ''
}

const handleSearch = () => {
  // 实际项目中应该调用搜索API
  // 这里简单过滤本地数据
  fetchEquipment()
}

const handleFilter = () => {
  // 实际项目中应该调用过滤API
  // 这里简单过滤本地数据
  fetchEquipment()
}

// 辅助函数
const formatDate = (dateString: string) => {
  if (!dateString) return '未知'
  return new Date(dateString).toLocaleString('zh-CN')
}

const getStatusText = (status: EquipmentStatus) => {
  const statusMap: Record<EquipmentStatus, string> = {
    running: '运行中',
    idle: '空闲',
    maintenance: '维护中',
    error: '故障',
    offline: '离线'
  }
  return statusMap[status]
}

onMounted(() => {
  fetchEquipmentTypes()
  fetchEquipment()
})
</script>

<style scoped>
.equipment-container {
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
  min-width: 150px;
}

.equipment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
  background-color: #f9f9f9;
  border-radius: 8px;
  grid-column: 1 / -1;
}

.equipment-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.equipment-card.running {
  border-left: 4px solid #28a745;
}

.equipment-card.idle {
  border-left: 4px solid #17a2b8;
}

.equipment-card.maintenance {
  border-left: 4px solid #ffc107;
}

.equipment-card.error {
  border-left: 4px solid #dc3545;
}

.equipment-card.offline {
  border-left: 4px solid #6c757d;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  color: #333;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.running {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.idle {
  background-color: #cce5ff;
  color: #004085;
}

.status-badge.maintenance {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.error {
  background-color: #f8d7da;
  color: #721c24;
}

.status-badge.offline {
  background-color: #e2e3e5;
  color: #383d41;
}

.card-content p {
  margin: 0.5rem 0;
  color: #666;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: auto;
}

.edit-btn, .status-btn, .delete-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  flex: 1;
}

.edit-btn {
  background-color: #28a745;
  color: white;
}

.edit-btn:hover {
  background-color: #218838;
}

.status-btn {
  background-color: #17a2b8;
  color: white;
}

.status-btn:hover {
  background-color: #138496;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
}

.delete-btn:hover {
  background-color: #c82333;
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
  .equipment-container {
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

  .equipment-grid {
    grid-template-columns: 1fr;
  }

  .card-actions {
    flex-direction: column;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style> 