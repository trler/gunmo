<template>
  <div class="process-entry-admin-view">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-user-shield"></i>
        光整工艺录入(管理员)
      </h1>
      <div class="header-actions">
        <el-button type="primary" icon="Plus" @click="showProcessDialog = true">新建工艺</el-button>
        <el-button icon="Refresh" @click="refreshData">刷新</el-button>
        <el-button type="success" icon="Download" @click="exportData">导出</el-button>
      </div>
    </div>

    <!-- 工艺录入对话框 -->
    <el-dialog 
      v-model="showProcessDialog" 
      title="光整工艺录入"
      width="90%"
      top="3vh"
      :close-on-click-modal="false"
    >
      <el-form 
        ref="processFormRef" 
        :model="processData" 
        label-width="120px"
        class="process-form"
      >
        <!-- 基础信息 -->
        <div class="form-section">
          <h3 class="section-title">基础信息</h3>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="生产批量：" prop="batchNumber">
                <el-input v-model="processData.batchNumber" placeholder="s001" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="数量：" prop="quantity">
                <el-input v-model="processData.quantity" placeholder="3" />
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="工件要求：">
            <el-row :gutter="10">
              <el-col :span="6">
                <el-select v-model="workpieceRequirementType" placeholder="表面粗糙度(Ra)" style="width: 100%">
                  <el-option label="表面粗糙度(Ra)" value="表面粗糙度(Ra)" />
                  <el-option label="平行度" value="平行度" />
                  <el-option label="垂直度" value="垂直度" />
                </el-select>
              </el-col>
              <el-col :span="4">
                <el-input v-model="processData.checkValue" placeholder="检查值" />
              </el-col>
              <el-col :span="4">
                <el-input v-model="processData.requirementValue" placeholder="0.4" />
              </el-col>
              <el-col :span="2">
                <el-button icon="Plus" @click="addWorkpieceRequirement" />
              </el-col>
            </el-row>
          </el-form-item>

          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="特殊保护要求：" prop="specialProtection">
                <el-input v-model="processData.specialProtection" placeholder="特殊保护要求" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="工件特殊要求：" prop="workpieceSpecialReq">
                <el-input v-model="processData.workpieceSpecialReq" placeholder="工件特殊要求" />
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="其他：" prop="others">
            <el-input 
              v-model="processData.others" 
              type="textarea" 
              :rows="2"
              placeholder="1.注意对比表面刀痕，不能超过：2.不可"
            />
          </el-form-item>

          <el-form-item label="附件：">
            <div class="file-upload-area">
              <el-upload
                class="upload-demo"
                action="#"
                :on-change="handleFileChange"
                :auto-upload="false"
                accept="*"
              >
                <el-button type="primary">选择文件</el-button>
                <el-button type="success" @click="startUpload" style="margin-left: 10px">开始上传</el-button>
              </el-upload>
              <div v-if="uploadedFiles.length > 0" class="file-list">
                <div v-for="(file, index) in uploadedFiles" :key="index" class="file-item">
                  <span>{{ file.name }}</span>
                  <el-button type="text" @click="removeFile(index)">删除</el-button>
                </div>
              </div>
            </div>
          </el-form-item>
        </div>

        <!-- 工艺流程 -->
        <div class="form-section">
          <h3 class="section-title">工艺流程</h3>
          <div v-for="(step, stepIndex) in processData.processSteps" :key="stepIndex" class="process-step">
            <div class="step-header">
              <h4>工步：{{ step.stepNumber }}</h4>
              <el-button type="danger" size="small" @click="removeProcessStep(stepIndex)" v-if="processData.processSteps.length > 1">删除工步</el-button>
            </div>

            <!-- 设备配置 -->
            <div class="equipment-section">
              <div v-for="(equipment, eqIndex) in step.equipments" :key="eqIndex" class="equipment-item">
                <el-row :gutter="15" class="equipment-row">
                  <el-col :span="6">
                    <el-form-item label="设备：">
                      <el-select v-model="equipment.name" placeholder="请选择设备" style="width: 100%">
                        <el-option label="BJG-X400E自动磨光装设备" value="BJG-X400E自动磨光装设备" />
                        <el-option label="BJG-L105自动磨光装设备" value="BJG-L105自动磨光装设备" />
                        <el-option label="手动抛光设备" value="手动抛光设备" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="4">
                    <el-form-item label="加工时间：">
                      <el-input v-model="equipment.processingTime" placeholder="加工时间" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="2">
                    <el-button icon="Plus" @click="addEquipment(stepIndex)" v-if="eqIndex === step.equipments.length - 1" />
                    <el-button icon="Minus" @click="removeEquipment(stepIndex, eqIndex)" v-if="step.equipments.length > 1" />
                  </el-col>
                </el-row>

                <!-- 磨料配置 -->
                <el-row :gutter="15" class="material-row">
                  <el-col :span="6">
                    <el-form-item label="磨料：">
                      <el-select v-model="equipment.abrasive" placeholder="请选择磨料" style="width: 100%">
                        <el-option label="3号白磁磨料" value="3号白磁磨料" />
                        <el-option label="3号中硬磨料块" value="3号中硬磨料块" />
                        <el-option label="陶瓷磨料" value="陶瓷磨料" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="2">
                    <el-button icon="Plus" @click="addAbrasive(stepIndex, eqIndex)" />
                  </el-col>
                </el-row>

                <!-- 添加剂配置 -->
                <el-row :gutter="15" class="additive-row">
                  <el-col :span="6">
                    <el-form-item label="添加剂：">
                      <el-select v-model="equipment.additive" placeholder="请选择添加剂" style="width: 100%">
                        <el-option label="硅脂液" value="硅脂液" />
                        <el-option label="HYF" value="HYF" />
                        <el-option label="清洁剂" value="清洁剂" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="2">
                    <el-button icon="Plus" @click="addAdditive(stepIndex, eqIndex)" />
                  </el-col>
                </el-row>

                <!-- 试验结果 -->
                <div class="test-results">
                  <h5>试验结果：</h5>
                  <div v-for="(result, resultIndex) in equipment.testResults" :key="resultIndex" class="test-result-item">
                    <el-row :gutter="10">
                      <el-col :span="4">
                        <el-select v-model="result.type" placeholder="表面粗糙度(Ra)" style="width: 100%">
                          <el-option label="表面粗糙度(Ra)" value="表面粗糙度(Ra)" />
                          <el-option label="平行度" value="平行度" />
                          <el-option label="垂直度" value="垂直度" />
                        </el-select>
                      </el-col>
                      <el-col :span="3">
                        <el-input v-model="result.location" placeholder="叶片" />
                      </el-col>
                      <el-col :span="3">
                        <el-input v-model="result.value" placeholder="0.152" />
                      </el-col>
                      <el-col :span="2">
                        <el-button icon="Plus" @click="addTestResult(stepIndex, eqIndex)" v-if="resultIndex === equipment.testResults.length - 1" />
                        <el-button icon="Minus" @click="removeTestResult(stepIndex, eqIndex, resultIndex)" v-if="equipment.testResults.length > 1" />
                      </el-col>
                    </el-row>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="step-actions">
            <el-button type="primary" @click="addProcessStep">添加工步</el-button>
          </div>
        </div>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showProcessDialog = false">取消</el-button>
          <el-button @click="saveAsDraft">暂存</el-button>
          <el-button type="primary" @click="submitProcess">提交</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 工艺列表 -->
    <div class="process-list">
      <el-table :data="processList" style="width: 100%" stripe>
        <el-table-column prop="batchNumber" label="生产批量" width="120" />
        <el-table-column prop="quantity" label="数量" width="80" />
        <el-table-column prop="stepsCount" label="工步数量" width="100" />
        <el-table-column prop="createTime" label="创建时间" width="160" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === '已提交' ? 'success' : 'warning'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editProcess(scope.row)">编辑</el-button>
            <el-button type="success" size="small" @click="viewProcess(scope.row)">查看</el-button>
            <el-button type="danger" size="small" @click="deleteProcess(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'

// 响应式数据
const showProcessDialog = ref(false)
const processFormRef = ref<FormInstance>()
const uploadedFiles = ref([])
const workpieceRequirementType = ref('表面粗糙度(Ra)')

// 工艺数据结构
const processData = reactive({
  batchNumber: '',
  quantity: '',
  checkValue: '',
  requirementValue: '',
  specialProtection: '',
  workpieceSpecialReq: '',
  others: '',
  processSteps: [
    {
      stepNumber: 1,
      equipments: [
        {
          name: '',
          processingTime: '',
          abrasive: '',
          additive: '',
          testResults: [
            {
              type: '表面粗糙度(Ra)',
              location: '',
              value: ''
            }
          ]
        }
      ]
    }
  ]
})

// 工艺列表数据
const processList = ref([
  {
    id: 1,
    batchNumber: 's001',
    quantity: '3',
    stepsCount: 2,
    createTime: '2024-01-15 14:30',
    status: '已提交'
  },
  {
    id: 2,
    batchNumber: 's002',
    quantity: '5',
    stepsCount: 1,
    createTime: '2024-01-14 10:20',
    status: '暂存'
  }
])

// 方法定义
const refreshData = () => {
  ElMessage.success('数据已刷新')
}

const exportData = () => {
  ElMessage.info('导出功能开发中')
}

const addWorkpieceRequirement = () => {
  ElMessage.info('添加工件要求')
}

const handleFileChange = (file: any) => {
  uploadedFiles.value.push(file)
  ElMessage.success('文件已选择')
}

const startUpload = () => {
  ElMessage.success('文件上传成功')
}

const removeFile = (index: number) => {
  uploadedFiles.value.splice(index, 1)
  ElMessage.info('文件已删除')
}

const addProcessStep = () => {
  const newStepNumber = processData.processSteps.length + 1
  processData.processSteps.push({
    stepNumber: newStepNumber,
    equipments: [
      {
        name: '',
        processingTime: '',
        abrasive: '',
        additive: '',
        testResults: [
          {
            type: '表面粗糙度(Ra)',
            location: '',
            value: ''
          }
        ]
      }
    ]
  })
  ElMessage.success(`已添加工步 ${newStepNumber}`)
}

const removeProcessStep = (stepIndex: number) => {
  processData.processSteps.splice(stepIndex, 1)
  // 重新编号
  processData.processSteps.forEach((step, index) => {
    step.stepNumber = index + 1
  })
  ElMessage.success('工步已删除')
}

const addEquipment = (stepIndex: number) => {
  processData.processSteps[stepIndex].equipments.push({
    name: '',
    processingTime: '',
    abrasive: '',
    additive: '',
    testResults: [
      {
        type: '表面粗糙度(Ra)',
        location: '',
        value: ''
      }
    ]
  })
  ElMessage.success('已添加设备')
}

const removeEquipment = (stepIndex: number, eqIndex: number) => {
  processData.processSteps[stepIndex].equipments.splice(eqIndex, 1)
  ElMessage.success('设备已删除')
}

const addAbrasive = (stepIndex: number, eqIndex: number) => {
  ElMessage.info('添加磨料配置')
}

const addAdditive = (stepIndex: number, eqIndex: number) => {
  ElMessage.info('添加添加剂配置')
}

const addTestResult = (stepIndex: number, eqIndex: number) => {
  processData.processSteps[stepIndex].equipments[eqIndex].testResults.push({
    type: '表面粗糙度(Ra)',
    location: '',
    value: ''
  })
  ElMessage.success('已添加试验结果')
}

const removeTestResult = (stepIndex: number, eqIndex: number, resultIndex: number) => {
  processData.processSteps[stepIndex].equipments[eqIndex].testResults.splice(resultIndex, 1)
  ElMessage.success('试验结果已删除')
}

const saveAsDraft = () => {
  ElMessage.success('工艺已暂存')
}

const submitProcess = () => {
  // 这里可以添加表单验证
  ElMessage.success('工艺提交成功')
  showProcessDialog.value = false
}

const editProcess = (row: any) => {
  ElMessage.info(`编辑工艺：${row.batchNumber}`)
  showProcessDialog.value = true
}

const viewProcess = (row: any) => {
  ElMessage.info(`查看工艺：${row.batchNumber}`)
}

const deleteProcess = (row: any) => {
  ElMessageBox.confirm('确定要删除这个工艺吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    const index = processList.value.findIndex(item => item.id === row.id)
    if (index !== -1) {
      processList.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  }).catch(() => {
    ElMessage.info('已取消删除')
  })
}

onMounted(() => {
  console.log('光整工艺录入(管理员)页面已加载')
})
</script>

<style scoped>
.process-entry-admin-view {
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
  color: #e74c3c;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.process-form {
  max-height: 70vh;
  overflow-y: auto;
  padding-right: 12px;
}

.form-section {
  margin-bottom: 32px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 20px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #e9ecef;
}

.process-step {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid #e9ecef;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e9ecef;
}

.step-header h4 {
  margin: 0;
  color: #495057;
  font-size: 16px;
  font-weight: 600;
}

.equipment-section {
  margin-top: 15px;
}

.equipment-item {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 15px;
  border: 1px solid #dee2e6;
}

.equipment-row,
.material-row,
.additive-row {
  margin-bottom: 10px;
}

.test-results {
  margin-top: 15px;
  padding: 15px;
  background: #fff;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.test-results h5 {
  margin: 0 0 15px 0;
  color: #495057;
  font-size: 14px;
  font-weight: 600;
}

.test-result-item {
  margin-bottom: 10px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
}

.step-actions {
  text-align: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 2px dashed #dee2e6;
}

.file-upload-area {
  background: #f8f9fa;
  border: 2px dashed #dee2e6;
  border-radius: 6px;
  padding: 20px;
  text-align: center;
}

.file-list {
  margin-top: 15px;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: white;
  border-radius: 4px;
  margin-bottom: 8px;
  border: 1px solid #dee2e6;
}

.process-list {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dialog-footer {
  text-align: right;
}

:deep(.el-dialog__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px 24px;
  border-radius: 8px 8px 0 0;
}

:deep(.el-dialog__title) {
  color: white;
  font-size: 18px;
  font-weight: 600;
}

:deep(.el-dialog__headerbtn .el-dialog__close) {
  color: white;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #495057;
}

@media (max-width: 768px) {
  .process-entry-admin-view {
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
  
  .process-form {
    max-height: 60vh;
  }
  
  .form-section {
    padding: 15px;
  }
  
  .process-step {
    padding: 15px;
  }
}
</style> 