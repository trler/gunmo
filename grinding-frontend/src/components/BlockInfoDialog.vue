<template>
  <el-dialog
    v-model="dialogVisible"
    title="磨块信息维护"
    width="900px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="120px"
      class="block-form"
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="磨块编号" prop="blockNo">
            <el-input v-model="formData.blockNo" placeholder="请输入磨块编号" />
          </el-form-item>
          <el-form-item label="磨块类型" prop="blockType">
            <el-select v-model="formData.blockType" placeholder="请选择磨块类型" style="width: 100%">
              <el-option
                v-for="type in blockTypes"
                :key="type.value"
                :label="type.label"
                :value="type.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="磨块厂家" prop="blockFactory">
            <el-select v-model="formData.blockFactory" placeholder="请选择磨块厂家" style="width: 100%">
              <el-option
                v-for="factory in factories"
                :key="factory.value"
                :label="factory.label"
                :value="factory.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="磨块规格" prop="blockSpec">
            <el-input v-model="formData.blockSpec" placeholder="请输入磨块规格" />
          </el-form-item>
          <el-form-item label="磨块颜色" prop="blockColor">
            <el-select v-model="formData.blockColor" placeholder="请选择磨块颜色" style="width: 100%">
              <el-option
                v-for="color in colors"
                :key="color.value"
                :label="color.label"
                :value="color.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="磨耗率" prop="wearRate">
            <el-input v-model="formData.wearRate" placeholder="请输入磨耗率">
              <template #append>%</template>
            </el-input>
          </el-form-item>
          <el-form-item label="批次" prop="batch">
            <el-input v-model="formData.batch" placeholder="请输入批次号" />
          </el-form-item>
          <el-form-item label="特征信息1" prop="feature1">
            <el-input v-model="formData.feature1" placeholder="请输入特征信息1" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="磨块名称" prop="blockName">
            <el-input v-model="formData.blockName" placeholder="请输入磨块名称" />
          </el-form-item>
          <el-form-item label="磨块牌号" prop="blockBrand">
            <el-input v-model="formData.blockBrand" placeholder="请输入磨块牌号" />
          </el-form-item>
          <el-form-item label="磨块形状" prop="blockShape">
            <el-select v-model="formData.blockShape" placeholder="请选择磨块形状" style="width: 100%">
              <el-option
                v-for="shape in shapes"
                :key="shape.value"
                :label="shape.label"
                :value="shape.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="磨块材质" prop="blockMaterial">
            <el-select v-model="formData.blockMaterial" placeholder="请选择磨块材质" style="width: 100%">
              <el-option
                v-for="material in materials"
                :key="material.value"
                :label="material.label"
                :value="material.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="重量" prop="weight">
            <el-input v-model="formData.weight" placeholder="请输入重量">
              <template #append>g</template>
            </el-input>
          </el-form-item>
          <el-form-item label="磨削率" prop="grindingRate">
            <el-input v-model="formData.grindingRate" placeholder="请输入磨削率">
              <template #append>%</template>
            </el-input>
          </el-form-item>
          <el-form-item label="备注" prop="remark">
            <el-input
              v-model="formData.remark"
              type="textarea"
              :rows="2"
              placeholder="请输入备注信息"
            />
          </el-form-item>
          <el-form-item label="特征信息2" prop="feature2">
            <el-input v-model="formData.feature2" placeholder="请输入特征信息2" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="图片上传" prop="images">
        <el-upload
          class="block-upload"
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
              支持 jpg/png 格式，单个文件大小不超过 500KB
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

export interface BlockFormData {
  id?: number
  blockNo: string
  blockName: string
  blockType: string
  blockBrand: string
  blockFactory: string
  blockShape: string
  blockSpec: string
  blockMaterial: string
  blockColor: string
  weight: string
  wearRate: string
  grindingRate: string
  batch: string
  remark: string
  feature1: string
  feature2: string
  images: string[]
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
  (e: 'submit', data: BlockFormData): void
}>()

// 对话框可见性
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 表单引用
const formRef = ref<FormInstance>()

// 表单数据
const formData = reactive<BlockFormData>({
  blockNo: '',
  blockName: '',
  blockType: '',
  blockBrand: '',
  blockFactory: '',
  blockShape: '',
  blockSpec: '',
  blockMaterial: '',
  blockColor: '',
  weight: '',
  wearRate: '',
  grindingRate: '',
  batch: '',
  remark: '',
  feature1: '',
  feature2: '',
  images: []
})

// 文件列表
const fileList = ref<UploadFile[]>([])

// 提交状态
const submitting = ref(false)

// 表单验证规则
const rules: FormRules = {
  blockNo: [
    { required: true, message: '请输入磨块编号', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  blockName: [
    { required: true, message: '请输入磨块名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  blockType: [
    { required: true, message: '请选择磨块类型', trigger: 'change' }
  ],
  blockFactory: [
    { required: true, message: '请选择磨块厂家', trigger: 'change' }
  ],
  blockShape: [
    { required: true, message: '请选择磨块形状', trigger: 'change' }
  ],
  blockMaterial: [
    { required: true, message: '请选择磨块材质', trigger: 'change' }
  ],
  blockColor: [
    { required: true, message: '请选择磨块颜色', trigger: 'change' }
  ],
  weight: [
    { pattern: /^\d+(\.\d{1,2})?$/, message: '请输入有效的重量数值', trigger: 'blur' }
  ],
  wearRate: [
    { pattern: /^\d+(\.\d{1,2})?$/, message: '请输入有效的磨耗率', trigger: 'blur' }
  ],
  grindingRate: [
    { pattern: /^\d+(\.\d{1,2})?$/, message: '请输入有效的磨削率', trigger: 'blur' }
  ]
}

// 下拉选项数据
const blockTypes: SelectOption[] = [
  { value: 'white_alumina', label: '白刚玉磨料' },
  { value: 'brown_alumina', label: '棕刚玉磨料' },
  { value: 'silicon_carbide', label: '碳化硅磨料' }
]

const factories: SelectOption[] = [
  { value: 'factory_a', label: '厂家A' },
  { value: 'factory_b', label: '厂家B' },
  { value: 'factory_c', label: '厂家C' }
]

const shapes: SelectOption[] = [
  { value: 'spherical', label: '圆球形' },
  { value: 'cylindrical', label: '圆柱形' },
  { value: 'triangular', label: '三角形' }
]

const materials: SelectOption[] = [
  { value: 'WA', label: 'WA' },
  { value: 'A', label: 'A' },
  { value: 'C', label: 'C' }
]

const colors: SelectOption[] = [
  { value: 'green', label: '绿色' },
  { value: 'red', label: '红色' },
  { value: 'blue', label: '蓝色' }
]

// 文件上传前的验证
const beforeFileUpload = (file: File) => {
  const isImage = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt500K = file.size / 1024 < 500

  if (!isImage) {
    ElMessage.error('只能上传 JPG/PNG 格式的图片！')
    return false
  }
  if (!isLt500K) {
    ElMessage.error('图片大小不能超过 500KB！')
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
      images: fileList.value.map(file => file.url || '')
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
.block-form {
  padding: 20px;
}

.block-upload {
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