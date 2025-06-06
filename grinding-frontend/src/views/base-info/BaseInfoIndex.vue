<template>
  <div class="base-info-container">
    <div class="page-header">
      <h2>基础信息库</h2>
      <p>企业基础信息管理系统</p>
    </div>
    
    <div class="info-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="info-card" @click="navigateTo('companies')">
            <div class="card-content">
              <div class="card-icon">
                <el-icon size="40">
                  <Building />
                </el-icon>
              </div>
              <div class="card-info">
                <h3>企业信息</h3>
                <p>企业基本信息管理</p>
                <div class="count">{{ statistics.companies || 0 }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card class="info-card" @click="navigateTo('departments')">
            <div class="card-content">
              <div class="card-icon">
                <el-icon size="40">
                  <OfficeBuilding />
                </el-icon>
              </div>
              <div class="card-info">
                <h3>部门信息</h3>
                <p>部门组织架构管理</p>
                <div class="count">{{ statistics.departments || 0 }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card class="info-card" @click="navigateTo('personnel')">
            <div class="card-content">
              <div class="card-icon">
                <el-icon size="40">
                  <Avatar />
                </el-icon>
              </div>
              <div class="card-info">
                <h3>人员信息</h3>
                <p>员工档案信息管理</p>
                <div class="count">{{ statistics.personnel || 0 }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card class="info-card" @click="navigateTo('standards')">
            <div class="card-content">
              <div class="card-icon">
                <el-icon size="40">
                  <Document />
                </el-icon>
              </div>
              <div class="card-info">
                <h3>标准规范</h3>
                <p>技术标准文档管理</p>
                <div class="count">{{ statistics.standards || 0 }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <div class="charts-section">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <template #header>
              <h3>企业类型分布</h3>
            </template>
            <div id="company-type-chart" style="height: 300px;"></div>
          </el-card>
        </el-col>
        
        <el-col :span="12">
          <el-card>
            <template #header>
              <h3>人员学历分布</h3>
            </template>
            <div id="education-chart" style="height: 300px;"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <div class="recent-section">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <template #header>
              <div class="card-header">
                <h3>最近添加的企业</h3>
                <el-button type="text" @click="navigateTo('companies')">查看全部</el-button>
              </div>
            </template>
            <div class="recent-list">
              <div v-for="company in recentCompanies" :key="company.id" class="recent-item">
                <div class="item-info">
                  <strong>{{ company.name }}</strong>
                  <span class="item-type">{{ company.company_type_display }}</span>
                </div>
                <div class="item-time">{{ formatDate(company.created_at) }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="12">
          <el-card>
            <template #header>
              <div class="card-header">
                <h3>最新标准规范</h3>
                <el-button type="text" @click="navigateTo('standards')">查看全部</el-button>
              </div>
            </template>
            <div class="recent-list">
              <div v-for="standard in recentStandards" :key="standard.id" class="recent-item">
                <div class="item-info">
                  <strong>{{ standard.standard_code }}</strong>
                  <span class="item-desc">{{ standard.title }}</span>
                </div>
                <div class="item-time">{{ formatDate(standard.publish_date) }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Building, OfficeBuilding, Avatar, Document } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { baseInfoApi } from '@/api/baseInfo'

const router = useRouter()

const statistics = ref({
  companies: 0,
  departments: 0,
  personnel: 0,
  standards: 0
})

const recentCompanies = ref([])
const recentStandards = ref([])

const navigateTo = (path) => {
  router.push(`/base-info/${path}`)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const loadStatistics = async () => {
  try {
    const [companyStats, departmentRes, personnelStats, standardStats] = await Promise.all([
      baseInfoApi.getCompanyStatistics(),
      baseInfoApi.getDepartments(),
      baseInfoApi.getPersonnelStatistics(),
      baseInfoApi.getStandardStatistics()
    ])
    
    statistics.value = {
      companies: companyStats.total,
      departments: departmentRes.count,
      personnel: personnelStats.total,
      standards: standardStats.total
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

const loadRecentData = async () => {
  try {
    const [companies, standards] = await Promise.all([
      baseInfoApi.getCompanies({ page: 1, page_size: 5 }),
      baseInfoApi.getStandards({ page: 1, page_size: 5 })
    ])
    
    recentCompanies.value = companies.results
    recentStandards.value = standards.results
  } catch (error) {
    console.error('获取最近数据失败:', error)
  }
}

const initCharts = async () => {
  try {
    const [companyStats, personnelStats] = await Promise.all([
      baseInfoApi.getCompanyStatistics(),
      baseInfoApi.getPersonnelStatistics()
    ])
    
    // 企业类型图表
    const companyChart = echarts.init(document.getElementById('company-type-chart'))
    const companyData = Object.entries(companyStats.type_stats || {}).map(([key, value]) => ({
      name: key,
      value
    }))
    
    companyChart.setOption({
      tooltip: {
        trigger: 'item'
      },
      series: [{
        type: 'pie',
        radius: '60%',
        data: companyData,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }]
    })
    
    // 人员学历图表
    const educationChart = echarts.init(document.getElementById('education-chart'))
    const educationData = Object.entries(personnelStats.education_stats || {}).map(([key, value]) => ({
      name: key,
      value
    }))
    
    educationChart.setOption({
      tooltip: {
        trigger: 'item'
      },
      series: [{
        type: 'pie',
        radius: '60%',
        data: educationData,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }]
    })
    
  } catch (error) {
    console.error('初始化图表失败:', error)
  }
}

onMounted(async () => {
  await loadStatistics()
  await loadRecentData()
  setTimeout(initCharts, 100) // 确保DOM已渲染
})
</script>

<style scoped>
.base-info-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h2 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 28px;
  font-weight: 600;
}

.page-header p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.info-cards {
  margin-bottom: 30px;
}

.info-card {
  cursor: pointer;
  transition: all 0.3s ease;
  height: 120px;
}

.info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.card-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.card-icon {
  margin-right: 20px;
  color: #409EFF;
}

.card-info h3 {
  margin: 0 0 5px 0;
  font-size: 18px;
  color: #303133;
}

.card-info p {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #909399;
}

.count {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.charts-section {
  margin-bottom: 30px;
}

.recent-section {
  margin-bottom: 30px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.recent-list {
  max-height: 300px;
  overflow-y: auto;
}

.recent-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.recent-item:last-child {
  border-bottom: none;
}

.item-info {
  flex: 1;
}

.item-info strong {
  display: block;
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
}

.item-type,
.item-desc {
  font-size: 12px;
  color: #909399;
}

.item-time {
  font-size: 12px;
  color: #C0C4CC;
}
</style> 