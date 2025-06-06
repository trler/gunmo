<template>
  <div class="system-logs">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>系统日志管理</span>
          <div class="header-operations">
            <el-button type="danger" @click="handleClearLogs">
              <el-icon><Delete /></el-icon>清空日志
            </el-button>
            <el-button type="primary" @click="handleExport">
              <el-icon><Download /></el-icon>导出日志
            </el-button>
          </div>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="操作模块">
            <el-input v-model="searchForm.module" placeholder="请输入操作模块" clearable />
          </el-form-item>
          <el-form-item label="操作类型">
            <el-select v-model="searchForm.type" placeholder="请选择操作类型" clearable>
              <el-option label="查询" value="query" />
              <el-option label="新增" value="create" />
              <el-option label="修改" value="update" />
              <el-option label="删除" value="delete" />
              <el-option label="导出" value="export" />
              <el-option label="导入" value="import" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          <el-form-item label="操作状态">
            <el-select v-model="searchForm.status" placeholder="请选择操作状态" clearable>
              <el-option label="成功" value="success" />
              <el-option label="失败" value="error" />
            </el-select>
          </el-form-item>
          <el-form-item label="操作时间">
            <el-date-picker
              v-model="searchForm.timeRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 日志列表 -->
      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="日志ID" width="80" />
        <el-table-column prop="module" label="操作模块" width="120" />
        <el-table-column prop="type" label="操作类型" width="100">
          <template #default="scope">
            <el-tag :type="getOperationTypeTag(scope.row.type)">
              {{ getOperationTypeLabel(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="操作描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="operator" label="操作人" width="120" />
        <el-table-column prop="ip" label="操作IP" width="120" />
        <el-table-column prop="status" label="操作状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'">
              {{ scope.row.status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="操作时间" width="180" />
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="scope">
            <el-button type="primary" link @click="handleViewDetail(scope.row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 日志详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="日志详情"
      width="800px"
    >
      <el-descriptions :column="2" border>
        <el-descriptions-item label="日志ID">{{ currentLog?.id }}</el-descriptions-item>
        <el-descriptions-item label="操作模块">{{ currentLog?.module }}</el-descriptions-item>
        <el-descriptions-item label="操作类型">
          <el-tag :type="getOperationTypeTag(currentLog?.type)">
            {{ getOperationTypeLabel(currentLog?.type) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="操作状态">
          <el-tag :type="currentLog?.status === 'success' ? 'success' : 'danger'">
            {{ currentLog?.status === 'success' ? '成功' : '失败' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="操作人">{{ currentLog?.operator }}</el-descriptions-item>
        <el-descriptions-item label="操作IP">{{ currentLog?.ip }}</el-descriptions-item>
        <el-descriptions-item label="操作时间">{{ currentLog?.createTime }}</el-descriptions-item>
        <el-descriptions-item label="请求方法">{{ currentLog?.method }}</el-descriptions-item>
        <el-descriptions-item label="请求URL" :span="2">{{ currentLog?.url }}</el-descriptions-item>
        <el-descriptions-item label="操作描述" :span="2">{{ currentLog?.description }}</el-descriptions-item>
        <el-descriptions-item label="请求参数" :span="2">
          <pre class="log-content">{{ formatJson(currentLog?.requestParams) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="响应结果" :span="2">
          <pre class="log-content">{{ formatJson(currentLog?.responseResult) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="错误信息" :span="2" v-if="currentLog?.status === 'error'">
          <pre class="log-content error">{{ currentLog?.errorMessage }}</pre>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete, Download } from '@element-plus/icons-vue'

// 搜索表单
const searchForm = reactive({
  module: '',
  type: '',
  status: '',
  timeRange: []
})

// 表格数据
const loading = ref(false)
const tableData = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 详情对话框
const detailDialogVisible = ref(false)
const currentLog = ref<any>(null)

// 获取操作类型标签
const getOperationTypeTag = (type: string): 'success' | 'primary' | 'warning' | 'info' | 'danger' => {
  const typeMap: Record<string, 'success' | 'primary' | 'warning' | 'info' | 'danger'> = {
    query: 'info',
    create: 'success',
    update: 'warning',
    delete: 'danger',
    export: 'primary',
    import: 'primary',
    other: 'info'
  }
  return typeMap[type] || 'info'
}

// 获取操作类型标签文本
const getOperationTypeLabel = (type: string) => {
  const typeMap: Record<string, string> = {
    query: '查询',
    create: '新增',
    update: '修改',
    delete: '删除',
    export: '导出',
    import: '导入',
    other: '其他'
  }
  return typeMap[type] || '其他'
}

// 格式化 JSON
const formatJson = (json: any) => {
  if (!json) return ''
  try {
    if (typeof json === 'string') {
      json = JSON.parse(json)
    }
    return JSON.stringify(json, null, 2)
  } catch (e) {
    return json
  }
}

// 获取日志列表
const getList = async () => {
  loading.value = true
  try {
    // TODO: 调用后端API获取数据
    // const res = await getLogList({
    //   page: currentPage.value,
    //   pageSize: pageSize.value,
    //   ...searchForm,
    //   startTime: searchForm.timeRange?.[0],
    //   endTime: searchForm.timeRange?.[1]
    // })
    // tableData.value = res.data.list
    // total.value = res.data.total

    // 模拟数据
    tableData.value = [
      {
        id: '1',
        module: '系统管理',
        type: 'query',
        description: '查询系统参数列表',
        operator: 'admin',
        ip: '127.0.0.1',
        status: 'success',
        createTime: '2024-01-01 12:00:00',
        method: 'GET',
        url: '/api/system/params',
        requestParams: { page: 1, pageSize: 10 },
        responseResult: { code: 200, message: 'success', data: [] }
      },
      {
        id: '2',
        module: '用户管理',
        type: 'create',
        description: '新增用户',
        operator: 'admin',
        ip: '127.0.0.1',
        status: 'error',
        createTime: '2024-01-01 12:00:00',
        method: 'POST',
        url: '/api/system/users',
        requestParams: { username: 'test', name: '测试用户' },
        responseResult: { code: 500, message: 'error' },
        errorMessage: '用户名已存在'
      }
    ]
    total.value = 2
  } catch (error) {
    console.error('获取日志列表失败:', error)
    ElMessage.error('获取日志列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  getList()
}

// 重置搜索
const resetSearch = () => {
  searchForm.module = ''
  searchForm.type = ''
  searchForm.status = ''
  searchForm.timeRange = []
  handleSearch()
}

// 分页
const handleSizeChange = (val: number) => {
  pageSize.value = val
  getList()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  getList()
}

// 查看详情
const handleViewDetail = (row: any) => {
  currentLog.value = row
  detailDialogVisible.value = true
}

// 清空日志
const handleClearLogs = () => {
  ElMessageBox.confirm(
    '确认清空所有日志吗？此操作不可恢复！',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      // TODO: 调用后端API清空日志
      // await clearLogs()
      ElMessage.success('清空成功')
      getList()
    } catch (error) {
      console.error('清空日志失败:', error)
      ElMessage.error('清空日志失败')
    }
  })
}

// 导出日志
const handleExport = async () => {
  try {
    // TODO: 调用后端API导出日志
    // const res = await exportLogs({
    //   ...searchForm,
    //   startTime: searchForm.timeRange?.[0],
    //   endTime: searchForm.timeRange?.[1]
    // })
    // const blob = new Blob([res.data], { type: 'application/vnd.ms-excel' })
    // const url = window.URL.createObjectURL(blob)
    // const link = document.createElement('a')
    // link.href = url
    // link.download = `系统日志_${new Date().getTime()}.xlsx`
    // link.click()
    // window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出日志失败:', error)
    ElMessage.error('导出日志失败')
  }
}

onMounted(() => {
  getList()
})
</script>

<style scoped>
.system-logs {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-operations {
  display: flex;
  gap: 10px;
}

.search-bar {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.log-content {
  margin: 0;
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-family: monospace;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 200px;
  overflow-y: auto;
}

.log-content.error {
  color: #f56c6c;
  background-color: #fef0f0;
}
</style> 