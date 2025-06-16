<template>
  <div class="requirement-entry-view">
    <div class="page-header">
      <h1 class="page-title">
        <i class="fas fa-edit"></i>
        光整需求录入
      </h1>
      <div class="header-actions">
        <el-button type="primary" icon="Plus" @click="showAddDialog = true">添加</el-button>
        <el-button icon="Refresh" @click="refreshData">刷新</el-button>
      </div>
    </div>

    <!-- 添加/编辑对话框 -->
    <el-dialog 
      v-model="showAddDialog" 
      :title="editingItem ? '编辑工件信息' : '添加工件信息'"
      width="80%"
      top="5vh"
      :close-on-click-modal="false"
    >
      <el-form 
        ref="formRef" 
        :model="formData" 
        :rules="formRules" 
        label-width="120px"
        class="requirement-form"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="工件名称：" prop="workpieceName">
              <el-input v-model="formData.workpieceName" placeholder="请输入工件名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属部件：" prop="component">
              <el-input v-model="formData.component" placeholder="请输入所属部件" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="设备名称：" prop="equipmentName">
              <el-input v-model="formData.equipmentName" placeholder="请输入设备名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="材质：" prop="material">
              <el-select v-model="formData.material" placeholder="请选择材质" style="width: 100%">
                <el-option label="钛合金" value="钛合金" />
                <el-option label="不锈钢" value="不锈钢" />
                <el-option label="铝合金" value="铝合金" />
                <el-option label="碳钢" value="碳钢" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="代号：" prop="code">
              <el-select v-model="formData.code" placeholder="请选择代号" style="width: 100%">
                <el-option label="sylm201908" value="sylm201908" />
                <el-option label="sylm201909" value="sylm201909" />
                <el-option label="sylm201910" value="sylm201910" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="热处理：" prop="heatTreatment">
              <el-select v-model="formData.heatTreatment" placeholder="请选择热处理" style="width: 100%">
                <el-option label="热处理" value="热处理" />
                <el-option label="退火" value="退火" />
                <el-option label="淬火" value="淬火" />
                <el-option label="回火" value="回火" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="牌号：" prop="grade">
              <el-select v-model="formData.grade" placeholder="请选择牌号" style="width: 100%">
                <el-option label="硬度" value="硬度" />
                <el-option label="TC4" value="TC4" />
                <el-option label="TA2" value="TA2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结构尺寸：" prop="structuralSize">
              <el-select v-model="formData.structuralSize" placeholder="请选择结构尺寸" style="width: 100%">
                <el-option label="方形结构" value="方形结构" />
                <el-option label="圆形结构" value="圆形结构" />
                <el-option label="异形结构" value="异形结构" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="尺寸：">
          <el-row :gutter="10">
            <el-col :span="8">
              <el-input-group>
                <el-select v-model="lengthUnit" slot="prepend" style="width: 80px">
                  <el-option label="长(mm)" value="长(mm)" />
                </el-select>
                <el-input v-model="formData.length" placeholder="110">
                  <template #append>
                    <el-button icon="Plus" @click="addLength" />
                  </template>
                </el-input>
              </el-input-group>
            </el-col>
            <el-col :span="8">
              <el-input-group>
                <el-select v-model="widthUnit" slot="prepend" style="width: 80px">
                  <el-option label="宽(mm)" value="宽(mm)" />
                </el-select>
                <el-input v-model="formData.width" placeholder="36">
                  <template #append>
                    <el-button icon="Minus" @click="subtractWidth" />
                  </template>
                </el-input>
              </el-input-group>
            </el-col>
            <el-col :span="8">
              <el-input-group>
                <el-select v-model="thicknessUnit" slot="prepend" style="width: 80px">
                  <el-option label="厚度(mm)" value="厚度(mm)" />
                </el-select>
                <el-input v-model="formData.thickness" placeholder="27">
                  <template #append>
                    <el-button icon="Minus" @click="subtractThickness" />
                  </template>
                </el-input>
              </el-input-group>
            </el-col>
          </el-row>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="重要尺寸：" prop="importantSize">
              <el-select v-model="formData.importantSize" placeholder="请选择重要尺寸" style="width: 100%">
                <el-option label="重要尺寸" value="重要尺寸" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="精度等级：" prop="precisionLevel">
              <el-select v-model="formData.precisionLevel" placeholder="请选择精度等级" style="width: 100%">
                <el-option label="精度等级" value="精度等级" />
                <el-option label="IT6" value="IT6" />
                <el-option label="IT7" value="IT7" />
                <el-option label="IT8" value="IT8" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="生产批量：" prop="batchSize">
              <el-input v-model="formData.batchSize" placeholder="4001" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="数量：" prop="quantity">
              <el-input v-model="formData.quantity" placeholder="3" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="加工要求：">
          <el-row :gutter="10">
            <el-col :span="6">
              <el-select v-model="processingType" placeholder="表面粗糙度(Ra)" style="width: 100%">
                <el-option label="表面粗糙度(Ra)" value="表面粗糙度(Ra)" />
              </el-select>
            </el-col>
            <el-col :span="4">
              <el-input v-model="formData.surfaceRoughness" placeholder="检查值" />
            </el-col>
            <el-col :span="4">
              <el-input v-model="formData.processingValue" placeholder="0.4" />
            </el-col>
            <el-col :span="2">
              <el-button icon="Plus" @click="addProcessingRequirement" />
            </el-col>
          </el-row>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="特殊保护要求：" prop="specialProtection">
              <el-input v-model="formData.specialProtection" placeholder="特殊保护要求" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="工件特殊要求：" prop="specialRequirements">
              <el-input v-model="formData.specialRequirements" placeholder="工件特殊要求" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="其他：" prop="others">
          <el-input 
            v-model="formData.others" 
            type="textarea" 
            :rows="3"
            placeholder="1.注意对比表面刀痕，不能超过：2.要求无去除量过少"
          />
        </el-form-item>

        <el-form-item label="附件：">
          <div class="file-upload-area">
            <el-upload
              class="upload-demo"
              drag
              action="#"
              :on-change="handleFileChange"
              :auto-upload="false"
              accept="image/*"
            >
              <div class="upload-content">
                <div v-if="!uploadedFile">
                  <i class="el-icon-upload"></i>
                  <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                  <div class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
                </div>
                <div v-else class="uploaded-file">
                  <i class="el-icon-document"></i>
                  <span>{{ uploadedFile.name }}</span>
                  <el-button type="text" @click="removeFile">删除</el-button>
                </div>
              </div>
            </el-upload>
          </div>
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showAddDialog = false">关闭</el-button>
          <el-button @click="saveAsDraft">暂存</el-button>
          <el-button type="primary" @click="submitForm">提交</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 数据表格 -->
    <div class="table-container">
      <el-table :data="tableData" style="width: 100%" stripe>
        <el-table-column prop="workpieceName" label="工件名称" width="120" />
        <el-table-column prop="component" label="所属部件" width="120" />
        <el-table-column prop="equipmentName" label="设备名称" width="120" />
        <el-table-column prop="material" label="材质" width="100" />
        <el-table-column prop="code" label="代号" width="120" />
        <el-table-column prop="heatTreatment" label="热处理" width="100" />
        <el-table-column prop="batchSize" label="生产批量" width="100" />
        <el-table-column prop="quantity" label="数量" width="80" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editItem(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteItem(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

// 响应式数据
const showAddDialog = ref(false)
const editingItem = ref(null)
const formRef = ref<FormInstance>()
const uploadedFile = ref(null)

// 尺寸单位
const lengthUnit = ref('长(mm)')
const widthUnit = ref('宽(mm)')
const thicknessUnit = ref('厚度(mm)')
const processingType = ref('表面粗糙度(Ra)')

// 表单数据
const formData = reactive({
  workpieceName: '',
  component: '',
  equipmentName: '',
  material: '',
  code: '',
  heatTreatment: '',
  grade: '',
  structuralSize: '',
  length: '',
  width: '',
  thickness: '',
  importantSize: '',
  precisionLevel: '',
  batchSize: '',
  quantity: '',
  surfaceRoughness: '',
  processingValue: '',
  specialProtection: '',
  specialRequirements: '',
  others: ''
})

// 表单验证规则
const formRules: FormRules = {
  workpieceName: [
    { required: true, message: '请输入工件名称', trigger: 'blur' }
  ],
  equipmentName: [
    { required: true, message: '请输入设备名称', trigger: 'blur' }
  ],
  material: [
    { required: true, message: '请选择材质', trigger: 'change' }
  ]
}

// 表格数据
const tableData = ref([
  {
    id: 1,
    workpieceName: '齿轮片',
    component: '新型部件',
    equipmentName: '设备名称',
    material: '钛合金',
    code: 'sylm201908',
    heatTreatment: '热处理',
    batchSize: '4001',
    quantity: '3'
  }
])

// 方法
const refreshData = () => {
  ElMessage.success('数据已刷新')
}

const addLength = () => {
  const currentValue = parseFloat(formData.length) || 0
  formData.length = (currentValue + 1).toString()
}

const subtractWidth = () => {
  const currentValue = parseFloat(formData.width) || 0
  formData.width = Math.max(0, currentValue - 1).toString()
}

const subtractThickness = () => {
  const currentValue = parseFloat(formData.thickness) || 0
  formData.thickness = Math.max(0, currentValue - 1).toString()
}

const addProcessingRequirement = () => {
  ElMessage.info('添加加工要求')
}

const handleFileChange = (file: any) => {
  if (file.size > 500 * 1024) {
    ElMessage.error('文件大小不能超过500KB')
    return
  }
  uploadedFile.value = file
  ElMessage.success('文件上传成功')
}

const removeFile = () => {
  uploadedFile.value = null
  ElMessage.info('文件已删除')
}

const resetForm = () => {
  Object.keys(formData).forEach(key => {
    formData[key] = ''
  })
  uploadedFile.value = null
}

const saveAsDraft = () => {
  ElMessage.success('已暂存')
}

const submitForm = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    if (editingItem.value) {
      // 编辑模式
      const index = tableData.value.findIndex(item => item.id === editingItem.value.id)
      if (index !== -1) {
        tableData.value[index] = { ...formData, id: editingItem.value.id }
      }
      ElMessage.success('修改成功')
    } else {
      // 新增模式
      const newItem = {
        ...formData,
        id: Date.now()
      }
      tableData.value.push(newItem)
      ElMessage.success('添加成功')
    }
    
    showAddDialog.value = false
    resetForm()
    editingItem.value = null
  } catch (error) {
    ElMessage.error('请检查表单填写是否正确')
  }
}

const editItem = (row: any) => {
  editingItem.value = row
  Object.keys(formData).forEach(key => {
    if (row[key] !== undefined) {
      formData[key] = row[key]
    }
  })
  showAddDialog.value = true
}

const deleteItem = (row: any) => {
  ElMessageBox.confirm('确定要删除这条记录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    const index = tableData.value.findIndex(item => item.id === row.id)
    if (index !== -1) {
      tableData.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  }).catch(() => {
    ElMessage.info('已取消删除')
  })
}

onMounted(() => {
  console.log('光整需求录入页面已加载')
})
</script>

<style scoped>
.requirement-entry-view {
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

.requirement-form {
  max-height: 60vh;
  overflow-y: auto;
  padding-right: 12px;
}

.file-upload-area {
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  padding: 20px;
  text-align: center;
  background-color: #fafafa;
}

.upload-content {
  padding: 20px;
}

.uploaded-file {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.table-container {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dialog-footer {
  text-align: right;
}

.el-input-group {
  width: 100%;
}

:deep(.el-input-group__prepend) {
  background-color: #f5f7fa;
  color: #909399;
  border-right: 1px solid #dcdfe6;
}

:deep(.el-upload-dragger) {
  width: 100%;
  height: auto;
  background-color: transparent;
  border: none;
}

@media (max-width: 768px) {
  .requirement-entry-view {
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
}
</style> 