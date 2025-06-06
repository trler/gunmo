<template>
  <div class="quality-reports">
    <div class="page-header">
      <h1>质量报告</h1>
      <p>查看和管理质量检测报告</p>
    </div>

    <el-card>
      <template #header>
        <div class="card-header">
          <span>报告列表</span>
          <el-button type="primary" @click="generateReport">
            <el-icon><DocumentAdd /></el-icon>
            生成新报告
          </el-button>
        </div>
      </template>

      <div class="filter-section">
        <el-row :gutter="16">
          <el-col :span="6">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              @change="filterReports"
            />
          </el-col>
          <el-col :span="6">
            <el-select v-model="statusFilter" placeholder="选择状态" @change="filterReports">
              <el-option label="全部" value=""></el-option>
              <el-option label="待审核" value="pending"></el-option>
              <el-option label="已通过" value="approved"></el-option>
              <el-option label="已拒绝" value="rejected"></el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-input
              v-model="searchText"
              placeholder="搜索报告..."
              @input="filterReports"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-col>
        </el-row>
      </div>

      <el-table :data="filteredReports" style="width: 100%">
        <el-table-column prop="id" label="报告ID" width="100" />
        <el-table-column prop="title" label="报告标题" />
        <el-table-column prop="inspector" label="检测员" width="120" />
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag
              :type="getStatusType(scope.row.status)"
              size="small"
            >
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="viewReport(scope.row)">
              查看
            </el-button>
            <el-button size="small" type="primary" @click="downloadReport(scope.row)">
              下载
            </el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="deleteReport(scope.row)"
              v-if="scope.row.status === 'pending'"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="totalReports"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 报告详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="报告详情"
      width="80%"
      :before-close="handleClose"
    >
      <div v-if="selectedReport">
        <h3>{{ selectedReport.title }}</h3>
        <p><strong>检测员：</strong>{{ selectedReport.inspector }}</p>
        <p><strong>创建时间：</strong>{{ selectedReport.createTime }}</p>
        <p><strong>状态：</strong>{{ getStatusText(selectedReport.status) }}</p>
        
        <div class="report-content">
          <h4>检测结果</h4>
          <el-table :data="selectedReport.testResults" size="small">
            <el-table-column prop="item" label="检测项目" />
            <el-table-column prop="standard" label="标准值" />
            <el-table-column prop="actual" label="实际值" />
            <el-table-column prop="result" label="结果">
              <template #default="scope">
                <el-tag
                  :type="scope.row.result === '合格' ? 'success' : 'danger'"
                  size="small"
                >
                  {{ scope.row.result }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div class="report-conclusion">
          <h4>检测结论</h4>
          <p>{{ selectedReport.conclusion }}</p>
        </div>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="downloadReport(selectedReport)">
            下载报告
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { DocumentAdd, Search } from '@element-plus/icons-vue'

// 数据结构定义
interface TestResult {
  item: string
  standard: string
  actual: string
  result: string
}

interface QualityReport {
  id: string
  title: string
  inspector: string
  createTime: string
  status: 'pending' | 'approved' | 'rejected'
  testResults: TestResult[]
  conclusion: string
}

// 响应式数据
const reports = ref<QualityReport[]>([])
const filteredReports = ref<QualityReport[]>([])
const dateRange = ref<[Date, Date] | null>(null)
const statusFilter = ref('')
const searchText = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const totalReports = computed(() => filteredReports.value.length)

// 对话框相关
const dialogVisible = ref(false)
const selectedReport = ref<QualityReport | null>(null)

// 初始化模拟数据
const initializeData = () => {
  reports.value = [
    {
      id: 'QR001',
      title: '磨块表面质量检测报告',
      inspector: '张三',
      createTime: '2024-01-15 10:30:00',
      status: 'approved',
      testResults: [
        { item: '表面粗糙度', standard: 'Ra≤0.8μm', actual: 'Ra=0.6μm', result: '合格' },
        { item: '平行度', standard: '≤0.05mm', actual: '0.03mm', result: '合格' },
        { item: '垂直度', standard: '≤0.02mm', actual: '0.015mm', result: '合格' }
      ],
      conclusion: '该批磨块表面质量符合技术要求，可用于生产。'
    },
    {
      id: 'QR002',
      title: '工件精度检测报告',
      inspector: '李四',
      createTime: '2024-01-14 14:20:00',
      status: 'pending',
      testResults: [
        { item: '尺寸精度', standard: '±0.01mm', actual: '+0.008mm', result: '合格' },
        { item: '形状精度', standard: '≤0.005mm', actual: '0.004mm', result: '合格' },
        { item: '位置精度', standard: '≤0.02mm', actual: '0.018mm', result: '合格' }
      ],
      conclusion: '工件精度满足设计要求，质量良好。'
    },
    {
      id: 'QR003',
      title: '设备运行状态检测报告',
      inspector: '王五',
      createTime: '2024-01-13 09:15:00',
      status: 'rejected',
      testResults: [
        { item: '振动幅度', standard: '≤0.1mm', actual: '0.15mm', result: '不合格' },
        { item: '温度', standard: '≤60℃', actual: '65℃', result: '不合格' },
        { item: '噪音', standard: '≤80dB', actual: '75dB', result: '合格' }
      ],
      conclusion: '设备运行状态异常，需要维护检修。'
    }
  ]
  filteredReports.value = [...reports.value]
}

// 状态相关方法
const getStatusType = (status: string) => {
  switch (status) {
    case 'approved': return 'success'
    case 'rejected': return 'danger'
    case 'pending': return 'warning'
    default: return 'info'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'approved': return '已通过'
    case 'rejected': return '已拒绝'
    case 'pending': return '待审核'
    default: return '未知'
  }
}

// 过滤方法
const filterReports = () => {
  let filtered = [...reports.value]

  // 日期范围过滤
  if (dateRange.value) {
    const [start, end] = dateRange.value
    filtered = filtered.filter(report => {
      const reportDate = new Date(report.createTime)
      return reportDate >= start && reportDate <= end
    })
  }

  // 状态过滤
  if (statusFilter.value) {
    filtered = filtered.filter(report => report.status === statusFilter.value)
  }

  // 搜索过滤
  if (searchText.value) {
    const search = searchText.value.toLowerCase()
    filtered = filtered.filter(report =>
      report.title.toLowerCase().includes(search) ||
      report.inspector.toLowerCase().includes(search) ||
      report.id.toLowerCase().includes(search)
    )
  }

  filteredReports.value = filtered
  currentPage.value = 1
}

// 分页方法
const handleSizeChange = (val: number) => {
  pageSize.value = val
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}

// 操作方法
const generateReport = () => {
  ElMessage.info('生成新报告功能开发中...')
}

const viewReport = (report: QualityReport) => {
  selectedReport.value = report
  dialogVisible.value = true
}

const downloadReport = (report: QualityReport) => {
  ElMessage.success(`开始下载报告: ${report.title}`)
  // 这里可以实现实际的下载逻辑
}

const deleteReport = async (report: QualityReport) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除报告 "${report.title}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    const index = reports.value.findIndex(r => r.id === report.id)
    if (index > -1) {
      reports.value.splice(index, 1)
      filterReports()
      ElMessage.success('删除成功')
    }
  } catch {
    ElMessage.info('已取消删除')
  }
}

const handleClose = (done: () => void) => {
  selectedReport.value = null
  done()
}

// 生命周期
onMounted(() => {
  initializeData()
})
</script>

<style scoped>
.quality-reports {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #333;
}

.page-header p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-section {
  margin-bottom: 20px;
}

.pagination-wrapper {
  margin-top: 20px;
  text-align: center;
}

.report-content {
  margin: 20px 0;
}

.report-content h4,
.report-conclusion h4 {
  margin: 16px 0 8px 0;
  color: #333;
}

.report-conclusion {
  margin-top: 20px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style> 