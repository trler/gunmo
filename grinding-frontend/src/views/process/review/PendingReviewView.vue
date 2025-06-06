<template>
  <div class="pending-review">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-clock"></i>
        待审核工艺
      </h1>
      <p class="page-description">管理待审核的工艺方案</p>
    </div>

    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <span>待审核工艺列表</span>
          <el-button type="primary" @click="batchReview">
            <i class="fas fa-check-double"></i>
            批量审核
          </el-button>
        </div>
      </template>
      <el-table :data="pendingData" v-loading="loading" border @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="processName" label="工艺名称" width="150" />
        <el-table-column prop="submitter" label="提交人" width="100" />
        <el-table-column prop="submitTime" label="提交时间" width="150" />
        <el-table-column prop="processType" label="工艺类型" width="120" />
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="{ row }">
            <el-tag :type="row.priority === '高' ? 'danger' : row.priority === '中' ? 'warning' : 'info'">
              {{ row.priority }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewDetails(row)">查看详情</el-button>
            <el-button type="success" link @click="approve(row)">批准</el-button>
            <el-button type="danger" link @click="reject(row)">驳回</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const pendingData = ref([])
const selectedRows = ref([])

const loadData = async () => {
  loading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    pendingData.value = [
      {
        id: 1,
        processName: '表面光整工艺方案A',
        submitter: '张工程师',
        submitTime: '2024-01-15 10:30',
        processType: '表面处理',
        priority: '高'
      },
      {
        id: 2,
        processName: '精密去毛刺方案B',
        submitter: '李工程师',
        submitTime: '2024-01-14 14:20',
        processType: '精密加工',
        priority: '中'
      }
    ]
  } catch (error) {
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const handleSelectionChange = (selection: any[]) => {
  selectedRows.value = selection
}

const viewDetails = (row: any) => {
  ElMessage.info(`查看工艺详情: ${row.processName}`)
}

const approve = (row: any) => {
  ElMessage.success(`已批准工艺: ${row.processName}`)
}

const reject = (row: any) => {
  ElMessage.warning(`已驳回工艺: ${row.processName}`)
}

const batchReview = () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请选择要审核的工艺')
    return
  }
  ElMessage.success(`批量审核 ${selectedRows.value.length} 个工艺`)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.pending-review {
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

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 