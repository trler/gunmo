<template>
  <div class="department-management">
    <div class="page-header">
      <h2>部门信息管理</h2>
      <div class="header-actions">
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          添加部门
        </el-button>
      </div>
    </div>

    <div class="search-bar">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input 
            v-model="searchForm.search" 
            placeholder="搜索部门名称、编号" 
            clearable
            @change="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.company" placeholder="所属企业" clearable @change="handleSearch">
            <el-option 
              v-for="company in companies" 
              :key="company.id" 
              :label="company.name" 
              :value="company.id"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.department_type" placeholder="部门类型" clearable @change="handleSearch">
            <el-option label="生产部门" value="production"></el-option>
            <el-option label="技术部门" value="technology"></el-option>
            <el-option label="质量部门" value="quality"></el-option>
            <el-option label="管理部门" value="management"></el-option>
            <el-option label="销售部门" value="sales"></el-option>
            <el-option label="财务部门" value="finance"></el-option>
            <el-option label="人力资源" value="hr"></el-option>
            <el-option label="物流部门" value="logistics"></el-option>
            <el-option label="其他" value="other"></el-option>
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.is_active" placeholder="状态" clearable @change="handleSearch">
            <el-option label="启用" :value="true"></el-option>
            <el-option label="禁用" :value="false"></el-option>
          </el-select>
        </el-col>
      </el-row>
    </div>

    <div class="table-container">
      <el-table 
        :data="tableData" 
        v-loading="loading"
        border
        stripe
        style="width: 100%"
      >
        <el-table-column prop="code" label="部门编号" width="120" />
        <el-table-column prop="name" label="部门名称" min-width="150" />
        <el-table-column prop="company_name" label="所属企业" min-width="150" />
        <el-table-column prop="department_type" label="部门类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getDepartmentTypeTagType(row.department_type)">
              {{ getDepartmentTypeLabel(row.department_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="level" label="部门层级" width="80" />
        <el-table-column prop="manager_name" label="部门负责人" width="120" />
        <el-table-column prop="office_location" label="办公地点" width="150" />
        <el-table-column prop="extension" label="分机号码" width="100" />
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewDetail(row)">查看</el-button>
            <el-button size="small" type="primary" @click="editDepartment(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteDepartment(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 添加/编辑部门对话框 -->
    <el-dialog
      :title="dialogForm.id ? '编辑部门' : '添加部门'"
      v-model="dialogVisible"
      width="60%"
      :before-close="handleCloseDialog"
    >
      <el-form
        ref="formRef"
        :model="dialogForm"
        :rules="formRules"
        label-width="120px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="部门编号" prop="code">
              <el-input v-model="dialogForm.code" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="部门名称" prop="name">
              <el-input v-model="dialogForm.name" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="所属企业" prop="company">
              <el-select v-model="dialogForm.company" style="width: 100%">
                <el-option 
                  v-for="company in companies" 
                  :key="company.id" 
                  :label="company.name" 
                  :value="company.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="部门类型" prop="department_type">
              <el-select v-model="dialogForm.department_type" style="width: 100%">
                <el-option label="生产部门" value="production"></el-option>
                <el-option label="技术部门" value="technology"></el-option>
                <el-option label="质量部门" value="quality"></el-option>
                <el-option label="管理部门" value="management"></el-option>
                <el-option label="销售部门" value="sales"></el-option>
                <el-option label="财务部门" value="finance"></el-option>
                <el-option label="人力资源" value="hr"></el-option>
                <el-option label="物流部门" value="logistics"></el-option>
                <el-option label="其他" value="other"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="上级部门" prop="parent_department">
              <el-select v-model="dialogForm.parent_department" style="width: 100%" clearable>
                <el-option 
                  v-for="dept in departmentOptions" 
                  :key="dept.id" 
                  :label="dept.name" 
                  :value="dept.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="部门层级" prop="level">
              <el-input-number v-model="dialogForm.level" :min="1" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="部门描述" prop="description">
          <el-input v-model="dialogForm.description" type="textarea" :rows="2" />
        </el-form-item>

        <el-form-item label="主要职责" prop="responsibilities">
          <el-input v-model="dialogForm.responsibilities" type="textarea" :rows="3" />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="办公地点" prop="office_location">
              <el-input v-model="dialogForm.office_location" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="分机号码" prop="extension">
              <el-input v-model="dialogForm.extension" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="部门邮箱" prop="email">
              <el-input v-model="dialogForm.email" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="成立日期" prop="establishment_date">
              <el-date-picker
                v-model="dialogForm.establishment_date"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="is_active">
              <el-switch v-model="dialogForm.is_active" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog
      title="部门详情"
      v-model="detailVisible"
      width="50%"
    >
      <div class="detail-content" v-if="currentDepartment">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="部门编号">{{ currentDepartment.code }}</el-descriptions-item>
          <el-descriptions-item label="部门名称">{{ currentDepartment.name }}</el-descriptions-item>
          <el-descriptions-item label="所属企业">{{ currentDepartment.company_name }}</el-descriptions-item>
          <el-descriptions-item label="部门类型">{{ getDepartmentTypeLabel(currentDepartment.department_type) }}</el-descriptions-item>
          <el-descriptions-item label="部门层级">{{ currentDepartment.level }}</el-descriptions-item>
          <el-descriptions-item label="部门负责人">{{ currentDepartment.manager_name || '暂无' }}</el-descriptions-item>
          <el-descriptions-item label="办公地点">{{ currentDepartment.office_location }}</el-descriptions-item>
          <el-descriptions-item label="分机号码">{{ currentDepartment.extension }}</el-descriptions-item>
          <el-descriptions-item label="部门邮箱">{{ currentDepartment.email }}</el-descriptions-item>
          <el-descriptions-item label="成立日期">{{ currentDepartment.establishment_date }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="currentDepartment.is_active ? 'success' : 'danger'">
              {{ currentDepartment.is_active ? '启用' : '禁用' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
        
        <div style="margin-top: 20px;">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="部门描述">{{ currentDepartment.description }}</el-descriptions-item>
            <el-descriptions-item label="主要职责">{{ currentDepartment.responsibilities }}</el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import { baseInfoApi } from '@/api/baseInfo'

// 响应式数据
const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const detailVisible = ref(false)
const currentDepartment = ref(null)
const companies = ref([])
const departmentOptions = ref([])

// 搜索表单
const searchForm = reactive({
  search: '',
  company: '',
  department_type: '',
  is_active: ''
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 对话框表单
const dialogForm = reactive({
  id: null,
  code: '',
  name: '',
  department_type: '',
  company: '',
  parent_department: null,
  level: 1,
  description: '',
  responsibilities: '',
  office_location: '',
  extension: '',
  email: '',
  is_active: true,
  establishment_date: ''
})

// 表单引用
const formRef = ref()

// 表单验证规则
const formRules = {
  code: [{ required: true, message: '请输入部门编号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入部门名称', trigger: 'blur' }],
  department_type: [{ required: true, message: '请选择部门类型', trigger: 'change' }],
  company: [{ required: true, message: '请选择所属企业', trigger: 'change' }],
  level: [{ required: true, message: '请输入部门层级', trigger: 'blur' }]
}

// 方法
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm
    }
    
    const response = await baseInfoApi.getDepartments(params)
    tableData.value = response.results
    pagination.total = response.count
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const loadCompanies = async () => {
  try {
    const response = await baseInfoApi.getCompanies({ page_size: 100 })
    companies.value = response.results
  } catch (error) {
    console.error('加载企业列表失败:', error)
  }
}

const loadDepartmentOptions = async () => {
  try {
    const response = await baseInfoApi.getDepartments({ page_size: 100 })
    departmentOptions.value = response.results
  } catch (error) {
    console.error('加载部门选项失败:', error)
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadData()
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  loadData()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  loadData()
}

const showAddDialog = () => {
  resetForm()
  dialogVisible.value = true
}

const editDepartment = (row) => {
  Object.assign(dialogForm, { ...row })
  dialogVisible.value = true
}

const resetForm = () => {
  Object.assign(dialogForm, {
    id: null,
    code: '',
    name: '',
    department_type: '',
    company: '',
    parent_department: null,
    level: 1,
    description: '',
    responsibilities: '',
    office_location: '',
    extension: '',
    email: '',
    is_active: true,
    establishment_date: ''
  })
  formRef.value?.resetFields()
}

const handleCloseDialog = () => {
  resetForm()
  dialogVisible.value = false
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    const data = { ...dialogForm }
    if (data.establishment_date) {
      data.establishment_date = new Date(data.establishment_date).toISOString().split('T')[0]
    }
    
    if (dialogForm.id) {
      await baseInfoApi.updateDepartment(dialogForm.id, data)
      ElMessage.success('更新成功')
    } else {
      await baseInfoApi.createDepartment(data)
      ElMessage.success('添加成功')
    }
    
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('操作失败')
  }
}

const viewDetail = (row) => {
  currentDepartment.value = row
  detailVisible.value = true
}

const deleteDepartment = async (row) => {
  try {
    await ElMessageBox.confirm('确认删除这个部门吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    
    await baseInfoApi.deleteDepartment(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 辅助方法
const getDepartmentTypeLabel = (type) => {
  const labels = {
    production: '生产部门',
    technology: '技术部门',
    quality: '质量部门',
    management: '管理部门',
    sales: '销售部门',
    finance: '财务部门',
    hr: '人力资源',
    logistics: '物流部门',
    other: '其他'
  }
  return labels[type] || type
}

const getDepartmentTypeTagType = (type) => {
  const types = {
    production: 'primary',
    technology: 'success',
    quality: 'warning',
    management: 'info',
    sales: 'danger',
    finance: 'primary',
    hr: 'success',
    logistics: 'warning',
    other: 'default'
  }
  return types[type] || 'default'
}

// 生命周期
onMounted(() => {
  loadCompanies()
  loadDepartmentOptions()
  loadData()
})
</script>

<style scoped>
.department-management {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.search-bar {
  margin-bottom: 20px;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.table-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.pagination {
  padding: 20px;
  text-align: right;
  border-top: 1px solid #ebeef5;
}

.detail-content {
  max-height: 60vh;
  overflow-y: auto;
}
</style> 