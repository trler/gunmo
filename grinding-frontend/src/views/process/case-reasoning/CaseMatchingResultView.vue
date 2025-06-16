<template>
  <div class="case-matching-result-view">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-search"></i>
        案例匹配结果
      </h1>
      <div class="header-actions">
        <el-button type="primary" @click="executeSearch" :loading="searching">
          <i class="fas fa-play"></i>
          执行检索
        </el-button>
        <el-button @click="clearResults">
          <i class="fas fa-trash"></i>
          清空结果
        </el-button>
        <el-button @click="exportResults" :disabled="!matchingResults.length">
          <i class="fas fa-download"></i>
          导出结果
        </el-button>
      </div>
    </div>

    <!-- 检索配置区 -->
    <div class="search-config-card">
      <h3>检索配置</h3>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="相似度算法：">
            <el-select v-model="searchConfig.algorithm" placeholder="选择算法" style="width: 100%">
              <el-option label="加权欧氏距离" value="weighted_euclidean" />
              <el-option label="余弦相似度" value="cosine_similarity" />
              <el-option label="曼哈顿距离" value="manhattan_distance" />
              <el-option label="综合相似度" value="comprehensive" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="匹配阈值：">
            <el-slider 
              v-model="searchConfig.threshold" 
              :min="0" 
              :max="100" 
              show-input
              :marks="{ 70: '70%', 80: '80%', 90: '90%' }"
            />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="返回数量：">
            <el-input-number 
              v-model="searchConfig.maxResults" 
              :min="10" 
              :max="500" 
              :step="10"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-row>
      
      <div class="search-status">
        <el-alert 
          v-if="searchStatus.message"
          :title="searchStatus.message"
          :type="searchStatus.type"
          :closable="false"
          show-icon
        />
      </div>
    </div>

    <!-- 匹配结果表格 -->
    <div class="results-table-card">
      <div class="table-header">
        <h3>匹配结果 ({{ pagination.total }} 条记录)</h3>
        <div class="table-actions">
          <el-input 
            v-model="filterText" 
            placeholder="搜索案例ID或材质"
            style="width: 200px; margin-right: 10px"
            clearable
          >
            <template #prefix>
              <i class="fas fa-search"></i>
            </template>
          </el-input>
          <el-select v-model="sortField" placeholder="排序字段" style="width: 120px; margin-right: 10px">
            <el-option label="匹配度" value="similarity_score" />
            <el-option label="案例ID" value="case_id" />
            <el-option label="创建时间" value="create_time" />
          </el-select>
        </div>
      </div>

      <el-table 
        ref="resultsTable"
        :data="filteredResults" 
        v-loading="searching"
        element-loading-text="正在执行案例匹配..."
        stripe
        highlight-current-row
        @row-click="showCaseDetail"
        style="width: 100%"
      >
        <el-table-column type="index" label="序号" width="60" />
        
        <el-table-column prop="case_id" label="案例ID" width="120" sortable>
          <template #default="scope">
            <el-link type="primary" @click="showCaseDetail(scope.row)">
              {{ scope.row.case_id }}
            </el-link>
          </template>
        </el-table-column>
        
        <el-table-column prop="material_type" label="物料材质" width="120" sortable />
        
        <el-table-column prop="original_grinding_time" label="原滚磨时间(h)" width="130" sortable>
          <template #default="scope">
            <span>{{ scope.row.original_grinding_time || '-' }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="similarity_score" label="匹配度得分" width="130" sortable>
          <template #default="scope">
            <div class="score-container">
              <el-progress 
                :percentage="scope.row.similarity_score" 
                :color="getScoreColor(scope.row.similarity_score)"
                :stroke-width="8"
                text-inside
              />
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="matched_features" label="主要匹配特征" min-width="200">
          <template #default="scope">
            <el-tag 
              v-for="feature in scope.row.matched_features.slice(0, 3)" 
              :key="feature"
              size="small"
              style="margin-right: 5px"
            >
              {{ feature }}
            </el-tag>
            <span v-if="scope.row.matched_features.length > 3" class="more-features">
              +{{ scope.row.matched_features.length - 3 }}项
            </span>
          </template>
        </el-table-column>
        
        <el-table-column prop="process_parameters" label="关键工艺参数" min-width="180">
          <template #default="scope">
            <div class="process-params">
              <div v-if="scope.row.process_parameters.grinding_speed">
                转速: {{ scope.row.process_parameters.grinding_speed }}rpm
              </div>
              <div v-if="scope.row.process_parameters.grinding_pressure">
                压力: {{ scope.row.process_parameters.grinding_pressure }}MPa
              </div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="create_time" label="创建时间" width="140" sortable>
          <template #default="scope">
            <span>{{ formatDateTime(scope.row.create_time) }}</span>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="140" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="showCaseDetail(scope.row)">
              详情
            </el-button>
            <el-button type="success" size="small" @click="applyCaseParameters(scope.row)">
              应用
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页控件 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[20, 50, 100, 200]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 案例详情弹窗 -->
    <el-dialog 
      v-model="detailDialog.visible" 
      title="案例详细信息"
      width="80%"
      top="5vh"
      :close-on-click-modal="false"
    >
      <div v-if="detailDialog.caseData" class="case-detail-content">
        <el-tabs v-model="detailDialog.activeTab" type="border-card">
          
          <!-- 基本信息 -->
          <el-tab-pane label="基本信息" name="basic">
            <div class="detail-section">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-descriptions title="案例基础信息" :column="1" border>
                    <el-descriptions-item label="案例ID">{{ detailDialog.caseData.case_id }}</el-descriptions-item>
                    <el-descriptions-item label="物料材质">{{ detailDialog.caseData.material_type }}</el-descriptions-item>
                    <el-descriptions-item label="匹配度得分">
                      <el-tag :type="detailDialog.caseData.similarity_score >= 80 ? 'success' : 'warning'">
                        {{ detailDialog.caseData.similarity_score }}%
                      </el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="创建时间">{{ formatDateTime(detailDialog.caseData.create_time) }}</el-descriptions-item>
                  </el-descriptions>
                </el-col>
                <el-col :span="12">
                  <el-descriptions title="匹配特征" :column="1" border>
                    <el-descriptions-item label="匹配特征数">{{ detailDialog.caseData.matched_features.length }}</el-descriptions-item>
                    <el-descriptions-item label="特征列表">
                      <div class="feature-tags">
                        <el-tag 
                          v-for="feature in detailDialog.caseData.matched_features" 
                          :key="feature"
                          size="small"
                          style="margin: 2px"
                        >
                          {{ feature }}
                        </el-tag>
                      </div>
                    </el-descriptions-item>
                  </el-descriptions>
                </el-col>
              </el-row>
            </div>
          </el-tab-pane>
          
          <!-- 工艺参数 -->
          <el-tab-pane label="工艺参数" name="process">
            <div class="detail-section">
              <el-descriptions title="滚磨工艺参数" :column="2" border>
                <el-descriptions-item label="滚磨时间">{{ detailDialog.caseData.original_grinding_time }}h</el-descriptions-item>
                <el-descriptions-item label="转速">{{ detailDialog.caseData.process_parameters.grinding_speed }}rpm</el-descriptions-item>
                <el-descriptions-item label="压力">{{ detailDialog.caseData.process_parameters.grinding_pressure }}MPa</el-descriptions-item>
                <el-descriptions-item label="介质类型">{{ detailDialog.caseData.process_parameters.media_type }}</el-descriptions-item>
                <el-descriptions-item label="介质比例">{{ detailDialog.caseData.process_parameters.media_ratio }}</el-descriptions-item>
                <el-descriptions-item label="液体添加剂">{{ detailDialog.caseData.process_parameters.additive_type }}</el-descriptions-item>
              </el-descriptions>
            </div>
          </el-tab-pane>
          
          <!-- 特征对比 -->
          <el-tab-pane label="特征对比" name="comparison">
            <div class="detail-section">
              <el-table :data="detailDialog.featureComparison" border>
                <el-table-column prop="feature_name" label="特征名称" width="150" />
                <el-table-column prop="target_value" label="目标值" width="120" />
                <el-table-column prop="case_value" label="案例值" width="120" />
                <el-table-column prop="similarity" label="相似度" width="120">
                  <template #default="scope">
                    <el-progress 
                      :percentage="scope.row.similarity" 
                      :stroke-width="6"
                      :color="getScoreColor(scope.row.similarity)"
                    />
                  </template>
                </el-table-column>
                <el-table-column prop="weight" label="权重" width="100">
                  <template #default="scope">
                    <span>{{ (scope.row.weight * 100).toFixed(1) }}%</span>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-tab-pane>
          
        </el-tabs>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="detailDialog.visible = false">关闭</el-button>
          <el-button type="success" @click="applyCaseParameters(detailDialog.caseData)">
            应用此案例
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { caseMatchingService, type SimilarityResult } from '@/services/case-matching'

// 接口定义
interface MatchingCase {
  case_id: string
  material_type: string
  original_grinding_time: number
  similarity_score: number
  matched_features: string[]
  process_parameters: {
    grinding_speed: number
    grinding_pressure: number
    media_type: string
    media_ratio: string
    additive_type: string
  }
  create_time: string
  feature_details: Record<string, any>
}

interface SearchConfig {
  algorithm: string
  threshold: number
  maxResults: number
}

// 响应式数据
const searching = ref(false)
const filterText = ref('')
const sortField = ref('similarity_score')

// 检索配置
const searchConfig = reactive<SearchConfig>({
  algorithm: 'weighted_euclidean',
  threshold: 70,
  maxResults: 100
})

// 搜索状态
const searchStatus = reactive({
  message: '',
  type: 'info' as 'success' | 'warning' | 'info' | 'error'
})

// 匹配结果数据
const matchingResults = ref<MatchingCase[]>([])

// 分页配置
const pagination = reactive({
  currentPage: 1,
  pageSize: 20,
  total: 0
})

// 详情弹窗
const detailDialog = reactive({
  visible: false,
  activeTab: 'basic',
  caseData: null as MatchingCase | null,
  featureComparison: []
})

// 计算属性
const filteredResults = computed(() => {
  let results = matchingResults.value
  
  if (filterText.value) {
    results = results.filter(item => 
      item.case_id.toLowerCase().includes(filterText.value.toLowerCase()) ||
      item.material_type.toLowerCase().includes(filterText.value.toLowerCase())
    )
  }
  
  // 排序
  if (sortField.value) {
    results.sort((a, b) => {
      const aVal = a[sortField.value]
      const bVal = b[sortField.value]
      if (sortField.value === 'similarity_score') {
        return bVal - aVal // 降序
      }
      return aVal > bVal ? 1 : -1
    })
  }
  
  return results
})

// 工具方法
const getScoreColor = (score: number) => {
  if (score >= 90) return '#67c23a'
  if (score >= 80) return '#e6a23c'
  if (score >= 70) return '#f56c6c'
  return '#909399'
}

const formatDateTime = (dateTime: string) => {
  return new Date(dateTime).toLocaleString('zh-CN')
}

// 案例匹配算法实现
const executeSearch = async () => {
  searching.value = true
  searchStatus.message = '正在执行案例匹配...'
  searchStatus.type = 'info'
  
  try {
    // 获取目标案例数据（从特征录入区）
    const targetCaseData = getTargetCaseData()
    if (!targetCaseData) {
      throw new Error('请先在案例特征录入区填写目标案例数据')
    }
    
    // 加载权重配置
    caseMatchingService.loadWeightConfig()
    
    // 构建数据库查询
    const sqlQuery = buildSimilarityQuery(targetCaseData, searchConfig)
    console.log('Generated SQL Query:', sqlQuery)
    
    // 执行查询（模拟）
    const searchResults = await performDatabaseSearch(sqlQuery, searchConfig)
    
    // 处理结果
    matchingResults.value = searchResults
    pagination.total = searchResults.length
    
    searchStatus.message = `匹配完成，找到 ${searchResults.length} 个相似案例`
    searchStatus.type = 'success'
    
    ElMessage.success(`案例匹配完成，共找到 ${searchResults.length} 个相似案例`)
    
  } catch (error) {
    searchStatus.message = `匹配失败：${error.message}`
    searchStatus.type = 'error'
    ElMessage.error('案例匹配失败：' + error.message)
  } finally {
    searching.value = false
  }
}

// 获取目标案例数据
const getTargetCaseData = () => {
  // 从localStorage或者特征录入组件获取数据
  const storedData = localStorage.getItem('currentCaseFeatures')
  if (storedData) {
    return JSON.parse(storedData)
  }
  
  // 模拟数据
  return {
    material_type: '钛合金',
    diameter: 25.4,
    thickness: 3.2,
    surface_roughness: 0.8,
    hardness: 350,
    precision_requirement: 'IT7'
  }
}

// 构建SQL查询语句
const buildSimilarityQuery = (targetCase: any, config: SearchConfig): string => {
  const weightConfig = caseMatchingService.getWeightConfig()
  if (!weightConfig) {
    throw new Error('权重配置未找到，请先配置特征权重')
  }
  
  // 构建加权相似度计算SQL
  let similarityCalculation = ''
  const conditions = []
  
  if (config.algorithm === 'weighted_euclidean') {
    // 加权欧氏距离
    const distanceTerms = []
    weightConfig.groups.forEach(group => {
      group.features.forEach(feature => {
        if (targetCase[feature.key] !== undefined) {
          distanceTerms.push(`${feature.weight} * POWER((${feature.key} - ${targetCase[feature.key]}), 2)`)
          conditions.push(`${feature.key} IS NOT NULL`)
        }
      })
    })
    
    if (distanceTerms.length > 0) {
      similarityCalculation = `(100 - SQRT(${distanceTerms.join(' + ')})) AS similarity_score`
    }
  } else if (config.algorithm === 'cosine_similarity') {
    // 余弦相似度
    const dotProduct = []
    const targetNorm = []
    const caseNorm = []
    
    weightConfig.groups.forEach(group => {
      group.features.forEach(feature => {
        if (targetCase[feature.key] !== undefined) {
          dotProduct.push(`(${feature.key} * ${targetCase[feature.key]})`)
          targetNorm.push(`POWER(${targetCase[feature.key]}, 2)`)
          caseNorm.push(`POWER(${feature.key}, 2)`)
          conditions.push(`${feature.key} IS NOT NULL`)
        }
      })
    })
    
    if (dotProduct.length > 0) {
      similarityCalculation = `(${dotProduct.join(' + ')} / (SQRT(${targetNorm.join(' + ')}) * SQRT(${caseNorm.join(' + ')}))) * 100 AS similarity_score`
    }
  }
  
  // 构建完整SQL
  const sql = `
    SELECT 
      case_id,
      material_type,
      original_grinding_time,
      grinding_speed,
      grinding_pressure,
      media_type,
      media_ratio,
      additive_type,
      create_time,
      ${similarityCalculation}
    FROM grinding_cases 
    WHERE ${conditions.join(' AND ')}
    HAVING similarity_score >= ${config.threshold}
    ORDER BY similarity_score DESC
    LIMIT ${config.maxResults}
  `
  
  return sql
}

// 执行数据库搜索（模拟）
const performDatabaseSearch = async (sqlQuery: string, config: SearchConfig): Promise<MatchingCase[]> => {
  // 模拟网络延迟
  await new Promise(resolve => setTimeout(resolve, 1500))
  
  // 模拟数据库查询结果
  const mockResults: MatchingCase[] = [
    {
      case_id: 'GC_001',
      material_type: '钛合金',
      original_grinding_time: 4.5,
      similarity_score: 92,
      matched_features: ['材质类型', '直径', '表面粗糙度', '硬度'],
      process_parameters: {
        grinding_speed: 120,
        grinding_pressure: 0.8,
        media_type: '钢珠',
        media_ratio: '3:1',
        additive_type: '研磨液A'
      },
      create_time: '2024-01-15T10:30:00',
      feature_details: {}
    },
    {
      case_id: 'GC_002',
      material_type: '钛合金',
      original_grinding_time: 3.8,
      similarity_score: 88,
      matched_features: ['材质类型', '厚度', '精度要求'],
      process_parameters: {
        grinding_speed: 100,
        grinding_pressure: 0.6,
        media_type: '陶瓷珠',
        media_ratio: '2:1',
        additive_type: '研磨液B'
      },
      create_time: '2024-01-10T14:20:00',
      feature_details: {}
    },
    {
      case_id: 'GC_003',
      material_type: '不锈钢',
      original_grinding_time: 6.2,
      similarity_score: 75,
      matched_features: ['直径', '表面粗糙度'],
      process_parameters: {
        grinding_speed: 150,
        grinding_pressure: 1.0,
        media_type: '钢珠',
        media_ratio: '4:1',
        additive_type: '研磨液C'
      },
      create_time: '2024-01-08T09:15:00',
      feature_details: {}
    }
  ]
  
  // 根据阈值过滤
  return mockResults.filter(result => result.similarity_score >= config.threshold)
}

// 显示案例详情
const showCaseDetail = (caseData: MatchingCase) => {
  detailDialog.caseData = caseData
  detailDialog.activeTab = 'basic'
  
  // 生成特征对比数据
  detailDialog.featureComparison = generateFeatureComparison(caseData)
  
  detailDialog.visible = true
}

// 生成特征对比数据
const generateFeatureComparison = (caseData: MatchingCase) => {
  const targetCase = getTargetCaseData()
  const weightConfig = caseMatchingService.getWeightConfig()
  
  if (!weightConfig || !targetCase) return []
  
  const comparison = []
  
  weightConfig.groups.forEach(group => {
    group.features.forEach(feature => {
      if (targetCase[feature.key] !== undefined) {
        const targetValue = targetCase[feature.key]
        const caseValue = caseData.feature_details[feature.key] || '-'
        const similarity = Math.random() * 40 + 60 // 模拟相似度
        
        comparison.push({
          feature_name: feature.label,
          target_value: targetValue,
          case_value: caseValue,
          similarity: Math.round(similarity),
          weight: feature.weight
        })
      }
    })
  })
  
  return comparison
}

// 应用案例参数
const applyCaseParameters = (caseData: MatchingCase) => {
  ElMessageBox.confirm(
    `确定要应用案例 ${caseData.case_id} 的工艺参数吗？这将覆盖当前的工艺设置。`,
    '确认应用',
    {
      confirmButtonText: '确定应用',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // 应用工艺参数到系统
    const appliedParameters = {
      grinding_time: caseData.original_grinding_time,
      grinding_speed: caseData.process_parameters.grinding_speed,
      grinding_pressure: caseData.process_parameters.grinding_pressure,
      media_type: caseData.process_parameters.media_type,
      media_ratio: caseData.process_parameters.media_ratio,
      additive_type: caseData.process_parameters.additive_type
    }
    
    // 保存到localStorage或发送到后端
    localStorage.setItem('appliedProcessParameters', JSON.stringify(appliedParameters))
    
    ElMessage.success(`已成功应用案例 ${caseData.case_id} 的工艺参数`)
    
    // 可以触发事件通知其他组件
    console.log('Applied parameters:', appliedParameters)
    
    if (detailDialog.visible) {
      detailDialog.visible = false
    }
  })
}

// 清空结果
const clearResults = () => {
  matchingResults.value = []
  pagination.total = 0
  searchStatus.message = ''
  ElMessage.info('已清空匹配结果')
}

// 导出结果
const exportResults = () => {
  const exportData = caseMatchingService.exportResults(
    matchingResults.value.map(result => ({
      caseId: result.case_id,
      similarity: result.similarity_score,
      matchedFeatures: result.matched_features,
      weightedScore: result.similarity_score / 100
    })),
    'csv'
  )
  
  const blob = new Blob([exportData], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `case_matching_results_${Date.now()}.csv`
  a.click()
  URL.revokeObjectURL(url)
  
  ElMessage.success('匹配结果已导出')
}

// 分页处理
const handleSizeChange = (newSize: number) => {
  pagination.pageSize = newSize
  pagination.currentPage = 1
}

const handleCurrentChange = (newPage: number) => {
  pagination.currentPage = newPage
}

onMounted(() => {
  // 初始化时检查是否有目标案例数据
  const targetCase = getTargetCaseData()
  if (targetCase) {
    searchStatus.message = '目标案例数据已加载，可以执行匹配'
    searchStatus.type = 'info'
  } else {
    searchStatus.message = '请先在案例特征录入区填写目标案例数据'
    searchStatus.type = 'warning'
  }
})
</script>

<style scoped>
.case-matching-result-view {
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
  color: #3498db;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.search-config-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-config-card h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
}

.search-status {
  margin-top: 16px;
}

.results-table-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.table-header h3 {
  margin: 0;
  color: #2c3e50;
}

.table-actions {
  display: flex;
  align-items: center;
}

.score-container {
  padding: 0 8px;
}

.more-features {
  color: #909399;
  font-size: 12px;
}

.process-params {
  font-size: 12px;
  line-height: 1.4;
}

.process-params div {
  margin-bottom: 2px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.case-detail-content {
  max-height: 60vh;
  overflow-y: auto;
}

.detail-section {
  padding: 16px 0;
}

.feature-tags {
  max-height: 100px;
  overflow-y: auto;
}

.dialog-footer {
  text-align: right;
}

@media (max-width: 768px) {
  .case-matching-result-view {
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
  
  .table-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .table-actions {
    justify-content: center;
  }
}
</style> 