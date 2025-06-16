<template>
  <div class="weight-calculation-view">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-calculator"></i>
        计算特征权重
      </h1>
      <div class="header-actions">
        <el-button type="primary" icon="Download" @click="exportWeights">导出权重</el-button>
        <el-button icon="Refresh" @click="recalculateWeights">重新计算</el-button>
      </div>
    </div>

    <!-- 步骤导航 -->
    <div class="steps-navigation">
      <el-steps :active="currentStep" finish-status="success" align-center>
        <el-step title="输入新案例" description="完成案例特征录入" />
        <el-step title="设置特征值" description="配置特征参数" />
        <el-step title="计算特征权重" description="基于AHP计算权重" />
        <el-step title="案例匹配" description="智能匹配推荐" />
      </el-steps>
    </div>

    <!-- 权重计算结果 -->
    <div class="weight-results-container">
      <div class="results-header">
        <h2>特征权重计算结果</h2>
        <div class="calculation-info">
          <span class="info-item">
            <i class="fas fa-chart-line"></i>
            一致性比率: {{ consistencyRatio }}
          </span>
          <span class="info-item">
            <i class="fas fa-check-circle"></i>
            权重状态: {{ weightStatus }}
          </span>
        </div>
      </div>

      <!-- 权重表格 -->
      <div class="weight-table-container">
        <el-table 
          :data="weightData" 
          style="width: 100%" 
          stripe
          border
          class="weight-table"
        >
          <el-table-column 
            prop="feature" 
            label="案例特征" 
            width="200"
            align="center"
          />
          <el-table-column 
            prop="weight" 
            label="对应权值" 
            align="center"
          >
            <template #default="scope">
              <span class="weight-value">{{ scope.row.weight }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 权重分析 -->
      <div class="weight-analysis">
        <div class="analysis-section">
          <h3>权重分析</h3>
          <div class="analysis-charts">
            <div class="chart-container">
              <div class="chart-title">权重分布饼图</div>
              <div id="weightPieChart" class="chart-placeholder">
                <i class="fas fa-chart-pie"></i>
                <span>权重分布可视化</span>
              </div>
            </div>
            <div class="chart-container">
              <div class="chart-title">特征重要性排序</div>
              <div id="weightBarChart" class="chart-placeholder">
                <i class="fas fa-chart-bar"></i>
                <span>重要性排序图</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 计算详情 -->
      <div class="calculation-details">
        <el-collapse v-model="activeCollapse">
          <el-collapse-item title="判断矩阵详情" name="matrix">
            <div class="matrix-display">
              <table class="judgment-matrix">
                <thead>
                  <tr>
                    <th>特征</th>
                    <th v-for="feature in featureNames" :key="feature">{{ feature }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, i) in judgmentMatrix" :key="i">
                    <td class="feature-name">{{ featureNames[i] }}</td>
                    <td v-for="(value, j) in row" :key="j" class="matrix-value">
                      {{ value }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </el-collapse-item>
          
          <el-collapse-item title="计算过程" name="process">
            <div class="calculation-process">
              <div class="process-step">
                <h4>1. 构建判断矩阵</h4>
                <p>基于用户输入的两两比较值构建判断矩阵</p>
              </div>
              <div class="process-step">
                <h4>2. 计算特征向量</h4>
                <p>使用几何平均法计算各特征的权重向量</p>
              </div>
              <div class="process-step">
                <h4>3. 一致性检验</h4>
                <p>计算一致性指标CI和一致性比率CR，验证判断矩阵的一致性</p>
              </div>
              <div class="process-step">
                <h4>4. 权重归一化</h4>
                <p>对计算得到的权重向量进行归一化处理</p>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="action-buttons">
      <el-button @click="goBack">返回上一步</el-button>
      <el-button @click="saveWeights" type="success">保存权重配置</el-button>
      <el-button @click="proceedToMatching" type="primary">进入案例匹配</el-button>
    </div>

    <!-- 页脚信息 -->
    <div class="page-footer">
      <div class="footer-content">
        <span>© 2017-2021 天津理工大学 All Rights Reserved</span>
        <div class="pagination-controls">
          <el-button text>上一步</el-button>
          <el-button text>下一步</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 当前步骤
const currentStep = ref(2)

// 折叠面板状态
const activeCollapse = ref(['matrix'])

// 一致性比率和权重状态
const consistencyRatio = ref('0.0267')
const weightStatus = ref('通过一致性检验')

// 权重数据
const weightData = ref([
  { feature: '案例特征', weight: '0.0267' },
  { feature: '密度', weight: '0.0465' },
  { feature: '内直径', weight: '0.0882' },
  { feature: '加工系统编号', weight: '0.2474' },
  { feature: '加工系统类别', weight: '0.1645' },
  { feature: '加工系统次类别', weight: '0.0773' },
  { feature: '加工器械', weight: '0.0504' },
  { feature: '加工系统结构', weight: '0.1223' },
  { feature: '加工系统类别', weight: '0.0847' },
  { feature: '加工系统次类别', weight: '0.0436' },
  { feature: '加工器械', weight: '0.0283' },
  { feature: '加工系统高压力', weight: '0.018' }
])

// 特征名称（用于矩阵显示）
const featureNames = ref([
  '案例特征', '密度', '内直径', '加工系统编号', '加工系统类别',
  '加工系统次类别', '加工器械', '加工系统结构'
])

// 判断矩阵数据（示例数据）
const judgmentMatrix = ref([
  [1, 0.5, 0.33, 0.2, 0.25, 0.33, 0.5, 0.2],
  [2, 1, 0.5, 0.33, 0.5, 0.5, 1, 0.33],
  [3, 2, 1, 0.5, 1, 1, 2, 0.5],
  [5, 3, 2, 1, 2, 2, 3, 1],
  [4, 2, 1, 0.5, 1, 1, 2, 0.5],
  [3, 2, 1, 0.5, 1, 1, 2, 0.5],
  [2, 1, 0.5, 0.33, 0.5, 0.5, 1, 0.33],
  [5, 3, 2, 1, 2, 2, 3, 1]
])

// 方法
const exportWeights = () => {
  ElMessage.success('权重配置已导出')
}

const recalculateWeights = () => {
  ElMessage.info('正在重新计算权重...')
  // 模拟重新计算
  setTimeout(() => {
    ElMessage.success('权重计算完成')
  }, 1500)
}

const goBack = () => {
  ElMessage.info('返回权重设置页面')
  window.location.href = '/process/case-reasoning/weight-matrix'
}

const saveWeights = () => {
  ElMessageBox.confirm('确定要保存当前权重配置吗？', '确认保存', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'info'
  }).then(() => {
    ElMessage.success('权重配置已保存')
  }).catch(() => {
    ElMessage.info('已取消保存')
  })
}

const proceedToMatching = () => {
  ElMessage.success('进入案例匹配阶段')
  currentStep.value = 3
  window.location.href = '/process/case-reasoning/matching-result'
}

onMounted(() => {
  console.log('计算特征权重页面已加载')
})
</script>

<style scoped>
.weight-calculation-view {
  padding: 24px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title i {
  color: #409eff;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.steps-navigation {
  background: white;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.weight-results-container {
  background: white;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.results-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 18px;
}

.calculation-info {
  display: flex;
  gap: 24px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
  font-size: 14px;
}

.info-item i {
  color: #67c23a;
}

.weight-table-container {
  margin-bottom: 32px;
}

.weight-table {
  border-radius: 8px;
  overflow: hidden;
}

.weight-value {
  font-weight: 600;
  color: #409eff;
  font-family: 'Courier New', monospace;
}

.weight-analysis {
  margin-bottom: 32px;
}

.analysis-section h3 {
  margin-bottom: 16px;
  color: #2c3e50;
}

.analysis-charts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.chart-container {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
}

.chart-title {
  font-weight: 600;
  margin-bottom: 16px;
  color: #606266;
}

.chart-placeholder {
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 4px;
  color: #909399;
}

.chart-placeholder i {
  font-size: 48px;
  margin-bottom: 8px;
}

.calculation-details {
  margin-bottom: 32px;
}

.matrix-display {
  overflow-x: auto;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 4px;
}

.judgment-matrix {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.judgment-matrix th,
.judgment-matrix td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.judgment-matrix th {
  background: #f0f0f0;
  font-weight: 600;
}

.feature-name {
  background: #f9f9f9;
  font-weight: 600;
}

.matrix-value {
  font-family: 'Courier New', monospace;
}

.calculation-process {
  padding: 16px;
}

.process-step {
  margin-bottom: 16px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 4px;
  border-left: 4px solid #409eff;
}

.process-step h4 {
  margin: 0 0 8px 0;
  color: #409eff;
}

.process-step p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 32px;
}

.page-footer {
  background: white;
  border-radius: 8px;
  padding: 16px 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #909399;
  font-size: 12px;
}

.pagination-controls {
  display: flex;
  gap: 8px;
}

@media (max-width: 768px) {
  .weight-calculation-view {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .results-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .calculation-info {
    justify-content: center;
  }
  
  .analysis-charts {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
}

:deep(.el-step__title) {
  font-size: 14px;
}

:deep(.el-step__description) {
  font-size: 12px;
}

:deep(.el-table th) {
  background-color: #f8f9fa;
}

:deep(.el-collapse-item__header) {
  font-weight: 600;
}
</style> 