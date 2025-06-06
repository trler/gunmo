<template>
  <div class="material-database">
    <el-container>
      <!-- 左侧导航 -->
      <el-aside width="240px" class="material-aside">
        <div class="aside-header">
          <h2>物料数据库</h2>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="material-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="block">
            <el-icon><i class="fas fa-cubes"></i></el-icon>
            <span>磨块管理</span>
          </el-menu-item>
          <el-menu-item index="chemical">
            <el-icon><i class="fas fa-flask"></i></el-icon>
            <span>化学剂管理</span>
          </el-menu-item>
          <el-menu-item index="fixture">
            <el-icon><i class="fas fa-tools"></i></el-icon>
            <span>工装管理</span>
          </el-menu-item>
          <el-menu-item index="equipment">
            <el-icon><i class="fas fa-cogs"></i></el-icon>
            <span>设备管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 中央内容区 -->
      <el-main class="material-main">
        <!-- 搜索和操作栏 -->
        <div class="operation-bar">
          <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item>
              <el-input
                v-model="searchForm.keyword"
                :placeholder="getSearchPlaceholder"
                clearable
                @clear="handleSearch"
                @keyup.enter="handleSearch"
              >
                <template #prefix>
                  <el-icon><i class="fas fa-search"></i></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearch">搜索</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>
          <div class="action-buttons">
            <el-button type="primary" @click="handleAdd">
              <el-icon><i class="fas fa-plus"></i></el-icon>
              新增{{ getCurrentTypeLabel }}
            </el-button>
            <el-button type="success" @click="handleImport">
              <el-icon><i class="fas fa-file-import"></i></el-icon>
              批量导入
            </el-button>
            <el-button type="warning" @click="handleExport">
              <el-icon><i class="fas fa-file-export"></i></el-icon>
              导出数据
            </el-button>
          </div>
        </div>

        <!-- 数据表格 -->
        <el-card class="data-table-card">
          <div class="table-wrapper">
            <el-table
              ref="tableRef"
              v-loading="loading"
              :data="tableData"
              border
              style="width: 100%"
              @selection-change="handleSelectionChange"
            >
              <el-table-column type="selection" width="55" />
              <component :is="currentTableColumns" />
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button-group>
                    <el-button type="primary" link @click="handleEdit(row)">
                      编辑
                    </el-button>
                    <el-button type="primary" link @click="handleView(row)">
                      查看
                    </el-button>
                    <el-button type="danger" link @click="handleDelete(row)">
                      删除
                    </el-button>
                  </el-button-group>
                </template>
              </el-table-column>
            </el-table>
          </div>

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

        <!-- 物料信息维护对话框 -->
        <el-dialog
          v-model="dialogVisible"
          :title="dialogTitle"
          width="900px"
          :close-on-click-modal="false"
          @close="handleDialogClose"
        >
          <component
            :is="currentFormComponent"
            v-if="dialogVisible"
            :form-data="currentFormData"
            :dialog-type="dialogType"
            @submit="handleFormSubmit"
            @cancel="handleDialogClose"
          />
        </el-dialog>

        <!-- 批量导入对话框 -->
        <el-dialog
          v-model="importDialogVisible"
          title="批量导入"
          width="500px"
        >
          <el-upload
            class="upload-demo"
            drag
            action="/api/material/import"
            :headers="uploadHeaders"
            :data="{ type: currentType }"
            :before-upload="beforeUpload"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
            :file-list="fileList"
          >
            <el-icon class="el-icon--upload"><i class="fas fa-cloud-upload-alt"></i></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 .xlsx, .xls 格式，文件大小不超过 10MB
              </div>
            </template>
          </el-upload>
        </el-dialog>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, markRaw, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useMaterialStore, type MaterialType } from '@/stores/material'
import BlockTableColumns from './components/BlockTableColumns.vue'
import ChemicalTableColumns from './components/ChemicalTableColumns.vue'
import FixtureTableColumns from './components/FixtureTableColumns.vue'
import EquipmentTableColumns from './components/EquipmentTableColumns.vue'
import BlockForm from './components/BlockForm.vue'
import ChemicalForm from './components/ChemicalForm.vue'
import FixtureForm from './components/FixtureForm.vue'
import EquipmentForm from './components/EquipmentForm.vue'
import type { UploadFile } from 'element-plus'

// 状态定义
const materialStore = useMaterialStore()
const loading = ref(false)
const activeMenu = ref('block')
const currentType = ref<MaterialType>('block')
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit' | 'view'>('add')
const importDialogVisible = ref(false)
const currentFormData = ref<any>(null)
const fileList = ref<UploadFile[]>([])
const selectedRows = ref<any[]>([])
const tableData = ref<any[]>([])
const tableRef = ref()

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 搜索表单
const searchForm = ref({
  keyword: '',
  type: '',
  status: ''
})

// 计算属性
const getCurrentTypeLabel = computed(() => {
  const typeMap: Record<string, string> = {
    block: '磨块',
    chemical: '化学剂',
    fixture: '工装',
    equipment: '设备'
  }
  return typeMap[currentType.value] || ''
})

const getSearchPlaceholder = computed(() => {
  const placeholderMap: Record<string, string> = {
    block: '搜索磨块编号、名称...',
    chemical: '搜索化学剂编号、名称...',
    fixture: '搜索工装编号、名称...',
    equipment: '搜索设备编号、名称...'
  }
  return placeholderMap[currentType.value] || '搜索...'
})

const dialogTitle = computed(() => {
  const actionMap: Record<string, string> = {
    add: '新增',
    edit: '编辑',
    view: '查看'
  }
  return `${actionMap[dialogType.value]}${getCurrentTypeLabel.value}`
})

const currentTableColumns = computed(() => {
  const componentMap: Record<string, any> = {
    block: BlockTableColumns,
    chemical: ChemicalTableColumns,
    fixture: FixtureTableColumns,
    equipment: EquipmentTableColumns
  }
  return markRaw(componentMap[currentType.value])
})

const currentFormComponent = computed(() => {
  const componentMap: Record<string, any> = {
    block: BlockForm,
    chemical: ChemicalForm,
    fixture: FixtureForm,
    equipment: EquipmentForm
  }
  return markRaw(componentMap[currentType.value])
})

// 上传相关
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${localStorage.getItem('token')}`
}))

// 方法定义
const handleMenuSelect = (index: string) => {
  currentType.value = index as MaterialType
  activeMenu.value = index
  resetSearch()
  loadData()
}

const loadData = async () => {
  loading.value = true
  try {
    const response = await materialStore.getMaterialList({
      type: currentType.value,
      page: currentPage.value,
      page_size: pageSize.value,
      ...searchForm.value
    })
    tableData.value = response.results
    total.value = response.count
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

const resetSearch = () => {
  searchForm.value = {
    keyword: '',
    type: '',
    status: ''
  }
  handleSearch()
}

const handleAdd = () => {
  dialogType.value = 'add'
  currentFormData.value = null
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  currentFormData.value = { ...row }
  dialogVisible.value = true
}

const handleView = (row: any) => {
  dialogType.value = 'view'
  currentFormData.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除该${getCurrentTypeLabel.value}吗？`,
      '警告',
      {
        type: 'warning'
      }
    )
    await materialStore.deleteMaterial(currentType.value, row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

const handleFormSubmit = async (formData: any) => {
  try {
    if (dialogType.value === 'add') {
      await materialStore.createMaterial(currentType.value, formData)
      ElMessage.success('添加成功')
    } else {
      await materialStore.updateMaterial(currentType.value, formData.id, formData)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  }
}

const handleDialogClose = () => {
  dialogVisible.value = false
  currentFormData.value = null
}

const handleSelectionChange = (selection: any[]) => {
  selectedRows.value = selection
}

const handleImport = () => {
  importDialogVisible.value = true
}

const handleExport = async () => {
  try {
    await materialStore.exportMaterial(currentType.value, {
      ids: selectedRows.value.map(row => row.id)
    })
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}

const beforeUpload = (file: File) => {
  const isExcel = /\.(xlsx|xls)$/.test(file.name.toLowerCase())
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isExcel) {
    ElMessage.error('只能上传 Excel 文件！')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB！')
    return false
  }
  return true
}

const handleUploadSuccess = (response: any) => {
  ElMessage.success('导入成功')
  importDialogVisible.value = false
  loadData()
}

const handleUploadError = () => {
  ElMessage.error('导入失败')
}

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
  nextTick(() => {
    // 确保表格布局正确更新
    if (tableRef.value) {
      tableRef.value.doLayout()
    }
  })
  loadData()
})
</script>

<style scoped>
.material-database {
  height: 100%;
  background-color: #f5f7fa;
}

.material-aside {
  background-color: #fff;
  border-right: 1px solid #e6e6e6;
  position: relative;
  z-index: 100;
}

.aside-header {
  padding: 20px;
  border-bottom: 1px solid #e6e6e6;
}

.aside-header h2 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.material-menu {
  border-right: none;
}

.material-main {
  padding: 20px;
  position: relative;
  z-index: 1;
}

.operation-bar {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: transparent;
  position: relative;
  z-index: 1;
}

.search-form {
  display: flex;
  align-items: center;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.data-table-card {
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
}

.table-wrapper {
  overflow-x: auto;
  border-radius: 4px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  padding: 20px;
  border-top: 1px solid #ebeef5;
}

.upload-demo {
  text-align: center;
}

.el-upload__tip {
  color: #909399;
  font-size: 12px;
  margin-top: 5px;
}

:deep(.el-menu-item) {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.el-icon) {
  margin-right: 4px;
}

:deep(.el-container) {
  position: relative;
}

:deep(.el-aside) {
  position: relative;
  z-index: 100;
}

:deep(.el-main) {
  position: relative;
  z-index: 1;
}

/* 优化表格滚动条样式 */
.table-wrapper::-webkit-scrollbar {
  height: 8px;
}

.table-wrapper::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 表格样式优化 */
:deep(.el-table) {
  border-radius: 4px;
}

:deep(.el-table th) {
  background-color: #fafafa;
  color: #606266;
  font-weight: 600;
}

:deep(.el-table__fixed-right) {
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
}
</style> 