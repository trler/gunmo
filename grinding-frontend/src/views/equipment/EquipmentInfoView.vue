<template>
  <div class="equipment-info">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-cogs"></i>
        设备信息管理
      </h1>
      <p class="page-description">管理滚磨光整设备的基本信息和状态</p>
    </div>

    <!-- 搜索栏 -->
    <el-card class="search-card" shadow="never">
      <el-form :model="searchForm" :inline="true" class="search-form">
        <el-form-item label="设备编号">
          <el-input v-model="searchForm.equipment_code" placeholder="输入设备编号" clearable />
        </el-form-item>
        <el-form-item label="设备名称">
          <el-input v-model="searchForm.name" placeholder="输入设备名称" clearable />
        </el-form-item>
        <el-form-item label="设备状态">
          <el-select v-model="searchForm.status" placeholder="选择状态" clearable>
            <el-option label="运行中" value="running" />
            <el-option label="空闲" value="idle" />
            <el-option label="维护中" value="maintenance" />
            <el-option label="故障" value="error" />
            <el-option label="离线" value="offline" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <i class="fas fa-search"></i>
            搜索
          </el-button>
          <el-button @click="resetSearch">
            <i class="fas fa-undo"></i>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 操作栏 -->
    <el-card class="action-card" shadow="never">
      <div class="action-bar">
        <div class="action-left">
          <el-button type="primary" @click="handleAdd">
            <i class="fas fa-plus"></i>
            新增设备
          </el-button>
          <el-button type="success" @click="handleImport">
            <i class="fas fa-upload"></i>
            批量导入
          </el-button>
        </div>
        <div class="action-right">
          <el-button @click="handleExport">
            <i class="fas fa-download"></i>
            导出数据
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-card">
      <el-table :data="tableData" v-loading="loading" border>
        <el-table-column prop="code" label="设备编号" width="120" />
        <el-table-column prop="name" label="设备名称" width="150" />
        <el-table-column prop="model" label="设备型号" width="120" />
        <el-table-column prop="manufacturer" label="制造商" width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="location" label="设备位置" width="120" />
        <el-table-column prop="workshop" label="所属车间" width="120" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="info" link @click="handleMaintenance(row)">维护记录</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增设备' : '编辑设备'"
      width="600px"
    >
      <div class="form-content">
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="100px"
          class="equipment-form"
        >
          <el-form-item label="设备编号" prop="code">
            <el-input v-model="form.code" placeholder="请输入设备编号" />
          </el-form-item>
          <el-form-item label="设备名称" prop="name">
            <el-input v-model="form.name" placeholder="请输入设备名称" />
          </el-form-item>
          <el-form-item label="设备型号" prop="model">
            <el-input v-model="form.model" placeholder="请输入设备型号" />
          </el-form-item>
          <el-form-item label="制造商" prop="manufacturer">
            <el-input v-model="form.manufacturer" placeholder="请输入制造商" />
          </el-form-item>
          <el-form-item label="设备状态" prop="status">
            <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%">
              <el-option label="运行中" value="running" />
              <el-option label="空闲" value="idle" />
              <el-option label="维护中" value="maintenance" />
              <el-option label="故障" value="error" />
              <el-option label="离线" value="offline" />
            </el-select>
          </el-form-item>
          <el-form-item label="设备位置" prop="location">
            <el-input v-model="form.location" placeholder="请输入设备位置" />
          </el-form-item>
          <el-form-item label="所属车间" prop="workshop">
            <el-input v-model="form.workshop" placeholder="请输入所属车间" />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 维护记录对话框 -->
    <el-dialog
      v-model="maintenanceDialogVisible"
      title="维护记录"
      width="800px"
    >
      <div class="maintenance-content">
        <p>维护记录功能开发中...</p>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

// 搜索表单
const searchForm = reactive({
  equipment_code: '',
  name: '',
  status: ''
})

// 表格数据
const loading = ref(false)
const tableData = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 对话框控制
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const maintenanceDialogVisible = ref(false)
const formRef = ref<FormInstance>()

// 表单数据
const form = reactive({
  id: '',
  code: '',
  name: '',
  model: '',
  manufacturer: '',
  status: '',
  location: '',
  workshop: ''
})

// 表单验证规则
const rules: FormRules = {
  code: [
    { required: true, message: '请输入设备编号', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入设备名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  model: [
    { required: true, message: '请输入设备型号', trigger: 'blur' }
  ],
  manufacturer: [
    { required: true, message: '请输入制造商', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择设备状态', trigger: 'change' }
  ],
  location: [
    { required: true, message: '请输入设备位置', trigger: 'blur' }
  ],
  workshop: [
    { required: true, message: '请输入所属车间', trigger: 'blur' }
  ]
}

// 获取状态类型
const getStatusType = (status: string): 'success' | 'info' | 'warning' | 'danger' => {
  const statusMap: Record<string, 'success' | 'info' | 'warning' | 'danger'> = {
    running: 'success',
    idle: 'info',
    maintenance: 'warning',
    error: 'danger',
    offline: 'info'
  }
  return statusMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string): string => {
  const textMap: Record<string, string> = {
    running: '运行中',
    idle: '空闲',
    maintenance: '维护中',
    error: '故障',
    offline: '离线'
  }
  return textMap[status] || '未知'
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 模拟数据
    tableData.value = [
      {
        id: 1,
        code: 'EQ001',
        name: '振动研磨机A',
        model: 'VM-2000',
        manufacturer: '某设备厂',
        status: 'running',
        location: 'A车间',
        workshop: '生产车间一'
      },
      {
        id: 2,
        code: 'EQ002',
        name: '离心研磨机B',
        model: 'CM-1500',
        manufacturer: '某设备厂',
        status: 'idle',
        location: 'B车间',
        workshop: '生产车间二'
      },
      {
        id: 3,
        code: 'EQ003',
        name: '流动研磨机C',
        model: 'FM-3000',
        manufacturer: '某设备厂',
        status: 'maintenance',
        location: 'C车间',
        workshop: '生产车间三'
      }
    ]
    total.value = 3
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

// 重置搜索
const resetSearch = () => {
  searchForm.equipment_code = ''
  searchForm.name = ''
  searchForm.status = ''
  handleSearch()
}

// 新增
const handleAdd = () => {
  dialogType.value = 'add'
  Object.assign(form, {
    id: '',
    code: '',
    name: '',
    model: '',
    manufacturer: '',
    status: '',
    location: '',
    workshop: ''
  })
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  Object.assign(form, row)
  dialogVisible.value = true
}

// 删除
const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除这个设备吗？', '确认删除', {
      type: 'warning'
    })
    ElMessage.success('删除成功')
    loadData()
  } catch {
    // 用户取消删除
  }
}

// 维护记录
const handleMaintenance = (row: any) => {
  maintenanceDialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    if (dialogType.value === 'add') {
      ElMessage.success('设备添加成功')
    } else {
      ElMessage.success('设备更新成功')
    }
    
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

// 导入
const handleImport = () => {
  ElMessage.success('批量导入功能开发中')
}

// 导出
const handleExport = () => {
  ElMessage.success('数据导出功能开发中')
}

// 分页
const handleSizeChange = (val: number) => {
  pageSize.value = val
  loadData()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadData()
}

// 初始化
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.equipment-info {
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

.search-card, .action-card {
  margin-bottom: 16px;
}

.search-form {
  margin: 0;
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-left, .action-right {
  display: flex;
  gap: 8px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  padding: 20px;
  border-top: 1px solid #ebeef5;
}

.form-content, .maintenance-content {
  padding: 20px 0;
}

:deep(.el-card__body) {
  padding: 20px;
}
</style> 