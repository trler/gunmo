<template>
  <div class="history-by-date">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-calendar-alt"></i>
        按日期查询
      </h1>
      <p class="page-description">按时间范围查询审核记录</p>
    </div>

    <!-- 日期筛选 -->
    <el-card class="filter-card" shadow="never">
      <el-form :model="filterForm" :inline="true" class="filter-form">
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            @change="loadData"
          />
        </el-form-item>
        <el-form-item label="审核结果">
          <el-select v-model="filterForm.result" placeholder="选择结果" clearable @change="loadData">
            <el-option label="通过" value="approved" />
            <el-option label="驳回" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">
            <i class="fas fa-search"></i>
            查询
          </el-button>
          <el-button @click="resetFilter">
            <i class="fas fa-undo"></i>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <el-table :data="historyData" v-loading="loading" border>
        <el-table-column prop="processName" label="工艺名称" width="150" />
        <el-table-column prop="reviewDate" label="审核日期" width="120" />
        <el-table-column prop="reviewer" label="审核人" width="100" />
        <el-table-column prop="result" label="审核结果" width="100">
          <template #default="{ row }">
            <el-tag :type="row.result === '通过' ? 'success' : 'danger'">
              {{ row.result }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="comments" label="审核意见" min-width="200" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const historyData = ref([])

const filterForm = ref({
  dateRange: null,
  result: ''
})

const loadData = async () => {
  loading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    historyData.value = [
      {
        id: 1,
        processName: '标准抛光工艺',
        reviewDate: '2024-01-12',
        reviewer: '李主任',
        result: '通过',
        comments: '工艺方案合理，可以执行'
      }
    ]
  } finally {
    loading.value = false
  }
}

const resetFilter = () => {
  filterForm.value = {
    dateRange: null,
    result: ''
  }
  loadData()
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.history-by-date {
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
  color: #e6a23c;
}

.page-description {
  color: #666;
  margin: 0;
  font-size: 14px;
}

.filter-card {
  margin-bottom: 24px;
}
</style> 