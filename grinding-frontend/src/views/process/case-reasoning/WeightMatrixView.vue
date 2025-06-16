<template>
  <div class="weight-matrix-view">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-balance-scale"></i>
        权重设置与判断矩阵
      </h1>
      <div class="header-actions">
        <el-button type="success" @click="calculateAllWeights" :loading="calculating">
          <i class="fas fa-calculator"></i>
          计算权重
        </el-button>
        <el-button type="primary" @click="validateConsistency" :loading="validating">
          <i class="fas fa-check-circle"></i>
          一致性检验
        </el-button>
        <el-button @click="resetMatrices">
          <i class="fas fa-redo"></i>
          重置矩阵
        </el-button>
      </div>
    </div>

    <!-- 特征选择区 -->
    <div class="feature-selection-card">
      <h3>案例特征选择</h3>
      <p class="selection-tip">请选择需要进行权重分析的案例特征（至少选择3个特征）</p>
      <div class="feature-groups">
        <div v-for="group in featureGroups" :key="group.name" class="feature-group">
          <h4>{{ group.label }}</h4>
          <div class="feature-checkboxes">
            <el-checkbox-group v-model="selectedFeatures[group.name]" @change="onFeatureSelectionChange">
              <el-checkbox 
                v-for="feature in group.features" 
                :key="feature.key"
                :label="feature.key"
                class="feature-checkbox"
              >
                {{ feature.label }}
              </el-checkbox>
            </el-checkbox-group>
          </div>
        </div>
      </div>
    </div>

    <!-- 判断矩阵区域 -->
    <div class="matrices-container" v-if="totalSelectedFeatures >= 3">
      <div class="matrix-grid">
        <div v-for="group in activeGroups" :key="group.name" class="matrix-card">
          <div class="matrix-header">
            <h3>{{ group.label }}判断矩阵</h3>
            <div class="matrix-status">
              <el-tag v-if="group.calculating" type="warning">
                <i class="fas fa-spinner fa-spin"></i>
                权重计算中...
              </el-tag>
              <el-tag v-else-if="group.weights.length > 0" type="success">
                <i class="fas fa-check"></i>
                CR={{ group.cr.toFixed(3) }}，{{ group.cr < 0.1 ? '通过检验' : '需要调整' }}
              </el-tag>
              <el-tag v-else type="info">
                <i class="fas fa-info-circle"></i>
                待计算权重
              </el-tag>
            </div>
          </div>

          <!-- 判断矩阵表格 -->
          <div class="matrix-table-container">
            <table class="judgment-matrix">
              <thead>
                <tr>
                  <th class="matrix-corner"></th>
                  <th v-for="feature in group.selectedFeatures" :key="feature.key" class="matrix-header-cell">
                    {{ feature.key }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(rowFeature, i) in group.selectedFeatures" :key="rowFeature.key">
                  <td class="matrix-row-header">{{ rowFeature.key }}</td>
                  <td v-for="(colFeature, j) in group.selectedFeatures" :key="colFeature.key" class="matrix-cell">
                    <el-input-number
                      v-if="i <= j"
                      v-model="group.matrix[i][j]"
                      :min="1"
                      :max="9"
                      :step="1"
                      :precision="0"
                      size="small"
                      class="matrix-input"
                      @change="onMatrixValueChange(group, i, j)"
                      :disabled="i === j"
                    />
                    <span v-else class="reciprocal-value">
                      {{ group.matrix[j][i] > 0 ? (1 / group.matrix[j][i]).toFixed(3) : '-' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 权重结果显示 -->
          <div v-if="group.weights.length > 0" class="weight-results">
            <h4>计算结果</h4>
            <div class="weight-list">
              <div v-for="(weight, index) in group.weights" :key="index" class="weight-item">
                <span class="feature-name">{{ group.selectedFeatures[index].key }}</span>
                <div class="weight-bar-container">
                  <div class="weight-bar">
                    <div class="weight-fill" :style="{ width: (weight * 100) + '%' }"></div>
                  </div>
                  <span class="weight-value">{{ (weight * 100).toFixed(2) }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 综合权重结果 -->
    <div v-if="comprehensiveWeights.length > 0" class="comprehensive-results">
      <div class="results-header">
        <h2>综合权重分析结果</h2>
        <div class="overall-status">
          <el-tag v-if="overallConsistency" type="success" size="large">
            <i class="fas fa-check-circle"></i>
            整体一致性检验通过
          </el-tag>
          <el-tag v-else type="danger" size="large">
            <i class="fas fa-exclamation-triangle"></i>
            整体一致性检验未通过，建议调整
          </el-tag>
        </div>
      </div>
      
      <div class="comprehensive-chart">
        <div class="chart-container">
          <div class="weight-bars">
            <div v-for="(item, index) in comprehensiveWeights" :key="index" class="comprehensive-weight-item">
              <div class="weight-label">{{ item.feature }}</div>
              <div class="weight-bar-large">
                <div class="weight-fill-large" :style="{ width: (item.weight * 100) + '%' }"></div>
                <span class="weight-text">{{ (item.weight * 100).toFixed(2) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="export-actions">
        <el-button type="primary" @click="exportWeights">
          <i class="fas fa-download"></i>
          导出权重配置
        </el-button>
        <el-button type="success" @click="applyWeights">
          <i class="fas fa-check"></i>
          应用到案例匹配
        </el-button>
      </div>
    </div>

    <!-- 帮助信息 -->
    <div class="help-section">
      <el-collapse v-model="activeHelp">
        <el-collapse-item title="层次分析法使用说明" name="help">
          <div class="help-content">
            <h4>判断矩阵填写规则：</h4>
            <ul>
              <li><strong>1</strong> - 两个因素同等重要</li>
              <li><strong>3</strong> - 前者比后者稍微重要</li>
              <li><strong>5</strong> - 前者比后者明显重要</li>
              <li><strong>7</strong> - 前者比后者强烈重要</li>
              <li><strong>9</strong> - 前者比后者极端重要</li>
              <li><strong>2,4,6,8</strong> - 上述相邻判断的中值</li>
            </ul>
            <h4>一致性检验标准：</h4>
            <ul>
              <li>CR < 0.1：一致性可以接受</li>
              <li>CR ≥ 0.1：一致性不佳，需要重新调整判断矩阵</li>
            </ul>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 接口定义
interface Feature {
  key: string
  label: string
}

interface FeatureGroup {
  name: string
  label: string
  features: Feature[]
  selectedFeatures: Feature[]
  matrix: number[][]
  weights: number[]
  cr: number
  calculating: boolean
}

// 响应式数据
const calculating = ref(false)
const validating = ref(false)
const activeHelp = ref([])

// 特征组定义
const featureGroups = ref([
  {
    name: 'criteria',
    label: '准则层',
    features: [
      { key: 'A', label: '零件特征' },
      { key: 'A1', label: '几何特征' },
      { key: 'A2', label: '材料特征' },
      { key: 'A3', label: '工艺特征' }
    ]
  },
  {
    name: 'dimension',
    label: '尺寸层',
    features: [
      { key: 'A1', label: '长度' },
      { key: 'A11', label: '直径' },
      { key: 'A12', label: '厚度' },
      { key: 'A13', label: '表面积' }
    ]
  },
  {
    name: 'preprocessing',
    label: '加工前特征层',
    features: [
      { key: 'A2', label: '表面粗糙度' },
      { key: 'A21', label: '硬度' },
      { key: 'A22', label: '残余应力' },
      { key: 'A23', label: '表面缺陷' },
      { key: 'A24', label: '几何公差' }
    ]
  },
  {
    name: 'requirements',
    label: '加工要求层',
    features: [
      { key: 'A3', label: '精度要求' },
      { key: 'A31', label: '表面质量' },
      { key: 'A32', label: '去毛刺' },
      { key: 'A33', label: '圆角处理' },
      { key: 'A34', label: '表面光洁度' },
      { key: 'A35', label: '尺寸精度' }
    ]
  }
])

// 选中的特征
const selectedFeatures = reactive({
  criteria: [],
  dimension: [],
  preprocessing: [],
  requirements: []
})

// 矩阵组数据
const matrixGroups = ref<FeatureGroup[]>([])

// 综合权重结果
const comprehensiveWeights = ref([])
const overallConsistency = ref(false)

// 随机一致性指标表
const RI_TABLE = {
  1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
}

// 计算属性
const totalSelectedFeatures = computed(() => {
  return Object.values(selectedFeatures).reduce((total, features) => total + features.length, 0)
})

const activeGroups = computed(() => {
  return matrixGroups.value.filter(group => group.selectedFeatures.length >= 2)
})

// 层次分析法核心算法

// 计算特征向量（几何平均法）
const calculateEigenVector = (matrix: number[][]): number[] => {
  const n = matrix.length
  const weights = []
  
  for (let i = 0; i < n; i++) {
    let product = 1
    for (let j = 0; j < n; j++) {
      product *= matrix[i][j]
    }
    weights[i] = Math.pow(product, 1 / n)
  }
  
  // 归一化
  const sum = weights.reduce((acc, w) => acc + w, 0)
  return weights.map(w => w / sum)
}

// 计算最大特征值
const calculateLambdaMax = (matrix: number[][], weights: number[]): number => {
  const n = matrix.length
  let lambdaMax = 0
  
  for (let i = 0; i < n; i++) {
    let sum = 0
    for (let j = 0; j < n; j++) {
      sum += matrix[i][j] * weights[j]
    }
    lambdaMax += sum / weights[i]
  }
  
  return lambdaMax / n
}

// 一致性检验
const calculateConsistencyRatio = (matrix: number[][], weights: number[]): number => {
  const n = matrix.length
  if (n <= 2) return 0
  
  const lambdaMax = calculateLambdaMax(matrix, weights)
  const CI = (lambdaMax - n) / (n - 1)
  const RI = RI_TABLE[n] || 1.49
  
  return CI / RI
}

// 事件处理函数

// 特征选择变化处理
const onFeatureSelectionChange = () => {
  updateMatrixGroups()
}

// 更新矩阵组
const updateMatrixGroups = () => {
  matrixGroups.value = featureGroups.value.map(group => {
    const selectedInGroup = selectedFeatures[group.name] || []
    const selectedFeatureObjects = group.features.filter(f => selectedInGroup.includes(f.key))
    
    const size = selectedFeatureObjects.length
    const matrix = Array(size).fill(null).map(() => Array(size).fill(1))
    
    return {
      ...group,
      selectedFeatures: selectedFeatureObjects,
      matrix,
      weights: [],
      cr: 0,
      calculating: false
    }
  }).filter(group => group.selectedFeatures.length >= 2)
}

// 矩阵值变化处理
const onMatrixValueChange = (group: FeatureGroup, i: number, j: number) => {
  // 自动填充对称位置的倒数值
  if (i !== j && group.matrix[i][j] > 0) {
    group.matrix[j][i] = 1 / group.matrix[i][j]
  }
}

// 计算单个组的权重
const calculateGroupWeights = async (group: FeatureGroup) => {
  group.calculating = true
  
  try {
    // 模拟计算延迟
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 检查矩阵是否完整
    const n = group.matrix.length
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        if (group.matrix[i][j] <= 0) {
          throw new Error(`矩阵第${i+1}行第${j+1}列的值无效`)
        }
      }
    }
    
    // 计算权重
    const weights = calculateEigenVector(group.matrix)
    const cr = calculateConsistencyRatio(group.matrix, weights)
    
    group.weights = weights
    group.cr = cr
    
    if (cr >= 0.1) {
      ElMessage.warning(`${group.label}的一致性检验未通过 (CR=${cr.toFixed(3)})，建议调整判断矩阵`)
    } else {
      ElMessage.success(`${group.label}权重计算完成，一致性检验通过 (CR=${cr.toFixed(3)})`)
    }
    
  } catch (error) {
    ElMessage.error(`${group.label}权重计算失败：${error instanceof Error ? error.message : '未知错误'}`)
    group.weights = []
    group.cr = 1
  } finally {
    group.calculating = false
  }
}

// 计算所有权重
const calculateAllWeights = async () => {
  calculating.value = true
  
  try {
    // 并行计算所有组的权重
    await Promise.all(
      matrixGroups.value.map(group => calculateGroupWeights(group))
    )
    
    // 计算综合权重
    calculateComprehensiveWeights()
    
  } catch (error) {
    ElMessage.error('权重计算失败：' + (error instanceof Error ? error.message : '未知错误'))
  } finally {
    calculating.value = false
  }
}

// 计算综合权重
const calculateComprehensiveWeights = () => {
  const allFeatures = []
  
  matrixGroups.value.forEach(group => {
    if (group.weights.length > 0) {
      group.selectedFeatures.forEach((feature, index) => {
        allFeatures.push({
          feature: `${group.label}-${feature.label}`,
          weight: group.weights[index],
          group: group.name
        })
      })
    }
  })
  
  // 按权重排序
  allFeatures.sort((a, b) => b.weight - a.weight)
  
  comprehensiveWeights.value = allFeatures
  
  // 检查整体一致性
  const avgCR = matrixGroups.value.reduce((sum, group) => sum + group.cr, 0) / matrixGroups.value.length
  overallConsistency.value = avgCR < 0.1
}

// 一致性验证
const validateConsistency = async () => {
  validating.value = true
  
  try {
    let allPassed = true
    const results = []
    
    for (const group of matrixGroups.value) {
      if (group.weights.length === 0) {
        await calculateGroupWeights(group)
      }
      
      const passed = group.cr < 0.1
      if (!passed) allPassed = false
      
      results.push({
        group: group.label,
        cr: group.cr,
        passed
      })
    }
    
    if (allPassed) {
      ElMessage.success('所有判断矩阵一致性检验通过！')
    } else {
      ElMessage.warning('部分判断矩阵一致性检验未通过，建议调整')
    }
    
  } catch (error) {
    ElMessage.error('一致性检验失败：' + (error instanceof Error ? error.message : '未知错误'))
  } finally {
    validating.value = false
  }
}

// 重置矩阵
const resetMatrices = () => {
  ElMessageBox.confirm('确定要重置所有判断矩阵吗？', '确认重置', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    matrixGroups.value.forEach(group => {
      const size = group.selectedFeatures.length
      group.matrix = Array(size).fill(null).map(() => Array(size).fill(1))
      group.weights = []
      group.cr = 0
    })
    comprehensiveWeights.value = []
    overallConsistency.value = false
    ElMessage.success('判断矩阵已重置')
  })
}

// 导出权重配置
const exportWeights = () => {
  const exportData = {
    timestamp: new Date().toISOString(),
    groups: matrixGroups.value.map(group => ({
      name: group.name,
      label: group.label,
      features: group.selectedFeatures,
      weights: group.weights,
      cr: group.cr
    })),
    comprehensiveWeights: comprehensiveWeights.value,
    overallConsistency: overallConsistency.value
  }
  
  const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `weight_config_${Date.now()}.json`
  a.click()
  URL.revokeObjectURL(url)
  
  ElMessage.success('权重配置已导出')
}

// 应用权重到案例匹配
const applyWeights = () => {
  if (comprehensiveWeights.value.length === 0) {
    ElMessage.warning('请先计算权重')
    return
  }
  
  if (!overallConsistency.value) {
    ElMessageBox.confirm('整体一致性检验未通过，是否仍要应用权重配置？', '确认应用', {
      confirmButtonText: '仍要应用',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      doApplyWeights()
    })
  } else {
    doApplyWeights()
  }
}

// 执行权重应用
const doApplyWeights = () => {
  const weightConfig = {
    groups: matrixGroups.value.map(group => ({
      name: group.name,
      features: group.selectedFeatures.map((feature, index) => ({
        key: feature.key,
        label: feature.label,
        weight: group.weights[index] || 0
      }))
    })),
    timestamp: Date.now()
  }
  
  // 存储到 localStorage
  localStorage.setItem('caseWeightConfig', JSON.stringify(weightConfig))
  
  ElMessage.success('权重配置已应用到案例匹配模块')
  
  console.log('权重配置应用:', weightConfig)
}

onMounted(() => {
  // 初始化默认选择
  selectedFeatures.criteria = ['A', 'A1', 'A2']
  selectedFeatures.dimension = ['A1', 'A11', 'A12']
  updateMatrixGroups()
})
</script>

<style scoped>
.weight-matrix-view {
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
  color: #e67e22;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.feature-selection-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.feature-selection-card h3 {
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.selection-tip {
  color: #666;
  margin-bottom: 20px;
}

.feature-groups {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.feature-group h4 {
  margin: 0 0 12px 0;
  color: #34495e;
  font-size: 16px;
}

.feature-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.feature-checkbox {
  margin-right: 16px;
  margin-bottom: 8px;
}

.matrices-container {
  margin-bottom: 24px;
}

.matrix-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 24px;
}

.matrix-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.matrix-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.matrix-header h3 {
  margin: 0;
  color: #2c3e50;
}

.matrix-table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.judgment-matrix {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.judgment-matrix th,
.judgment-matrix td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.matrix-corner {
  background-color: #f8f9fa;
  font-weight: bold;
}

.matrix-header-cell {
  background-color: #e9ecef;
  font-weight: bold;
  min-width: 60px;
}

.matrix-row-header {
  background-color: #e9ecef;
  font-weight: bold;
  min-width: 60px;
}

.matrix-cell {
  min-width: 80px;
}

.matrix-input {
  width: 60px;
}

.matrix-input :deep(.el-input__inner) {
  text-align: center;
  font-size: 12px;
}

.reciprocal-value {
  color: #666;
  font-size: 12px;
}

.weight-results h4 {
  margin: 0 0 12px 0;
  color: #2c3e50;
}

.weight-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.weight-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.feature-name {
  min-width: 80px;
  font-weight: 500;
  color: #34495e;
}

.weight-bar-container {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.weight-bar {
  flex: 1;
  height: 16px;
  background-color: #ecf0f1;
  border-radius: 8px;
  overflow: hidden;
}

.weight-fill {
  height: 100%;
  background: linear-gradient(90deg, #3498db, #2980b9);
  transition: width 0.3s ease;
}

.weight-value {
  min-width: 50px;
  font-size: 12px;
  font-weight: 500;
  color: #2c3e50;
}

.comprehensive-results {
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
}

.results-header h2 {
  margin: 0;
  color: #2c3e50;
}

.comprehensive-chart {
  margin-bottom: 24px;
}

.weight-bars {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comprehensive-weight-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.weight-label {
  min-width: 200px;
  font-weight: 500;
  color: #2c3e50;
}

.weight-bar-large {
  flex: 1;
  height: 24px;
  background-color: #ecf0f1;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
}

.weight-fill-large {
  height: 100%;
  background: linear-gradient(90deg, #27ae60, #2ecc71);
  transition: width 0.5s ease;
}

.weight-text {
  position: absolute;
  right: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #2c3e50;
}

.export-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.help-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.help-content h4 {
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.help-content ul {
  margin: 0 0 16px 0;
  padding-left: 20px;
}

.help-content li {
  margin-bottom: 4px;
  color: #555;
}

@media (max-width: 768px) {
  .weight-matrix-view {
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
  
  .matrix-grid {
    grid-template-columns: 1fr;
  }
  
  .feature-groups {
    grid-template-columns: 1fr;
  }
  
  .results-header {
    flex-direction: column;
    gap: 12px;
  }
  
  .comprehensive-weight-item {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }
  
  .weight-label {
    min-width: auto;
  }
}
</style> 