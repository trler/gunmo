<template>
  <div class="rejected-review">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-times-circle"></i>
        驳回工艺
      </h1>
      <p class="page-description">查看被驳回的工艺方案及驳回原因</p>
    </div>

    <el-card class="table-card">
      <el-table :data="rejectedData" v-loading="loading" border>
        <el-table-column prop="processName" label="工艺名称" width="150" />
        <el-table-column prop="submitter" label="提交人" width="100" />
        <el-table-column prop="reviewer" label="审核人" width="100" />
        <el-table-column prop="rejectTime" label="驳回时间" width="150" />
        <el-table-column prop="rejectReason" label="驳回原因" min-width="200" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag type="danger">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewDetails(row)">查看详情</el-button>
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
const rejectedData = ref([])

const loadData = async () => {
  loading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    rejectedData.value = [
      {
        id: 1,
        processName: '试验性工艺方案',
        submitter: '陈工程师',
        reviewer: '张主任',
        rejectTime: '2024-01-10 14:30',
        rejectReason: '工艺参数不符合安全标准，需要重新设计',
        status: '已驳回'
      }
    ]
  } finally {
    loading.value = false
  }
}

const viewDetails = (row: any) => {
  ElMessage.info(`查看工艺详情: ${row.processName}`)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.rejected-review {
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
  color: #f56c6c;
}

.page-description {
  color: #666;
  margin: 0;
  font-size: 14px;
}
</style> 