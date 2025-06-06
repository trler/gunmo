<template>
  <el-dialog
    :title="chemical ? '编辑化学剂' : '新增化学剂'"
    v-model="dialogVisible"
    width="800px"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="chemical-form"
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <!-- 左栏：基本信息 -->
          <el-form-item label="化学剂编号" prop="code">
            <el-input v-model="form.code" placeholder="唯一标识（如CH-2024-001）" />
          </el-form-item>
          <el-form-item label="化学剂名称" prop="name">
            <el-input v-model="form.name" placeholder="如：防锈切削液" />
          </el-form-item>
          <el-form-item label="类型" prop="type">
            <el-select v-model="form.type" placeholder="选择类型">
              <el-option
                v-for="type in chemicalTypes"
                :key="type.value"
                :label="type.label"
                :value="type.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="生产厂家" prop="manufacturer">
            <el-input v-model="form.manufacturer" placeholder="输入生产厂家" />
          </el-form-item>
          <el-form-item label="有效期" prop="expiry_date">
            <el-date-picker
              v-model="form.expiry_date"
              type="date"
              placeholder="选择有效期截止日期"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <!-- 右栏：理化参数 -->
          <el-form-item label="主要成分" prop="components">
            <el-input
              v-model="form.components"
              type="textarea"
              :rows="2"
              placeholder="如：水基、防锈剂、表面活性剂"
            />
          </el-form-item>
          <el-form-item label="PH值范围" prop="ph_range">
            <el-input v-model="form.ph_range" placeholder="如：7.5-8.5" />
          </el-form-item>
          <el-form-item label="密度" prop="density">
            <el-input-number
              v-model="form.density"
              :precision="2"
              :step="0.1"
              :min="0"
              placeholder="单位：g/cm³"
            />
          </el-form-item>
          <el-form-item label="闪点" prop="flash_point">
            <el-input v-model="form.flash_point" placeholder="单位：℃（如≥60）" />
          </el-form-item>
          <el-form-item label="安全等级" prop="safety_level">
            <el-select v-model="form.safety_level" placeholder="选择等级">
              <el-option label="低风险" value="low" />
              <el-option label="中风险" value="medium" />
              <el-option label="高风险" value="high" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="24">
          <!-- 文件上传 -->
          <el-form-item label="MSDS文件" prop="msds_file">
            <el-upload
              class="upload-demo"
              :action="uploadAction"
              :headers="uploadHeaders"
              :file-list="msdsFileList"
              :before-upload="beforeUpload"
              :on-success="(res) => handleUploadSuccess(res, 'msds')"
              :on-remove="(file) => handleRemove(file, 'msds')"
              :limit="1"
            >
              <el-button type="primary">选择文件</el-button>
              <template #tip>
                <div class="el-upload__tip">
                  支持PDF、DOC格式，单文件≤1MB
                </div>
              </template>
            </el-upload>
          </el-form-item>

          <el-form-item label="配方文件" prop="formula_file">
            <el-upload
              class="upload-demo"
              :action="uploadAction"
              :headers="uploadHeaders"
              :file-list="formulaFileList"
              :before-upload="beforeUpload"
              :on-success="(res) => handleUploadSuccess(res, 'formula')"
              :on-remove="(file) => handleRemove(file, 'formula')"
              :limit="1"
            >
              <el-button type="primary">选择文件</el-button>
              <template #tip>
                <div class="el-upload__tip">
                  支持PDF、DOC格式，单文件≤1MB
                </div>
              </template>
            </el-upload>
          </el-form-item>

          <el-form-item label="备注" prop="remark">
            <el-input
              v-model="form.remark"
              type="textarea"
              :rows="2"
              placeholder="其他补充说明"
            />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" :loading="loading" @click="handleSubmit">
        确定
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import type { FormInstance, UploadProps, FormItemRule } from 'element-plus'
import { ElMessage } from 'element-plus'
import { useChemicalStore } from '@/stores/chemical'
import type { Chemical, ChemicalType } from '@/stores/chemical'
import axiosInstance from '@/api/axios'

const props = defineProps<{
  modelValue: boolean
  chemical: Chemical | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'success'): void
}>()

const chemicalStore = useChemicalStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

// 对话框可见性
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 表单数据
const form = reactive({
  code: '',
  name: '',
  type: undefined as ChemicalType | undefined,
  manufacturer: '',
  components: '',
  ph_range: '',
  density: 0,
  flash_point: '',
  safety_level: 'low' as const,
  expiry_date: '',
  msds_file: '',
  formula_file: '',
  remark: ''
})

// 文件列表
const msdsFileList = ref<UploadProps['fileList']>([])
const formulaFileList = ref<UploadProps['fileList']>([])

// 上传相关
const uploadAction = `${axiosInstance.defaults.baseURL}/equipment/chemicals/upload/`
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${localStorage.getItem('token')}`
}))

// 化学剂类型选项
const chemicalTypes = [
  { value: 'cutting_fluid', label: '切削液' },
  { value: 'cleaning_agent', label: '清洗剂' },
  { value: 'rust_preventive', label: '防锈剂' },
  { value: 'lubricant', label: '润滑剂' },
  { value: 'passivator', label: '钝化剂' }
]

// 表单验证规则
const rules: Record<string, FormItemRule[]> = {
  code: [
    { required: true, message: '请输入化学剂编号', trigger: 'blur' },
    { pattern: /^[A-Za-z0-9-]+$/, message: '编号只能包含字母、数字和连字符', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入化学剂名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择化学剂类型', trigger: 'change' }
  ],
  manufacturer: [
    { required: true, message: '请输入生产厂家', trigger: 'blur' }
  ],
  components: [
    { required: true, message: '请输入主要成分', trigger: 'blur' }
  ],
  ph_range: [
    { required: true, message: '请输入PH值范围', trigger: 'blur' },
    { pattern: /^\d+(\.\d+)?-\d+(\.\d+)?$/, message: '请输入正确的PH值范围（如：7.5-8.5）', trigger: 'blur' }
  ],
  density: [
    { required: true, message: '请输入密度', trigger: 'blur' },
    { type: 'number', min: 0, message: '密度必须大于0', trigger: 'blur' }
  ],
  flash_point: [
    { required: true, message: '请输入闪点', trigger: 'blur' }
  ],
  safety_level: [
    { required: true, message: '请选择安全等级', trigger: 'change' }
  ],
  expiry_date: [
    { required: true, message: '请选择有效期', trigger: 'change' }
  ]
}

// 监听编辑数据
watch(() => props.chemical, (newVal) => {
  if (newVal) {
    Object.assign(form, newVal)
    // 设置文件列表
    if (newVal.msds_file_url) {
      msdsFileList.value = [{
        name: 'MSDS文件',
        url: newVal.msds_file_url
      }]
    }
    if (newVal.formula_file_url) {
      formulaFileList.value = [{
        name: '配方文件',
        url: newVal.formula_file_url
      }]
    }
  } else {
    resetForm()
  }
}, { immediate: true })

// 文件上传前验证
const beforeUpload: UploadProps['beforeUpload'] = (file) => {
  const isPDF = file.type === 'application/pdf'
  const isDOC = file.type === 'application/msword' || file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  const isSizeValid = file.size <= 1024 * 1024

  if (!isPDF && !isDOC) {
    ElMessage.error('只能上传PDF或Word文档！')
    return false
  }
  if (!isSizeValid) {
    ElMessage.error('文件大小不能超过1MB！')
    return false
  }
  return true
}

// 文件上传成功处理
const handleUploadSuccess = (response: any, type: 'msds' | 'formula') => {
  if (response.url) {
    form[type === 'msds' ? 'msds_file' : 'formula_file'] = response.url
    ElMessage.success('文件上传成功')
  } else {
    ElMessage.error('文件上传失败')
  }
}

// 文件移除处理
const handleRemove = (file: UploadProps['fileList'][0], type: 'msds' | 'formula') => {
  form[type === 'msds' ? 'msds_file' : 'formula_file'] = ''
}

// 表单提交
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true

    const formData = new FormData()
    Object.entries(form).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        formData.append(key, value.toString())
      }
    })

    if (props.chemical) {
      await chemicalStore.updateChemical(props.chemical.id, formData)
      ElMessage.success('更新成功')
    } else {
      await chemicalStore.createChemical(formData)
      ElMessage.success('创建成功')
    }

    emit('success')
  } catch (error) {
    console.error('表单提交失败:', error)
  } finally {
    loading.value = false
  }
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  form.code = ''
  form.name = ''
  form.type = undefined
  form.manufacturer = ''
  form.components = ''
  form.ph_range = ''
  form.density = 0
  form.flash_point = ''
  form.safety_level = 'low'
  form.expiry_date = ''
  form.msds_file = ''
  form.formula_file = ''
  form.remark = ''
  msdsFileList.value = []
  formulaFileList.value = []
}

// 关闭对话框
const handleClose = () => {
  resetForm()
  dialogVisible.value = false
}
</script>

<style scoped>
.chemical-form {
  max-height: 70vh;
  overflow-y: auto;
  padding-right: 20px;
}

.upload-demo {
  margin-bottom: 20px;
}

:deep(.el-upload__tip) {
  line-height: 1.2;
  margin-top: 5px;
}
</style> 