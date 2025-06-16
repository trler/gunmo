<template>
  <div class="case-reasoning-result-view">
    <!-- 步骤导航 -->
    <div class="steps-navigation">
      <el-steps :active="3" finish-status="success" align-center>
        <el-step title="输入新案例" description="完成案例特征录入" />
        <el-step title="设置特征值" description="配置特征参数" />
        <el-step title="计算特征权重" description="基于AHP计算权重" />
        <el-step title="案例优选" description="智能匹配推荐" />
      </el-steps>
    </div>

    <!-- 搜索条件区域 -->
    <div class="search-conditions">
      <el-row :gutter="20" class="search-row">
        <el-col :span="6">
          <div class="condition-item">
            <span class="condition-label">案例含:</span>
            <el-input v-model="searchConditions.caseContent" placeholder="0.4" size="small" />
          </div>
        </el-col>
        <el-col :span="6">
          <div class="condition-item">
            <span class="condition-label">相似度案例总数h:</span>
            <el-input v-model="searchConditions.similarCaseCount" placeholder="0.7" size="small" />
          </div>
        </el-col>
        <el-col :span="6">
          <div class="condition-item">
            <span class="condition-label">修正因子Wh:</span>
            <el-input v-model="searchConditions.correctionFactor" placeholder="0.4" size="small" />
          </div>
        </el-col>
        <el-col :span="6">
          <div class="action-buttons">
            <el-button type="primary" size="small" @click="searchSimilarCases">查案例优选</el-button>
          </div>
        </el-col>
      </el-row>

      <div class="search-results-info">
        <span>搜索结果:</span>
      </div>
    </div>

    <!-- 案例匹配结果表格 -->
    <div class="results-container">
      <!-- 主要案例信息 -->
      <div class="main-case-info">
        <span>显示第 1 号到第 1 条记录，共有 1 条记录</span>
      </div>

      <!-- 案例详情表格 -->
      <div class="case-details-table">
        <el-table 
          :data="caseResults" 
          style="width: 100%" 
          border
          stripe
          class="details-table"
        >
          <el-table-column prop="caseNumber" label="案例实例" width="80" align="center" />
          <el-table-column prop="caseType" label="案例种类" width="100" align="center" />
          <el-table-column prop="processingSystem" label="加工系统次类别" width="120" align="center" />
          <el-table-column prop="systemSubcategory" label="加工系统次类别" width="120" align="center" />
          <el-table-column prop="height" label="高" width="80" align="center" />
          <el-table-column prop="externalDiameter" label="外直径" width="80" align="center" />
          <el-table-column prop="internalDiameter" label="内直径" width="80" align="center" />
          <el-table-column prop="processingSystemStructure" label="加工系统结构类型" width="140" align="center" />
          <el-table-column prop="processingEquipment" label="加工器械" width="100" align="center" />
          <el-table-column prop="processingPressure" label="加工压强" width="100" align="center" />
          <el-table-column prop="systemStructure" label="加工系统结构类型" width="140" align="center" />
          <el-table-column prop="remainingTime" label="残余时间" width="100" align="center" />
          <el-table-column prop="processingTime" label="加工系统时间" width="120" align="center" />
          <el-table-column prop="processingTimeUnit" label="加工系统时间单位" width="140" align="center" />
        </el-table>
      </div>

      <!-- 相似度分析表格 -->
      <div class="similarity-analysis">
        <div class="analysis-info">
          <span>显示第 1 号到第 12 条记录，共有 12 条记录</span>
        </div>
        
        <el-table 
          :data="similarityResults" 
          style="width: 100%" 
          border
          stripe
          class="similarity-table"
        >
          <el-table-column prop="caseId" label="案例编号" width="100" align="center" />
          <el-table-column prop="caseNumber" label="案例实例" width="100" align="center" />
          <el-table-column prop="caseType" label="案例种类" width="100" align="center" />
          <el-table-column prop="processingSystem" label="加工系统次类别" width="120" align="center" />
          <el-table-column prop="systemSubcategory" label="加工系统次类别" width="120" align="center" />
          <el-table-column prop="height" label="高" width="80" align="center" />
          <el-table-column prop="externalDiameter" label="外直径" width="80" align="center" />
          <el-table-column prop="internalDiameter" label="内直径" width="80" align="center" />
          <el-table-column prop="processingSystemStructure" label="加工系统结构类型" width="140" align="center" />
          <el-table-column prop="processingEquipment" label="加工器械" width="100" align="center" />
          <el-table-column prop="processingPressure" label="加工压强" width="100" align="center" />
          <el-table-column prop="systemStructure" label="加工系统结构类型" width="140" align="center" />
          <el-table-column prop="remainingTime" label="残余时间" width="100" align="center" />
          <el-table-column prop="processingTime" label="加工系统时间" width="120" align="center" />
          <el-table-column prop="similarity" label="相似度" width="100" align="center">
            <template #default="scope">
              <span class="similarity-score">{{ scope.row.similarity }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="recommendation" label="推荐级别" width="120" align="center">
            <template #default="scope">
              <el-tag :type="getRecommendationTagType(scope.row.recommendation)" size="small">
                {{ scope.row.recommendation }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
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
import { ElMessage } from 'element-plus'

// 搜索条件
const searchConditions = reactive({
  caseContent: '0.4',
  similarCaseCount: '0.7',
  correctionFactor: '0.4'
})

// 案例结果数据
const caseResults = ref([
  {
    caseNumber: '史钻类',
    caseType: '含类型',
    processingSystem: '1',
    systemSubcategory: '4',
    height: '89',
    externalDiameter: '200',
    internalDiameter: '100',
    processingSystemStructure: '0.654',
    processingEquipment: '1.8',
    processingPressure: '50',
    systemStructure: '0.3',
    remainingTime: '-250',
    processingTime: '60',
    processingTimeUnit: '1'
  }
])

// 相似度分析结果
const similarityResults = ref([
  {
    caseId: '00243',
    caseNumber: '史钻类',
    caseType: '含类型',
    processingSystem: '1',
    systemSubcategory: '4',
    height: '82',
    externalDiameter: '200',
    internalDiameter: '120',
    processingSystemStructure: '0.685',
    processingEquipment: '1.62',
    processingPressure: '48',
    systemStructure: '0.298',
    remainingTime: '-210',
    processingTime: '68',
    similarity: '0.895',
    recommendation: '2号=角磨盘'
  },
  {
    caseId: '00241',
    caseNumber: '史钻类',
    caseType: '含类型',
    processingSystem: '1',
    systemSubcategory: '4',
    height: '82',
    externalDiameter: '200',
    internalDiameter: '120',
    processingSystemStructure: '0.586',
    processingEquipment: '1.62',
    processingPressure: '48',
    systemStructure: '0.299',
    remainingTime: '-250',
    processingTime: '55',
    similarity: '0.896',
    recommendation: '2号=角磨盘'
  },
  {
    caseId: '00134',
    caseNumber: '史钻类',
    caseType: '含类型',
    processingSystem: '1',
    systemSubcategory: '4',
    height: '86',
    externalDiameter: '190',
    internalDiameter: '100',
    processingSystemStructure: '0.662',
    processingEquipment: '1.7',
    processingPressure: '52',
    systemStructure: '0.311',
    remainingTime: '-220',
    processingTime: '60',
    similarity: '0.825',
    recommendation: '2号=角磨盘'
  },
  {
    caseId: '00397',
    caseNumber: '史钻类',
    caseType: '含类型',
    processingSystem: '1',
    systemSubcategory: '4',
    height: '86',
    externalDiameter: '190',
    internalDiameter: '100',
    processingSystemStructure: '0.752',
    processingEquipment: '1.7',
    processingPressure: '52',
    systemStructure: '0.335',
    remainingTime: '-250',
    processingTime: '62',
    similarity: '0.821',
    recommendation: '2号=角磨盘'
  },
  {
    caseId: '00202',
    caseNumber: '史钻类',
    caseType: '含类型',
    processingSystem: '1',
    systemSubcategory: '4',
    height: '93',
    externalDiameter: '210',
    internalDiameter: '110',
    processingSystemStructure: '0.771',
    processingEquipment: '1.5',
    processingPressure: '50',
    systemStructure: '0.321',
    remainingTime: '-220',
    processingTime: '60',
    similarity: '0.8',
    recommendation: '3号=角磨盘'
  },
  {
    caseId: '00201',
    caseNumber: '史钻类',
    caseType: '含类型',
    processingSystem: '1',
    systemSubcategory: '4',
    height: '90',
    externalDiameter: '210',
    internalDiameter: '110',
    processingSystemStructure: '0.652',
    processingEquipment: '1.5',
    processingPressure: '50',
    systemStructure: '0.3',
    remainingTime: '-200',
    processingTime: '60',
    similarity: '0.786',
    recommendation: '7号=角磨盘'
  },
  {
    caseId: '00240',
    caseNumber: '史钻类',
    caseType: '含类型',
    processingSystem: '1',
    systemSubcategory: '4',
    height: '88',
    externalDiameter: '200',
    internalDiameter: '90',
    processingSystemStructure: '0.759',
    processingEquipment: '1.5',
    processingPressure: '50',
    systemStructure: '0.328',
    remainingTime: '-215',
    processingTime: '62',
    similarity: '0.781',
    recommendation: '7号=角磨盘'
  },
  {
    caseId: '00162',
    caseNumber: '史钻类',
    caseType: '20CrMnTi',
    processingSystem: '1',
    systemSubcategory: '4',
    height: '90',
    externalDiameter: '220',
    internalDiameter: '100',
    processingSystemStructure: '0.784',
    processingEquipment: '1.6',
    processingPressure: '42',
    systemStructure: '0.385',
    remainingTime: '-215',
    processingTime: '53',
    similarity: '0.756',
    recommendation: '2号=角磨盘'
  },
  {
    caseId: '00231',
    caseNumber: '史钻类',
    caseType: '20CrMnTi',
    processingSystem: '1',
    systemSubcategory: '4',
    height: '90',
    externalDiameter: '200',
    internalDiameter: '110',
    processingSystemStructure: '0.584',
    processingEquipment: '1.7',
    processingPressure: '45',
    systemStructure: '0.4',
    remainingTime: '-215',
    processingTime: '55',
    similarity: '0.752',
    recommendation: '2号=角磨盘'
  },
  {
    caseId: '00322',
    caseNumber: '史钻类',
    caseType: '20CrMnTi',
    processingSystem: '1',
    systemSubcategory: '4',
    height: '85',
    externalDiameter: '230',
    internalDiameter: '120',
    processingSystemStructure: '0.669',
    processingEquipment: '1.82',
    processingPressure: '50',
    systemStructure: '0.309',
    remainingTime: '-200',
    processingTime: '62',
    similarity: '0.732',
    recommendation: '4号=角磨盘'
  },
  {
    caseId: '00020',
    caseNumber: '史钻类',
    caseType: '含类型',
    processingSystem: '1',
    systemSubcategory: '4',
    height: '85',
    externalDiameter: '230',
    internalDiameter: '120',
    processingSystemStructure: '0.592',
    processingEquipment: '1.82',
    processingPressure: '48',
    systemStructure: '0.253',
    remainingTime: '-210',
    processingTime: '62',
    similarity: '0.731',
    recommendation: '2号=角磨盘'
  },
  {
    caseId: '00324',
    caseNumber: '史钻类',
    caseType: '含类型',
    processingSystem: '1',
    systemSubcategory: '4',
    height: '86',
    externalDiameter: '220',
    internalDiameter: '110',
    processingSystemStructure: '0.577',
    processingEquipment: '1.65',
    processingPressure: '50',
    systemStructure: '0.245',
    remainingTime: '-215',
    processingTime: '58',
    similarity: '0.719',
    recommendation: '2号=角磨盘'
  }
])

// 方法
const searchSimilarCases = () => {
  ElMessage.success('正在查询相似案例...')
  // 模拟搜索过程
  setTimeout(() => {
    ElMessage.success('案例优选完成')
  }, 1000)
}

const getRecommendationTagType = (recommendation: string) => {
  if (recommendation.includes('2号')) return 'success'
  if (recommendation.includes('3号')) return 'warning'
  if (recommendation.includes('4号')) return 'info'
  if (recommendation.includes('7号')) return 'danger'
  return 'primary'
}

onMounted(() => {
  console.log('案例推理结果页面已加载')
})
</script>

<style scoped>
.case-reasoning-result-view {
  padding: 16px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.steps-navigation {
  background: white;
  padding: 20px;
  border-radius: 6px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.search-conditions {
  background: white;
  padding: 16px;
  border-radius: 6px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.search-row {
  margin-bottom: 12px;
}

.condition-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.condition-label {
  font-size: 12px;
  color: #666;
  white-space: nowrap;
  min-width: 100px;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
}

.search-results-info {
  font-size: 12px;
  color: #666;
  margin-top: 8px;
}

.results-container {
  background: white;
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.main-case-info {
  font-size: 12px;
  color: #666;
  margin-bottom: 12px;
}

.case-details-table {
  margin-bottom: 24px;
}

.details-table {
  border-radius: 4px;
  overflow: hidden;
  font-size: 11px;
}

.similarity-analysis {
  margin-top: 20px;
}

.analysis-info {
  font-size: 12px;
  color: #666;
  margin-bottom: 12px;
}

.similarity-table {
  border-radius: 4px;
  overflow: hidden;
  font-size: 11px;
}

.similarity-score {
  font-weight: 600;
  color: #e6a23c;
  font-family: 'Courier New', monospace;
}

.page-footer {
  background: white;
  border-radius: 6px;
  padding: 12px 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #999;
  font-size: 11px;
}

.pagination-controls {
  display: flex;
  gap: 6px;
}

/* 表格样式优化 */
:deep(.el-table) {
  font-size: 11px;
}

:deep(.el-table th) {
  background-color: #5a8fb8 !important;
  color: white !important;
  font-weight: 600;
  font-size: 11px;
  padding: 6px 4px;
}

:deep(.el-table td) {
  padding: 4px;
  font-size: 11px;
}

:deep(.el-table .cell) {
  padding: 2px 4px;
  line-height: 1.2;
}

:deep(.el-input--small .el-input__inner) {
  height: 24px;
  font-size: 11px;
  padding: 0 8px;
}

:deep(.el-button--small) {
  font-size: 11px;
  padding: 4px 8px;
  height: 24px;
}

:deep(.el-step__title) {
  font-size: 12px;
}

:deep(.el-step__description) {
  font-size: 10px;
}

:deep(.el-tag--small) {
  height: 18px;
  font-size: 10px;
  padding: 0 4px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .case-reasoning-result-view {
    padding: 8px;
  }
  
  .search-row {
    flex-direction: column;
    gap: 8px;
  }
  
  .condition-item {
    flex-direction: column;
    align-items: stretch;
    gap: 4px;
  }
  
  .condition-label {
    min-width: auto;
    font-size: 11px;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
}
</style> 