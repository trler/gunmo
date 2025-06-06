<template>
  <div class="block-info-view">
    <div class="page-header">
      <h1>磨块信息管理</h1>
      <div class="header-actions">
        <el-button type="primary" @click="showDialog">
          <el-icon><Plus /></el-icon>
          新增磨块
        </el-button>
      </div>
    </div>

    <!-- 搜索和过滤区域 -->
    <div class="search-bar">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="磨块编号">
          <el-input v-model="searchForm.blockNo" placeholder="请输入磨块编号" clearable />
        </el-form-item>
        <el-form-item label="磨块类型">
          <el-select v-model="searchForm.blockType" placeholder="请选择类型" clearable>
            <el-option
              v-for="type in blockTypes"
              :key="type.value"
              :label="type.label"
              :value="type.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="磨块厂家">
          <el-select v-model="searchForm.blockFactory" placeholder="请选择厂家" clearable>
            <el-option
              v-for="factory in factories"
              :key="factory.value"
              :label="factory.label"
              :value="factory.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="resetSearch">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 数据表格 -->
    <el-table
      v-loading="loading"
      :data="tableData"
      border
      style="width: 100%"
      class="block-table"
    >
      <el-table-column prop="blockNo" label="磨块编号" min-width="120" />
      <el-table-column prop="blockName" label="磨块名称" min-width="120" />
      <el-table-column prop="blockType" label="磨块类型" min-width="120">
        <template #default="{ row }">
          {{ getBlockTypeLabel(row.blockType) }}
        </template>
      </el-table-column>
      <el-table-column prop="blockFactory" label="磨块厂家" min-width="120">
        <template #default="{ row }">
          {{ getFactoryLabel(row.blockFactory) }}
        </template>
      </el-table-column>
      <el-table-column prop="blockShape" label="磨块形状" min-width="120">
        <template #default="{ row }">
          {{ getShapeLabel(row.blockShape) }}
        </template>
      </el-table-column>
      <el-table-column prop="blockMaterial" label="磨块材质" min-width="100" />
      <el-table-column prop="weight" label="重量(g)" min-width="100" />
      <el-table-column prop="wearRate" label="磨耗率(%)" min-width="100" />
      <el-table-column prop="grindingRate" label="磨削率(%)" min-width="100" />
      <el-table-column prop="batch" label="批次" min-width="120" />
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

    <!-- 磨块信息维护对话框 -->
    <block-info-dialog
      v-model="dialogVisible"
      @submit="handleSubmit"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import BlockInfoDialog from '@/components/BlockInfoDialog.vue'
import type { BlockFormData } from '@/components/BlockInfoDialog.vue'
import axiosInstance from '@/api/axios'

// 搜索表单
const searchForm = reactive({
  blockNo: '',
  blockType: '',
  blockFactory: ''
})

// 表格数据
const loading = ref(false)
const tableData = ref<BlockFormData[]>([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 对话框控制
const dialogVisible = ref(false)

// 下拉选项数据（与 BlockInfoDialog 组件保持一致）
const blockTypes = [
  { value: 'white_alumina', label: '白刚玉磨料' },
  { value: 'brown_alumina', label: '棕刚玉磨料' },
  { value: 'silicon_carbide', label: '碳化硅磨料' }
]

const factories = [
  { value: 'factory_a', label: '厂家A' },
  { value: 'factory_b', label: '厂家B' },
  { value: 'factory_c', label: '厂家C' }
]

const shapes = [
  { value: 'spherical', label: '圆球形' },
  { value: 'cylindrical', label: '圆柱形' },
  { value: 'triangular', label: '三角形' }
]

// 获取选项标签的辅助函数
const getBlockTypeLabel = (value: string) => {
  return blockTypes.find(type => type.value === value)?.label || value
}

const getFactoryLabel = (value: string) => {
  return factories.find(factory => factory.value === value)?.label || value
}

const getShapeLabel = (value: string) => {
  return shapes.find(shape => shape.value === value)?.label || value
}

// 获取磨块列表
const fetchBlockList = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      ...searchForm
    }
    const response = await axiosInstance.get('/blocks/', { params })
    tableData.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('获取磨块列表失败:', error)
    ElMessage.error('获取磨块列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索和重置
const handleSearch = () => {
  currentPage.value = 1
  fetchBlockList()
}

const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key as keyof typeof searchForm] = ''
  })
  handleSearch()
}

// 分页处理
const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchBlockList()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchBlockList()
}

// 对话框操作
const showDialog = () => {
  dialogVisible.value = true
}

// 表单提交处理
const handleSubmit = async (data: BlockFormData) => {
  try {
    if (data.id) {
      // 更新
      await axiosInstance.put(`/blocks/${data.id}/`, data)
      ElMessage.success('更新成功')
    } else {
      // 新增
      await axiosInstance.post('/blocks/', data)
      ElMessage.success('创建成功')
    }
    fetchBlockList()
  } catch (error) {
    console.error('保存磨块信息失败:', error)
    ElMessage.error('保存失败')
  }
}

// 编辑磨块
const handleEdit = (row: BlockFormData) => {
  // TODO: 实现编辑功能
  console.log('编辑磨块:', row)
}

// 查看磨块详情
const handleView = (row: BlockFormData) => {
  // TODO: 实现查看详情功能
  console.log('查看磨块:', row)
}

// 删除磨块
const handleDelete = async (row: BlockFormData) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个磨块吗？此操作不可恢复。',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await axiosInstance.delete(`/blocks/${row.id}/`)
    ElMessage.success('删除成功')
    fetchBlockList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除磨块失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 初始化
onMounted(() => {
  fetchBlockList()
})
</script>

<style scoped>
.block-info-view {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  font-size: 24px;
  color: var(--el-text-color-primary);
}

.search-bar {
  background-color: var(--el-bg-color);
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.block-table {
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

:deep(.el-form--inline .el-form-item) {
  margin-right: 0;
  margin-bottom: 10px;
}

@media (max-width: 768px) {
  .search-form {
    flex-direction: column;
  }
  
  .el-form-item {
    margin-right: 0;
    width: 100%;
  }
  
  .el-input,
  .el-select {
    width: 100%;
  }
}
</style> 