<template>
  <div class="fixture-management">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>工装管理</span>
          <el-button type="primary" @click="handleAdd">新增工装</el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="工装编号">
          <el-input v-model="searchForm.code" placeholder="请输入工装编号" clearable />
        </el-form-item>
        <el-form-item label="工装名称">
          <el-input v-model="searchForm.name" placeholder="请输入工装名称" clearable />
        </el-form-item>
        <el-form-item label="工装类型">
          <el-select v-model="searchForm.type" placeholder="请选择类型" clearable>
            <el-option
              v-for="type in fixtureTypes"
              :key="type"
              :label="type"
              :value="type"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格区域 -->
      <el-table
        v-loading="loading"
        :data="tableData"
        border
        style="width: 100%"
      >
        <el-table-column prop="code" label="工装编号" width="150" />
        <el-table-column prop="name" label="工装名称" width="150" />
        <el-table-column prop="type" label="类型" width="120" />
        <el-table-column prop="manufacturer" label="生产厂家" width="150" />
        <el-table-column prop="partType" label="适用零件类型" width="150" />
        <el-table-column prop="size" label="工装尺寸" width="120" />
        <el-table-column prop="accuracy" label="定位精度" width="120" />
        <el-table-column prop="clampingForce" label="最大夹持力" width="120" />
        <el-table-column prop="material" label="材质" width="100">
          <template #default="{ row }">
            {{ getMaterialLabel(row.material) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
              <el-button type="primary" link @click="handleViewFiles(row)">查看文件</el-button>
              <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
            </el-button-group>
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

    <!-- 工装信息维护对话框 -->
    <el-dialog
      :title="dialogType === 'add' ? '新增工装' : '编辑工装'"
      v-model="dialogVisible"
      width="800px"
      @close="resetForm"
    >
      <el-form :model="fixtureForm" label-width="120px" :rules="rules" ref="formRef">
        <el-row :gutter="20">
          <el-col :span="12">
            <!-- 左栏：基本信息 -->
            <el-form-item label="工装编号" prop="code">
              <el-input v-model="fixtureForm.code" placeholder="唯一标识（如FX-2024-001）" />
            </el-form-item>
            <el-form-item label="工装名称" prop="name">
              <el-input v-model="fixtureForm.name" placeholder="如：轴类定位工装" />
            </el-form-item>
            <el-form-item label="类型" prop="type">
              <el-select v-model="fixtureForm.type" placeholder="选择类型">
                <el-option
                  v-for="type in fixtureTypes"
                  :key="type"
                  :label="type"
                  :value="type"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="生产厂家" prop="manufacturer">
              <el-select v-model="fixtureForm.manufacturer" placeholder="选择厂家">
                <el-option
                  v-for="factory in manufacturers"
                  :key="factory"
                  :label="factory"
                  :value="factory"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="适用零件类型" prop="partType">
              <el-input v-model="fixtureForm.partType" placeholder="如：轴类、齿轮类、叶片类" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <!-- 右栏：技术参数 -->
            <el-form-item label="工装尺寸" prop="size">
              <el-input v-model="fixtureForm.size" placeholder="单位：mm（如 Φ50×100）" />
            </el-form-item>
            <el-form-item label="定位精度" prop="accuracy">
              <el-input v-model="fixtureForm.accuracy" placeholder="单位：μm（如 ±0.02）" />
            </el-form-item>
            <el-form-item label="最大夹持力" prop="clampingForce">
              <el-input v-model="fixtureForm.clampingForce" placeholder="单位：N（如 5000）" />
            </el-form-item>
            <el-form-item label="材质" prop="material">
              <el-select v-model="fixtureForm.material" placeholder="选择材质">
                <el-option label="45#钢" value="45steel" />
                <el-option label="铝合金" value="aluminum" />
                <el-option label="工程塑料" value="plastic" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="margin-top: 20px">
          <el-col :span="24">
            <!-- 文件上传：工装图纸、使用说明 -->
            <el-upload
              class="upload-demo"
              action="/api/fixtures/upload"
              :file-list="fileList"
              :on-remove="handleRemove"
              :before-upload="beforeUpload"
              :on-success="handleUploadSuccess"
              :on-error="handleUploadError"
            >
              <el-button size="small" type="primary">选择文件</el-button>
              <div class="el-upload__tip">
                支持PDF、DWG格式，单文件≤2MB
              </div>
            </el-upload>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="resetForm">取消</el-button>
        <el-button type="primary" @click="submitForm">确认保存</el-button>
      </template>
    </el-dialog>

    <!-- 文件查看对话框 -->
    <el-dialog
      title="工装文件"
      v-model="fileDialogVisible"
      width="600px"
    >
      <el-table :data="currentFiles" border style="width: 100%">
        <el-table-column prop="name" label="文件名" />
        <el-table-column prop="size" label="大小" width="120">
          <template #default="{ row }">
            {{ formatFileSize(row.size) }}
          </template>
        </el-table-column>
        <el-table-column prop="uploadTime" label="上传时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleDownload(row)">下载</el-button>
            <el-button type="danger" link @click="handleDeleteFile(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus/es/components/form'
import type { UploadFile } from 'element-plus/es/components/upload/src/upload'
import axiosInstance from '@/api/axios'

// 状态定义
const loading = ref(false)
const dialogVisible = ref(false)
const fileDialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const formRef = ref<FormInstance>()
const fileList = ref<UploadFile[]>([])
const currentFiles = ref<any[]>([])
const tableData = ref<any[]>([])

// 搜索表单
const searchForm = reactive({
  code: '',
  name: '',
  type: ''
})

// 工装表单
const fixtureForm = reactive({
  id: '',
  code: '',
  name: '',
  type: '',
  manufacturer: '',
  partType: '',
  size: '',
  accuracy: '',
  clampingForce: '',
  material: '45steel',
  remark: ''
})

// 表单验证规则
const rules = {
  code: [
    { required: true, message: '请输入工装编号', trigger: 'blur' },
    { pattern: /^FX-\d{4}-\d{3}$/, message: '工装编号格式为：FX-YYYY-XXX', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入工装名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择工装类型', trigger: 'change' }
  ],
  manufacturer: [
    { required: true, message: '请选择生产厂家', trigger: 'change' }
  ],
  partType: [
    { required: true, message: '请输入适用零件类型', trigger: 'blur' }
  ],
  size: [
    { required: true, message: '请输入工装尺寸', trigger: 'blur' }
  ],
  accuracy: [
    { required: true, message: '请输入定位精度', trigger: 'blur' }
  ],
  clampingForce: [
    { required: true, message: '请输入最大夹持力', trigger: 'blur' }
  ],
  material: [
    { required: true, message: '请选择材质', trigger: 'change' }
  ]
}

// 常量定义
const fixtureTypes = ['定位工装', '夹持工装', '检测工装', '辅助工装']
const manufacturers = ['工装企业A', '精密制造B', '进口品牌C']

// 获取材质标签
const getMaterialLabel = (material: string) => {
  const materialMap: Record<string, string> = {
    '45steel': '45#钢',
    'aluminum': '铝合金',
    'plastic': '工程塑料'
  }
  return materialMap[material] || material
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const response = await axiosInstance.get('/fixtures/', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value,
        ...searchForm
      }
    })
    // TODO: 根据实际API响应结构调整
    tableData.value = response.data.results || []
    total.value = response.data.count || 0
  } catch (error) {
    console.error('加载工装列表失败:', error)
    ElMessage.error('加载工装列表失败')
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
  Object.keys(searchForm).forEach(key => {
    searchForm[key as keyof typeof searchForm] = ''
  })
  handleSearch()
}

// 新增工装
const handleAdd = () => {
  dialogType.value = 'add'
  Object.keys(fixtureForm).forEach(key => {
    fixtureForm[key as keyof typeof fixtureForm] = ''
  })
  fixtureForm.material = '45steel'
  fileList.value = []
  dialogVisible.value = true
}

// 编辑工装
const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  Object.assign(fixtureForm, row)
  // TODO: 加载工装相关文件
  dialogVisible.value = true
}

// 删除工装
const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该工装吗？', '警告', {
      type: 'warning'
    })
    await axiosInstance.delete(`/fixtures/${row.id}/`)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除工装失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 查看文件
const handleViewFiles = async (row: any) => {
  try {
    const response = await axiosInstance.get(`/fixtures/${row.id}/files/`)
    currentFiles.value = response.data
    fileDialogVisible.value = true
  } catch (error) {
    console.error('获取工装文件失败:', error)
    ElMessage.error('获取工装文件失败')
  }
}

// 文件上传相关
const beforeUpload = (file: File) => {
  const isPDF = file.type === 'application/pdf'
  const isDWG = file.name.toLowerCase().endsWith('.dwg')
  const isSizeValid = file.size <= 2 * 1024 * 1024

  if (!isPDF && !isDWG) {
    ElMessage.error('只能上传PDF或DWG文件！')
    return false
  }
  if (!isSizeValid) {
    ElMessage.error('文件大小不能超过2MB！')
    return false
  }
  return true
}

const handleUploadSuccess = (response: any, file: UploadFile) => {
  ElMessage.success('文件上传成功')
  fileList.value.push(file)
}

const handleUploadError = () => {
  ElMessage.error('文件上传失败')
}

const handleRemove = (file: UploadFile) => {
  const index = fileList.value.indexOf(file)
  if (index !== -1) {
    fileList.value.splice(index, 1)
  }
}

// 文件下载
const handleDownload = async (file: any) => {
  try {
    const response = await axiosInstance.get(`/fixtures/files/${file.id}/download/`, {
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', file.name)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (error) {
    console.error('文件下载失败:', error)
    ElMessage.error('文件下载失败')
  }
}

// 删除文件
const handleDeleteFile = async (file: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该文件吗？', '警告', {
      type: 'warning'
    })
    await axiosInstance.delete(`/fixtures/files/${file.id}/`)
    ElMessage.success('文件删除成功')
    handleViewFiles({ id: file.fixtureId })
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除文件失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 格式化文件大小
const formatFileSize = (size: number) => {
  if (size < 1024) {
    return size + ' B'
  } else if (size < 1024 * 1024) {
    return (size / 1024).toFixed(2) + ' KB'
  } else {
    return (size / (1024 * 1024)).toFixed(2) + ' MB'
  }
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const formData = new FormData()
        Object.keys(fixtureForm).forEach(key => {
          formData.append(key, fixtureForm[key as keyof typeof fixtureForm])
        })
        
        if (dialogType.value === 'add') {
          await axiosInstance.post('/fixtures/', formData)
          ElMessage.success('添加成功')
        } else {
          await axiosInstance.put(`/fixtures/${fixtureForm.id}/`, formData)
          ElMessage.success('更新成功')
        }
        
        dialogVisible.value = false
        loadData()
      } catch (error) {
        console.error('保存工装失败:', error)
        ElMessage.error(dialogType.value === 'add' ? '添加失败' : '更新失败')
      }
    }
  })
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  dialogVisible.value = false
  fileList.value = []
}

// 分页处理
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
.fixture-management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.upload-demo {
  margin-top: 20px;
}

.el-upload__tip {
  color: #909399;
  font-size: 12px;
  margin-top: 5px;
}
</style> 