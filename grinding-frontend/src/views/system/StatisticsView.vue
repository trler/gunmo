<template>
  <div class="statistics-container">
    <!-- 日期范围选择器 -->
    <div class="date-range-picker">
      <el-date-picker
        v-model="dateRangeValue"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        :shortcuts="dateShortcuts"
        @change="handleDateRangeChange"
      />
      <el-button type="primary" @click="handleExport">
        <el-icon><Download /></el-icon>
        导出数据
      </el-button>
    </div>

    <!-- 概览卡片 -->
    <el-row :gutter="20" class="overview-cards">
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>用户总数</span>
              <el-tag :type="overviewData.userGrowth >= 0 ? 'success' : 'danger'" size="small">
                {{ overviewData.userGrowth >= 0 ? '+' : '' }}{{ overviewData.userGrowth }}%
              </el-tag>
            </div>
          </template>
          <div class="card-value">{{ overviewData.totalUsers }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>设备总数</span>
              <el-tag :type="overviewData.equipmentGrowth >= 0 ? 'success' : 'danger'" size="small">
                {{ overviewData.equipmentGrowth >= 0 ? '+' : '' }}{{ overviewData.equipmentGrowth }}%
              </el-tag>
            </div>
          </template>
          <div class="card-value">{{ overviewData.totalEquipment }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>工艺总数</span>
              <el-tag :type="overviewData.processGrowth >= 0 ? 'success' : 'danger'" size="small">
                {{ overviewData.processGrowth >= 0 ? '+' : '' }}{{ overviewData.processGrowth }}%
              </el-tag>
            </div>
          </template>
          <div class="card-value">{{ overviewData.totalProcesses }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>质量合格率</span>
              <el-tag :type="overviewData.qualityGrowth >= 0 ? 'success' : 'danger'" size="small">
                {{ overviewData.qualityGrowth >= 0 ? '+' : '' }}{{ overviewData.qualityGrowth }}%
              </el-tag>
            </div>
          </template>
          <div class="card-value">{{ overviewData.qualityRate }}%</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-section">
      <!-- 用户趋势图 -->
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>用户趋势</span>
              <el-radio-group v-model="userChartType" size="small">
                <el-radio-button label="week">周</el-radio-button>
                <el-radio-button label="month">月</el-radio-button>
                <el-radio-button label="year">年</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="userChartOption" autoresize />
          </div>
        </el-card>
      </el-col>

      <!-- 设备状态图 -->
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>设备状态</span>
              <el-radio-group v-model="equipmentChartType" size="small">
                <el-radio-button label="status">状态分布</el-radio-button>
                <el-radio-button label="efficiency">效率分析</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="equipmentChartOption" autoresize />
          </div>
        </el-card>
      </el-col>

      <!-- 质量趋势图 -->
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>质量趋势</span>
              <el-radio-group v-model="qualityChartMetric" size="small">
                <el-radio-button label="pass_rate">合格率</el-radio-button>
                <el-radio-button label="defect_rate">缺陷率</el-radio-button>
                <el-radio-button label="rework_rate">返工率</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="qualityChartOption" autoresize />
          </div>
        </el-card>
      </el-col>

      <!-- 工艺分析图 -->
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>工艺分析</span>
              <el-radio-group v-model="processChartMetric" size="small">
                <el-radio-button label="efficiency">效率</el-radio-button>
                <el-radio-button label="quality">质量</el-radio-button>
                <el-radio-button label="cost">成本</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="processChartOption" autoresize />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 数据表格 -->
    <el-card shadow="hover" class="table-section">
      <template #header>
        <div class="card-header">
          <span>详细数据</span>
        </div>
      </template>
      <el-table
        v-loading="loading"
        :data="tableData"
        style="width: 100%"
        border
      >
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="newUsers" label="新增用户" width="100" />
        <el-table-column prop="activeUsers" label="活跃用户" width="100" />
        <el-table-column prop="onlineEquipment" label="在线设备" width="100" />
        <el-table-column prop="runningEquipment" label="运行设备" width="100" />
        <el-table-column prop="processCount" label="工艺数量" width="100" />
        <el-table-column prop="qualityRate" label="质量合格率" width="120">
          <template #default="{ row }">
            {{ row.qualityRate }}%
          </template>
        </el-table-column>
        <el-table-column prop="avgEfficiency" label="平均效率" width="120">
          <template #default="{ row }">
            {{ row.avgEfficiency }}%
          </template>
        </el-table-column>
        <el-table-column prop="remarks" label="备注" />
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useStatisticsStore } from '@/stores/statistics'
import { ElMessage } from 'element-plus'
import { Download } from '@element-plus/icons-vue'
import type { DateRange, UserChartData, EquipmentChartData, ProcessChartData } from '@/types/statistics'

// 图表相关导入
import VChart from 'vue-echarts'
import type { ComposeOption } from 'echarts/core'
import type { LineSeriesOption, BarSeriesOption, PieSeriesOption } from 'echarts/charts'
import type { TitleComponentOption, TooltipComponentOption, GridComponentOption, LegendComponentOption } from 'echarts/components'

type ECOption = ComposeOption<
  | LineSeriesOption
  | BarSeriesOption
  | PieSeriesOption
  | TitleComponentOption
  | TooltipComponentOption
  | GridComponentOption
  | LegendComponentOption
>

const statisticsStore = useStatisticsStore()
const loading = ref(false)

// 修改 dateRange 的类型为 [Date, Date] | null
const dateRangeValue = ref<[Date, Date] | null>([
  new Date(new Date().setDate(new Date().getDate() - 7)),
  new Date()
])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const tableData = ref([])

// 图表类型选择
const userChartType = ref<'week' | 'month' | 'year'>('week')
const equipmentChartType = ref<'status' | 'efficiency'>('status')
const qualityChartMetric = ref<'pass_rate' | 'defect_rate' | 'rework_rate'>('pass_rate')
const processChartMetric = ref<'efficiency' | 'quality' | 'cost'>('efficiency')

// 日期快捷选项
const dateShortcuts = [
  {
    text: '最近一周',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    }
  },
  {
    text: '最近一月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
      return [start, end]
    }
  },
  {
    text: '最近三月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
      return [start, end]
    }
  }
]

// 数据状态
const overviewData = ref({
  totalUsers: 0,
  userGrowth: 0,
  totalEquipment: 0,
  equipmentGrowth: 0,
  totalProcesses: 0,
  processGrowth: 0,
  qualityRate: 0,
  qualityGrowth: 0
})

const userChartData = ref<UserChartData>({
  dates: [],
  newUsers: [],
  activeUsers: []
})

const equipmentChartData = ref<EquipmentChartData>({
  status: [],
  efficiency: []
})

const processChartData = ref<ProcessChartData>({
  processes: [],
  values: []
})

// 图表配置
const userChartOption = computed<ECOption>(() => ({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['新增用户', '活跃用户']
  },
  xAxis: {
    type: 'category',
    data: userChartData.value.dates
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '新增用户',
      type: 'line',
      data: userChartData.value.newUsers
    },
    {
      name: '活跃用户',
      type: 'line',
      data: userChartData.value.activeUsers
    }
  ]
}))

const equipmentChartOption = computed<ECOption>(() => {
  if (equipmentChartType.value === 'status') {
    return {
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          type: 'pie',
          radius: '50%',
          data: equipmentChartData.value.status,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    }
  } else {
    return {
      tooltip: {
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        data: equipmentChartData.value.efficiency.map(item => item.name)
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '{value}%'
        }
      },
      series: [
        {
          type: 'bar',
          data: equipmentChartData.value.efficiency.map(item => item.value)
        }
      ]
    }
  }
})

const qualityChartOption = computed<ECOption>(() => ({
  tooltip: {
    trigger: 'axis'
  },
  xAxis: {
    type: 'category',
    data: processChartData.value.processes
  },
  yAxis: {
    type: 'value',
    axisLabel: {
      formatter: '{value}%'
    }
  },
  series: [
    {
      type: 'line',
      data: processChartData.value.values
    }
  ]
}))

const processChartOption = computed<ECOption>(() => ({
  tooltip: {
    trigger: 'axis'
  },
  xAxis: {
    type: 'category',
    data: processChartData.value.processes
  },
  yAxis: {
    type: 'value',
    axisLabel: {
      formatter: '{value}%'
    }
  },
  series: [
    {
      type: 'bar',
      data: processChartData.value.values
    }
  ]
}))

// 处理日期范围变化
const handleDateRangeChange = (val: [Date, Date] | null) => {
  if (val) {
    const [start, end] = val
    fetchData({ start, end })
  }
}

// 获取数据
const fetchData = async (range: DateRange) => {
  try {
    loading.value = true
    
    // 获取概览数据
    const overview = await statisticsStore.fetchOverview(range)
    overviewData.value = overview
    
    // 获取表格数据
    const tableResponse = await statisticsStore.fetchTableData({
      page: currentPage.value,
      page_size: pageSize.value,
      date_range: range
    })
    tableData.value = tableResponse.results
    total.value = tableResponse.count
    
    // 获取图表数据
    const [userData, equipmentData, processData] = await Promise.all([
      statisticsStore.fetchUserChartData(userChartType.value, range),
      statisticsStore.fetchEquipmentChartData(equipmentChartType.value, range),
      statisticsStore.fetchProcessChartData(processChartMetric.value, range)
    ])
    
    userChartData.value = userData
    equipmentChartData.value = {
      status: equipmentData.status || [],
      efficiency: equipmentData.efficiency || []
    }
    processChartData.value = processData
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
  } finally {
    loading.value = false
  }
}

// 导出数据
const handleExport = async () => {
  try {
    const dateRange = dateRangeValue.value ? {
      start: dateRangeValue.value[0],
      end: dateRangeValue.value[1]
    } : null
    const blob = await statisticsStore.exportStatistics(dateRange)
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `统计数据_${new Date().toISOString().split('T')[0]}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

// 事件处理
const handleSizeChange = (val: number) => {
  pageSize.value = val
  if (dateRangeValue.value) {
    const [start, end] = dateRangeValue.value
    fetchData({ start, end })
  }
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  if (dateRangeValue.value) {
    const [start, end] = dateRangeValue.value
    fetchData({ start, end })
  }
}

// 监听图表类型变化
watch([userChartType, equipmentChartType, qualityChartMetric, processChartMetric], () => {
  if (dateRangeValue.value) {
    const [start, end] = dateRangeValue.value
    fetchData({ start, end })
  }
})

// 初始化数据
onMounted(() => {
  if (dateRangeValue.value) {
    const [start, end] = dateRangeValue.value
    fetchData({ start, end })
  }
})
</script>

<style scoped>
.statistics-container {
  padding: 20px;
}

.date-range-picker {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.overview-cards {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-value {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  margin-top: 10px;
}

.chart-section {
  margin-bottom: 20px;
}

.chart-container {
  height: 300px;
}

.table-section {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 