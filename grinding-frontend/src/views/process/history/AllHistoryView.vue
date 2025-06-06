<template>
  <div class="all-history">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-history"></i>
        全部审核记录
      </h1>
      <p class="page-description">查看所有工艺审核的历史记录</p>
    </div>

    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <span>审核历史记录</span>
          <el-button type="primary" @click="exportRecords">
            <i class="fas fa-download"></i>
            导出记录
          </el-button>
        </div>
      </template>
      <el-table :data="historyData" v-loading="loading" border>
        <el-table-column prop="processName" label="工艺名称" width="150" />
        <el-table-column prop="submitter" label="提交人" width="100" />
        <el-table-column prop="reviewer" label="审核人" width="100" />
        <el-table-column prop="reviewTime" label="审核时间" width="150" />
        <el-table-column prop="result" label="审核结果" width="100">
          <template #default="{ row }">
            <el-tag :type="row.result === '通过' ? 'success' : 'danger'">
              {{ row.result }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="comments" label="审核意见" min-width="200" />
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
const historyData = ref([])

const loadData = async () => {
  loading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    historyData.value = [
      {
        id: 1,
        processName: '标准抛光工艺',
        submitter: '王工程师',
        reviewer: '李主任',
        reviewTime: '2024-01-12 16:30',
        result: '通过',
        comments: '工艺方案合理，可以执行'
      },
      {
        id: 2,
        processName: '试验性工艺方案',
        submitter: '陈工程师',
        reviewer: '张主任',
        reviewTime: '2024-01-10 14:30',
        result: '驳回',
        comments: '工艺参数不符合安全标准，需要重新设计'
      }
    ]
  } finally {
    loading.value = false
  }
}

const viewDetails = (row: any) => {
  ElMessage.info(`查看审核详情: ${row.processName}`)
}

const exportRecords = () => {
  ElMessage.success('导出功能开发中')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.all-history {
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
  color: #909399;
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