<template>
  <el-dialog
    v-model="dialogVisible"
    title="滚磨设备信息维护"
    width="900px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="120px"
      class="equipment-form"
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="设备编号" prop="deviceNo">
            <el-input v-model="formData.deviceNo" placeholder="请输入设备编号" />
          </el-form-item>
          <el-form-item label="设备类型" prop="deviceType">
            <el-select v-model="formData.deviceType" placeholder="请选择设备类型" style="width: 100%">
              <el-option
                v-for="type in deviceTypes"
                :key="type.value"
                :label="type.label"
                :value="type.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="设备厂家" prop="deviceFactory">
            <el-select v-model="formData.deviceFactory" placeholder="请选择设备厂家" style="width: 100%">
              <el-option
                v-for="factory in factories"
                :key="factory.value"
                :label="factory.label"
                :value="factory.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="设备规格" prop="deviceSpec">
            <el-input v-model="formData.deviceSpec" placeholder="请输入设备规格" />
          </el-form-item>
          <el-form-item label="出厂日期" prop="manufactureDate">
            <el-date-picker
              v-model="formData.manufactureDate"
              type="date"
              placeholder="选择出厂日期"
              style="width: 100%"
            />
          </el-form-item>
          <el-form-item label="额定功率" prop="ratedPower">
            <el-input v-model="formData.ratedPower" placeholder="请输入额定功率">
              <template #append>kW</template>
            </el-input>
          </el-form-item>
          <el-form-item label="特征信息1" prop="feature1">
            <el-input v-model="formData.feature1" placeholder="请输入特征信息1" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="设备名称" prop="deviceName">
            <el-input v-model="formData.deviceName" placeholder="请输入设备名称" />
          </el-form-item>
          <el-form-item label="设备型号" prop="deviceModel">
            <el-input v-model="formData.deviceModel" placeholder="请输入设备型号" />
          </el-form-item>
          <el-form-item label="设备状态" prop="deviceStatus">
            <el-select v-model="formData.deviceStatus" placeholder="请选择设备状态" style="width: 100%">
              <el-option
                v-for="status in statuses"
                :key="status.value"
                :label="status.label"
                :value="status.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="生产厂家" prop="manufacturer">
            <el-input v-model="formData.manufacturer" placeholder="请输入生产厂家" />
          </el-form-item>
          <el-form-item label="转速范围" prop="speedRange">
            <el-input v-model="formData.speedRange" placeholder="请输入转速范围">
              <template #append>rpm</template>
            </el-input>
          </el-form-item>
          <el-form-item label="重量" prop="weight">
            <el-input v-model="formData.weight" placeholder="请输入重量">
              <template #append>kg</template>
            </el-input>
          </el-form-item>
          <el-form-item label="特征信息2" prop="feature2">
            <el-input v-model="formData.feature2" placeholder="请输入特征信息2" />
          </el-form-item>
          <el-form-item label="备注" prop="remark">
            <el-input
              v-model="formData.remark"
              type="textarea"
              :rows="2"
              placeholder="请输入备注信息"
            />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="文件上传" prop="files">
        <el-upload
          class="equipment-upload"
          action="/api/upload"
          :auto-upload="false"
          :on-change="handleFileChange"
          :on-remove="handleFileRemove"
          :before-upload="beforeFileUpload"
          :file-list="fileList"
          multiple
          :limit="5"
          list-type="picture-card"
        >
          <el-icon><Plus /></el-icon>
          <template #tip>
            <div class="el-upload__tip">
              支持 jpg/png/pdf 格式，单个文件大小不超过 1MB
            </div>
          </template>
        </el-upload>
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">关闭</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ submitting ? '提交中...' : '确认' }}
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed, defineProps, defineEmits } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type UploadFile } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import type { FormRules } from 'element-plus'

export interface EquipmentFormData {
  id?: number
  deviceNo: string
  deviceName: string
  deviceType: string
  deviceModel: string
  deviceFactory: string
  deviceStatus: string
  deviceSpec: string
  manufacturer: string
  manufactureDate: string
  ratedPower: string
  speedRange: string
  weight: string
  remark: string
  feature1: string
  feature2: string
  files: string[]
}

interface SelectOption {
  value: string
  label: string
}

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'submit', data: EquipmentFormData): void
}>()

// 对话框可见性
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 表单引用
const formRef = ref<FormInstance>()

// 表单数据
const formData = reactive<EquipmentFormData>({
  deviceNo: '',
  deviceName: '',
  deviceType: '',
  deviceModel: '',
  deviceFactory: '',
  deviceStatus: '',
  deviceSpec: '',
  manufacturer: '',
  manufactureDate: '',
  ratedPower: '',
  speedRange: '',
  weight: '',
  remark: '',
  feature1: '',
  feature2: '',
  files: []
})

// 文件列表
const fileList = ref<UploadFile[]>([])

// 提交状态
const submitting = ref(false)

// 表单验证规则
const rules: FormRules = {
  deviceNo: [
    { required: true, message: '请输入设备编号', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  deviceName: [
    { required: true, message: '请输入设备名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  deviceType: [
    { required: true, message: '请选择设备类型', trigger: 'change' }
  ],
  deviceFactory: [
    { required: true, message: '请选择设备厂家', trigger: 'change' }
  ],
  deviceStatus: [
    { required: true, message: '请选择设备状态', trigger: 'change' }
  ],
  ratedPower: [
    { pattern: /^\d+(\.\d{1,2})?$/, message: '请输入有效的功率数值', trigger: 'blur' }
  ],
  weight: [
    { pattern: /^\d+(\.\d{1,2})?$/, message: '请输入有效的重量数值', trigger: 'blur' }
  ]
}

// 下拉选项数据
const deviceTypes: SelectOption[] = [
  { value: 'horizontal', label: '卧式滚磨机' },
  { value: 'vertical', label: '立式滚磨机' },
  { value: 'vibratory', label: '振动滚磨机' }
]

const factories: SelectOption[] = [
  { value: 'factory_a', label: '厂家A' },
  { value: 'factory_b', label: '厂家B' },
  { value: 'factory_c', label: '厂家C' }
]

const statuses: SelectOption[] = [
  { value: 'normal', label: '正常' },
  { value: 'maintenance', label: '维修中' },
  { value: 'scrapped', label: '报废' }
]

// 文件上传前的验证
const beforeFileUpload = (file: File) => {
  const isValidType = ['image/jpeg', 'image/png', 'application/pdf'].includes(file.type)
  const isLt1M = file.size / 1024 / 1024 < 1

  if (!isValidType) {
    ElMessage.error('只能上传 JPG/PNG/PDF 格式的文件！')
    return false
  }
  if (!isLt1M) {
    ElMessage.error('文件大小不能超过 1MB！')
    return false
  }
  return true
}

// 文件状态改变时的钩子
const handleFileChange = (file: UploadFile) => {
  console.log('文件状态改变:', file)
}

// 移除文件时的钩子
const handleFileRemove = (file: UploadFile) => {
  console.log('移除文件:', file)
}

// 关闭对话框
const handleClose = () => {
  ElMessageBox.confirm('确认关闭？未保存的数据将会丢失', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    dialogVisible.value = false
    resetForm()
  }).catch(() => {})
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  fileList.value = []
  submitting.value = false
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    submitting.value = true
    
    // 构建提交数据
    const submitData = {
      ...formData,
      files: fileList.value.map(file => file.url || '')
    }
    
    // 触发提交事件
    emit('submit', submitData)
    
    // 模拟提交延迟
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('保存成功')
    dialogVisible.value = false
    resetForm()
  } catch (error) {
    console.error('表单验证失败:', error)
    ElMessage.error('请检查表单填写是否正确')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.equipment-form {
  padding: 20px;
}

.equipment-upload {
  width: 100%;
}

:deep(.el-upload--picture-card) {
  width: 120px;
  height: 120px;
  line-height: 120px;
}

:deep(.el-upload-list--picture-card .el-upload-list__item) {
  width: 120px;
  height: 120px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.el-upload__tip {
  color: #909399;
  font-size: 12px;
  margin-top: 8px;
}
</style> 