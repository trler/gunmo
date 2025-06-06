<template>
  <div class="chemical-management">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>化学剂管理</span>
          <el-button type="primary" @click="handleAdd">新增化学剂</el-button>
        </div>
      </template>

      <!-- 搜索表单 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="化学剂编号">
          <el-input v-model="searchForm.code" placeholder="请输入编号" clearable />
        </el-form-item>
        <el-form-item label="化学剂名称">
          <el-input v-model="searchForm.name" placeholder="请输入名称" clearable />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="searchForm.type" placeholder="请选择类型" clearable>
            <el-option
              v-for="type in chemicalTypes"
              :key="type.value"
              :label="type.label"
              :value="type.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="生产厂家">
          <el-input v-model="searchForm.manufacturer" placeholder="请输入厂家" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 数据表格 -->
      <el-table
        v-loading="loading"
        :data="chemicalList"
        style="width: 100%"
        border
      >
        <el-table-column prop="code" label="化学剂编号" width="120" />
        <el-table-column prop="name" label="化学剂名称" width="150" />
        <el-table-column prop="type_display" label="类型" width="100" />
        <el-table-column prop="manufacturer" label="生产厂家" width="150" />
        <el-table-column prop="components" label="主要成分" show-overflow-tooltip />
        <el-table-column prop="ph_range" label="PH值范围" width="100" />
        <el-table-column prop="density" label="密度(g/cm³)" width="100" />
        <el-table-column prop="flash_point" label="闪点(℃)" width="100" />
        <el-table-column prop="safety_level_display" label="安全等级" width="100">
          <template #default="{ row }">
            <el-tag :type="getSafetyLevelType(row.safety_level)">
              {{ row.safety_level_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="expiry_date" label="有效期" width="120" />
        <el-table-column label="文档" width="150">
          <template #default="{ row }">
            <el-button
              v-if="row.msds_file_url"
              link
              type="primary"
              @click="handleDownload(row.msds_file_url, 'MSDS')"
            >
              MSDS
            </el-button>
            <el-button
              v-if="row.formula_file_url"
              link
              type="primary"
              @click="handleDownload(row.formula_file_url, '配方')"
            >
              配方
            </el-button>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
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

    <!-- 化学剂表单对话框 -->
    <chemical-form-dialog
      v-model="dialogVisible"
      :chemical="currentChemical"
      @success="handleSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useChemicalStore } from '@/stores/chemical'
import type { Chemical, ChemicalType } from '@/stores/chemical'
import ChemicalFormDialog from './components/ChemicalFormDialog.vue'

const chemicalStore = useChemicalStore()
const loading = ref(false)
const dialogVisible = ref(false)
const currentChemical = ref<Chemical | null>(null)

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 搜索表单
const searchForm = reactive({
  code: '',
  name: '',
  type: '' as ChemicalType | '',
  manufacturer: ''
})

// 化学剂类型选项
const chemicalTypes = [
  { value: 'cutting_fluid', label: '切削液' },
  { value: 'cleaning_agent', label: '清洗剂' },
  { value: 'rust_preventive', label: '防锈剂' },
  { value: 'lubricant', label: '润滑剂' },
  { value: 'passivator', label: '钝化剂' }
]

// 获取化学剂列表
const chemicalList = ref<Chemical[]>([])
const fetchChemicalList = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      ...searchForm
    }
    const response = await chemicalStore.getChemicalList(params)
    chemicalList.value = response.results
    total.value = response.count
  } catch (error) {
    console.error('获取化学剂列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索和重置
const handleSearch = () => {
  currentPage.value = 1
  fetchChemicalList()
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
  fetchChemicalList()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchChemicalList()
}

// 新增化学剂
const handleAdd = () => {
  currentChemical.value = null
  dialogVisible.value = true
}

// 编辑化学剂
const handleEdit = (row: Chemical) => {
  currentChemical.value = row
  dialogVisible.value = true
}

// 删除化学剂
const handleDelete = async (row: Chemical) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除化学剂"${row.name}"吗？`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await chemicalStore.deleteChemical(row.id)
    ElMessage.success('删除成功')
    fetchChemicalList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除化学剂失败:', error)
    }
  }
}

// 下载文件
const handleDownload = (url: string, type: string) => {
  window.open(url, '_blank')
}

// 获取安全等级标签类型
const getSafetyLevelType = (level: string) => {
  switch (level) {
    case 'low':
      return 'success'
    case 'medium':
      return 'warning'
    case 'high':
      return 'danger'
    default:
      return 'info'
  }
}

// 表单提交成功处理
const handleSuccess = () => {
  dialogVisible.value = false
  fetchChemicalList()
}

// 初始化
onMounted(() => {
  fetchChemicalList()
})
</script>

<style scoped>
.chemical-management {
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
</style> 