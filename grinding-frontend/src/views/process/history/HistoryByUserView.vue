<template>
  <div class="history-by-user">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-user"></i>
        按用户查询
      </h1>
      <p class="page-description">按审核人员查询审核记录</p>
    </div>

    <!-- 用户筛选 -->
    <el-card class="filter-card" shadow="never">
      <el-form :model="filterForm" :inline="true" class="filter-form">
        <el-form-item label="审核人员">
          <el-select v-model="filterForm.reviewer" placeholder="选择审核人员" clearable @change="loadData">
            <el-option label="李主任" value="李主任" />
            <el-option label="张主任" value="张主任" />
            <el-option label="王主任" value="王主任" />
          </el-select>
        </el-form-item>
        <el-form-item label="提交人员">
          <el-select v-model="filterForm.submitter" placeholder="选择提交人员" clearable @change="loadData">
            <el-option label="张工程师" value="张工程师" />
            <el-option label="李工程师" value="李工程师" />
            <el-option label="王工程师" value="王工程师" />
            <el-option label="陈工程师" value="陈工程师" />
          </el-select>
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

    <!-- 统计概览 -->
    <div class="stats-overview">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-number">{{ totalReviews }}</div>
              <div class="stats-label">总审核数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-number">{{ approvedCount }}</div>
              <div class="stats-label">通过数量</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-number">{{ rejectedCount }}</div>
              <div class="stats-label">驳回数量</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <el-card class="table-card">
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
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const historyData = ref([])

const filterForm = ref({
  reviewer: '',
  submitter: '',
  result: ''
})

// 统计数据
const totalReviews = computed(() => historyData.value.length)
const approvedCount = computed(() => historyData.value.filter((item: any) => item.result === '通过').length)
const rejectedCount = computed(() => historyData.value.filter((item: any) => item.result === '驳回').length)

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

const resetFilter = () => {
  filterForm.value = {
    reviewer: '',
    submitter: '',
    result: ''
  }
  loadData()
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.history-by-user {
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
  color: #606266;
}

.page-description {
  color: #666;
  margin: 0;
  font-size: 14px;
}

.filter-card {
  margin-bottom: 24px;
}

.stats-overview {
  margin-bottom: 24px;
}

.stats-card {
  padding: 20px;
  text-align: center;
}

.stats-number {
  font-size: 32px;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 8px;
}

.stats-label {
  font-size: 14px;
  color: #666;
}
</style> 