<template>
  <div class="case-feature-entry-view">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-brain"></i>
        案例推理系统
      </h1>
      <div class="header-actions">
        <el-button type="primary" icon="Plus" @click="showAddDialog = true">输入新案例</el-button>
        <el-button icon="Refresh" @click="refreshData">刷新</el-button>
      </div>
    </div>

    <!-- 案例特征录入对话框 -->
    <el-dialog 
      v-model="showAddDialog" 
      title="案例特征录入"
      width="85%"
      top="3vh"
      :close-on-click-modal="false"
      class="case-feature-dialog"
    >
      <el-form 
        ref="formRef" 
        :model="formData" 
        :rules="formRules" 
        label-width="140px"
        class="case-feature-form"
      >
        <!-- 第一行：零件信息 -->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="零件型号：" prop="partModel">
              <el-select v-model="formData.partModel" placeholder="请选择零件型号" style="width: 100%">
                <el-option label="齿轮件" value="齿轮件" />
                <el-option label="轴承件" value="轴承件" />
                <el-option label="叶片件" value="叶片件" />
                <el-option label="复杂件" value="复杂件" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="零件材质：" prop="partMaterial">
              <el-select v-model="formData.partMaterial" placeholder="请选择零件材质" style="width: 100%">
                <el-option label="钛合金" value="钛合金" />
                <el-option label="不锈钢" value="不锈钢" />
                <el-option label="铝合金" value="铝合金" />
                <el-option label="碳钢" value="碳钢" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="工艺参数种类：" prop="processParameterType">
              <el-select v-model="formData.processParameterType" placeholder="请选择工艺参数种类" style="width: 100%">
                <el-option label="表面处理" value="表面处理" />
                <el-option label="精密加工" value="精密加工" />
                <el-option label="热处理" value="热处理" />
                <el-option label="抛光工艺" value="抛光工艺" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 第二行：尺寸参数 -->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="内径或含缺陷：" prop="innerDiameterOrDefect">
              <el-input v-model="formData.innerDiameterOrDefect" placeholder="请输入内径或含缺陷信息">
                <template #append>mm</template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="长度或最大截面：" prop="lengthOrMaxSection">
              <el-input v-model="formData.lengthOrMaxSection" placeholder="请输入长度或最大截面">
                <template #append>mm</template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="高度或宽度：" prop="heightOrWidth">
              <el-input v-model="formData.heightOrWidth" placeholder="请输入高度或宽度">
                <template #append>mm</template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 第三行：工艺参数 -->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="分量设定值：" prop="componentSettingValue">
              <el-input v-model="formData.componentSettingValue" placeholder="请输入分量设定值" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="加工系统编号：" prop="processingSystemNumber">
              <el-input v-model="formData.processingSystemNumber" placeholder="请输入加工系统编号" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="加工方式：" prop="processingMethod">
              <el-select v-model="formData.processingMethod" placeholder="请选择加工方式" style="width: 100%">
                <el-option label="粗加工" value="粗加工" />
                <el-option label="精加工" value="精加工" />
                <el-option label="超精加工" value="超精加工" />
                <el-option label="复合加工" value="复合加工" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 第四行：质量参数 -->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="加工量：" prop="processingAmount">
              <el-input v-model="formData.processingAmount" placeholder="请输入加工量">
                <template #append>μm</template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="厚度：" prop="thickness">
              <el-input v-model="formData.thickness" placeholder="请输入厚度">
                <template #append>mm</template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="条件变量：" prop="conditionVariable">
              <el-input v-model="formData.conditionVariable" placeholder="请输入条件变量" />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 第五行：质量控制参数 -->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="等级：" prop="level">
              <el-select v-model="formData.level" placeholder="请选择等级" style="width: 100%">
                <el-option label="A级" value="A级" />
                <el-option label="B级" value="B级" />
                <el-option label="C级" value="C级" />
                <el-option label="D级" value="D级" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="尺寸：" prop="dimension">
              <el-input v-model="formData.dimension" placeholder="请输入尺寸规格" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="质量：" prop="quality">
              <el-input v-model="formData.quality" placeholder="请输入质量要求">
                <template #append>Ra</template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 第六行：误差与备注 -->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="误差：" prop="error">
              <el-input v-model="formData.error" placeholder="请输入误差范围">
                <template #append>±μm</template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="16">
            <el-form-item label="备注：" prop="remarks">
              <el-input 
                v-model="formData.remarks" 
                type="textarea" 
                :rows="2"
                placeholder="请输入相关备注信息"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 案例相似度设置 -->
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="相似度阈值：" prop="similarityThreshold">
              <el-slider
                v-model="formData.similarityThreshold"
                :min="0"
                :max="100"
                :step="5"
                show-input
                :format-tooltip="formatTooltip"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="权重分配：" prop="weightDistribution">
              <el-select v-model="formData.weightDistribution" placeholder="请选择权重分配方案" style="width: 100%">
                <el-option label="均等权重" value="均等权重" />
                <el-option label="尺寸优先" value="尺寸优先" />
                <el-option label="材质优先" value="材质优先" />
                <el-option label="工艺优先" value="工艺优先" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showAddDialog = false">关闭</el-button>
          <el-button @click="resetForm">重置</el-button>
          <el-button type="success" @click="searchSimilarCases">搜索相似案例</el-button>
          <el-button type="primary" @click="submitForm">保存案例</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 案例列表展示 -->
    <div class="case-list-container">
      <div class="case-tabs">
        <el-tabs v-model="activeTab" @tab-click="handleTabClick">
          <el-tab-pane label="当前案例库" name="current">
            <el-table :data="currentCases" style="width: 100%" stripe>
              <el-table-column prop="partModel" label="零件型号" width="120" />
              <el-table-column prop="partMaterial" label="零件材质" width="100" />
              <el-table-column prop="processParameterType" label="工艺参数种类" width="130" />
              <el-table-column prop="processingMethod" label="加工方式" width="100" />
              <el-table-column prop="quality" label="质量要求" width="100" />
              <el-table-column prop="level" label="等级" width="80" />
              <el-table-column prop="createTime" label="创建时间" width="180" />
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="viewCase(scope.row)">查看</el-button>
                  <el-button type="warning" size="small" @click="editCase(scope.row)">编辑</el-button>
                  <el-button type="danger" size="small" @click="deleteCase(scope.row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          
          <el-tab-pane label="相似案例推荐" name="similar">
            <div v-if="similarCases.length === 0" class="empty-state">
              <el-empty description="暂无相似案例，请先进行案例搜索" />
            </div>
            <el-table v-else :data="similarCases" style="width: 100%" stripe>
              <el-table-column prop="partModel" label="零件型号" width="120" />
              <el-table-column prop="partMaterial" label="零件材质" width="100" />
              <el-table-column prop="similarity" label="相似度" width="100">
                <template #default="scope">
                  <el-progress :percentage="scope.row.similarity" :stroke-width="8" />
                </template>
              </el-table-column>
              <el-table-column prop="processingMethod" label="推荐工艺" width="120" />
              <el-table-column prop="quality" label="预期质量" width="100" />
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="scope">
                  <el-button type="success" size="small" @click="adoptCase(scope.row)">采用</el-button>
                  <el-button type="info" size="small" @click="viewDetails(scope.row)">详情</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

// 响应式数据
const showAddDialog = ref(false)
const editingCase = ref(null)
const formRef = ref<FormInstance>()
const activeTab = ref('current')

// 表单数据
const formData = reactive({
  partModel: '',
  partMaterial: '',
  processParameterType: '',
  innerDiameterOrDefect: '',
  lengthOrMaxSection: '',
  heightOrWidth: '',
  componentSettingValue: '',
  processingSystemNumber: '',
  processingMethod: '',
  processingAmount: '',
  thickness: '',
  conditionVariable: '',
  level: '',
  dimension: '',
  quality: '',
  error: '',
  remarks: '',
  similarityThreshold: 85,
  weightDistribution: '均等权重'
})

// 表单验证规则
const formRules: FormRules = {
  partModel: [
    { required: true, message: '请选择零件型号', trigger: 'change' }
  ],
  partMaterial: [
    { required: true, message: '请选择零件材质', trigger: 'change' }
  ],
  processParameterType: [
    { required: true, message: '请选择工艺参数种类', trigger: 'change' }
  ],
  processingMethod: [
    { required: true, message: '请选择加工方式', trigger: 'change' }
  ]
}

// 当前案例库数据
const currentCases = ref([
  {
    id: 1,
    partModel: '齿轮件',
    partMaterial: '钛合金',
    processParameterType: '表面处理',
    processingMethod: '精加工',
    quality: '0.4',
    level: 'A级',
    createTime: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    partModel: '轴承件',
    partMaterial: '不锈钢',
    processParameterType: '精密加工',
    processingMethod: '超精加工',
    quality: '0.2',
    level: 'A级',
    createTime: '2024-01-14 14:20:00'
  }
])

// 相似案例数据
const similarCases = ref([])

// 方法
const refreshData = () => {
  ElMessage.success('数据已刷新')
}

const formatTooltip = (val: number) => {
  return `${val}%`
}

const resetForm = () => {
  Object.keys(formData).forEach(key => {
    if (key !== 'similarityThreshold' && key !== 'weightDistribution') {
      formData[key] = ''
    }
  })
  formData.similarityThreshold = 85
  formData.weightDistribution = '均等权重'
}

const searchSimilarCases = () => {
  // 模拟搜索相似案例
  const mockSimilarCases = [
    {
      id: 101,
      partModel: '齿轮件',
      partMaterial: '钛合金',
      similarity: 92,
      processingMethod: '精加工',
      quality: '0.3',
      matchedFeatures: ['零件型号', '材质', '加工方式']
    },
    {
      id: 102,
      partModel: '齿轮件',
      partMaterial: '铝合金',
      similarity: 78,
      processingMethod: '精加工',
      quality: '0.5',
      matchedFeatures: ['零件型号', '加工方式']
    }
  ]
  
  similarCases.value = mockSimilarCases
  activeTab.value = 'similar'
  ElMessage.success(`找到 ${mockSimilarCases.length} 个相似案例`)
}

const submitForm = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    const newCase = {
      ...formData,
      id: Date.now(),
      createTime: new Date().toLocaleString('zh-CN')
    }
    
    currentCases.value.unshift(newCase)
    ElMessage.success('案例保存成功')
    showAddDialog.value = false
    resetForm()
    activeTab.value = 'current'
  } catch (error) {
    ElMessage.error('请检查表单填写是否正确')
  }
}

const viewCase = (row: any) => {
  ElMessage.info(`查看案例：${row.partModel}`)
}

const editCase = (row: any) => {
  editingCase.value = row
  Object.keys(formData).forEach(key => {
    if (row[key] !== undefined) {
      formData[key] = row[key]
    }
  })
  showAddDialog.value = true
}

const deleteCase = (row: any) => {
  ElMessageBox.confirm('确定要删除这个案例吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    const index = currentCases.value.findIndex(item => item.id === row.id)
    if (index !== -1) {
      currentCases.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  }).catch(() => {
    ElMessage.info('已取消删除')
  })
}

const adoptCase = (row: any) => {
  ElMessageBox.confirm('确定要采用这个相似案例的参数吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'info'
  }).then(() => {
    // 将相似案例的参数填充到表单中
    formData.partModel = row.partModel
    formData.partMaterial = row.partMaterial
    formData.processingMethod = row.processingMethod
    formData.quality = row.quality
    
    showAddDialog.value = true
    ElMessage.success('已采用相似案例参数，请完善其他信息')
  })
}

const viewDetails = (row: any) => {
  ElMessage.info(`查看详细信息：相似度 ${row.similarity}%`)
}

const handleTabClick = (tab: any) => {
  console.log('切换到标签页:', tab.name)
}

onMounted(() => {
  console.log('案例推理系统已加载')
})
</script>

<style scoped>
.case-feature-entry-view {
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
  color: #67c23a;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.case-feature-dialog {
  max-height: 90vh;
}

.case-feature-form {
  max-height: 65vh;
  overflow-y: auto;
  padding-right: 12px;
}

.case-list-container {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.case-tabs {
  width: 100%;
}

.empty-state {
  padding: 40px;
  text-align: center;
}

.dialog-footer {
  text-align: right;
  padding: 16px 0;
}

:deep(.el-input-group__append) {
  background-color: #f5f7fa;
  color: #909399;
  border-left: 1px solid #dcdfe6;
}

:deep(.el-slider__runway) {
  margin: 16px 0;
}

:deep(.el-tabs__content) {
  padding-top: 20px;
}

:deep(.el-progress-bar__outer) {
  border-radius: 4px;
}

@media (max-width: 768px) {
  .case-feature-entry-view {
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
  
  .case-feature-dialog {
    width: 95%;
  }
}
</style> 