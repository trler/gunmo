<template>
  <div class="approved-review">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-check-circle"></i>
        已审核工艺
      </h1>
      <p class="page-description">查看已通过审核的工艺方案</p>
    </div>

    <el-card class="table-card">
      <el-table :data="approvedData" v-loading="loading" border>
        <el-table-column prop="processName" label="工艺名称" width="150" />
        <el-table-column prop="submitter" label="提交人" width="100" />
        <el-table-column prop="reviewer" label="审核人" width="100" />
        <el-table-column prop="approveTime" label="审核时间" width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag type="success">{{ row.status }}</el-tag>
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
const approvedData = ref([])

const loadData = async () => {
  loading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    approvedData.value = [
      {
        id: 1,
        processName: '标准抛光工艺',
        submitter: '王工程师',
        reviewer: '李主任',
        approveTime: '2024-01-12 16:30',
        status: '已批准'
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
.approved-review {
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
  color: #67c23a;
}

.page-description {
  color: #666;
  margin: 0;
  font-size: 14px;
}
</style> 