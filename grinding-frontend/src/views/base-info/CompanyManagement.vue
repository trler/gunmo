<template>
  <div class="company-management">
    <div class="page-header">
      <h2>企业信息管理</h2>
      <div class="header-actions">
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          添加企业
        </el-button>
      </div>
    </div>

    <div class="search-bar">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input 
            v-model="searchForm.search" 
            placeholder="搜索企业名称、编号" 
            clearable
            @change="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.company_type" placeholder="企业类型" clearable @change="handleSearch">
            <el-option label="制造商" value="manufacturer"></el-option>
            <el-option label="供应商" value="supplier"></el-option>
            <el-option label="科研机构" value="research"></el-option>
            <el-option label="服务商" value="service"></el-option>
            <el-option label="其他" value="other"></el-option>
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.scale" placeholder="企业规模" clearable @change="handleSearch">
            <el-option label="大型企业" value="large"></el-option>
            <el-option label="中型企业" value="medium"></el-option>
            <el-option label="小型企业" value="small"></el-option>
            <el-option label="微型企业" value="micro"></el-option>
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
        <el-table-column prop="code" label="企业编号" width="120" />
        <el-table-column prop="name" label="企业名称" min-width="180" />
        <el-table-column prop="company_type" label="企业类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getCompanyTypeTagType(row.company_type)">
              {{ getCompanyTypeLabel(row.company_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="scale" label="企业规模" width="100">
          <template #default="{ row }">
            <el-tag :type="getScaleTagType(row.scale)">
              {{ getScaleLabel(row.scale) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="联系电话" width="140" />
        <el-table-column prop="legal_representative" label="法定代表人" width="120" />
        <el-table-column prop="registered_capital" label="注册资本(万元)" width="140" align="right" />
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
            <el-button size="small" type="primary" @click="editCompany(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteCompany(row)">删除</el-button>
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

    <!-- 添加/编辑企业对话框 -->
    <el-dialog
      :title="dialogForm.id ? '编辑企业' : '添加企业'"
      v-model="dialogVisible"
      width="70%"
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
            <el-form-item label="企业编号" prop="code">
              <el-input v-model="dialogForm.code" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="企业名称" prop="name">
              <el-input v-model="dialogForm.name" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="企业简称" prop="short_name">
              <el-input v-model="dialogForm.short_name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="企业类型" prop="company_type">
              <el-select v-model="dialogForm.company_type" style="width: 100%">
                <el-option label="制造商" value="manufacturer"></el-option>
                <el-option label="供应商" value="supplier"></el-option>
                <el-option label="科研机构" value="research"></el-option>
                <el-option label="服务商" value="service"></el-option>
                <el-option label="其他" value="other"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="统一社会信用代码" prop="unified_social_code">
              <el-input v-model="dialogForm.unified_social_code" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="法定代表人" prop="legal_representative">
              <el-input v-model="dialogForm.legal_representative" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="注册资本(万元)" prop="registered_capital">
              <el-input-number v-model="dialogForm.registered_capital" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
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
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="企业规模" prop="scale">
              <el-select v-model="dialogForm.scale" style="width: 100%">
                <el-option label="大型企业" value="large"></el-option>
                <el-option label="中型企业" value="medium"></el-option>
                <el-option label="小型企业" value="small"></el-option>
                <el-option label="微型企业" value="micro"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="dialogForm.phone" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="企业地址" prop="address">
          <el-input v-model="dialogForm.address" type="textarea" :rows="2" />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="邮政编码" prop="postal_code">
              <el-input v-model="dialogForm.postal_code" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="传真号码" prop="fax">
              <el-input v-model="dialogForm.fax" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="企业邮箱" prop="email">
              <el-input v-model="dialogForm.email" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="企业网站" prop="website">
          <el-input v-model="dialogForm.website" />
        </el-form-item>

        <el-form-item label="经营范围" prop="business_scope">
          <el-input v-model="dialogForm.business_scope" type="textarea" :rows="3" />
        </el-form-item>

        <el-form-item label="主要产品" prop="main_products">
          <el-input v-model="dialogForm.main_products" type="textarea" :rows="3" />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="行业类别" prop="industry_category">
              <el-input v-model="dialogForm.industry_category" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="质量管理体系" prop="quality_system">
              <el-input v-model="dialogForm.quality_system" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="企业资质" prop="certifications">
          <el-input v-model="dialogForm.certifications" type="textarea" :rows="2" />
        </el-form-item>

        <el-form-item label="备注信息" prop="remarks">
          <el-input v-model="dialogForm.remarks" type="textarea" :rows="2" />
        </el-form-item>

        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="dialogForm.is_active" />
        </el-form-item>
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
      title="企业详情"
      v-model="detailVisible"
      width="60%"
    >
      <div class="detail-content" v-if="currentCompany">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="企业编号">{{ currentCompany.code }}</el-descriptions-item>
          <el-descriptions-item label="企业名称">{{ currentCompany.name }}</el-descriptions-item>
          <el-descriptions-item label="企业简称">{{ currentCompany.short_name }}</el-descriptions-item>
          <el-descriptions-item label="企业类型">{{ getCompanyTypeLabel(currentCompany.company_type) }}</el-descriptions-item>
          <el-descriptions-item label="统一社会信用代码">{{ currentCompany.unified_social_code }}</el-descriptions-item>
          <el-descriptions-item label="法定代表人">{{ currentCompany.legal_representative }}</el-descriptions-item>
          <el-descriptions-item label="注册资本">{{ currentCompany.registered_capital }}万元</el-descriptions-item>
          <el-descriptions-item label="成立日期">{{ currentCompany.establishment_date }}</el-descriptions-item>
          <el-descriptions-item label="企业规模">{{ getScaleLabel(currentCompany.scale) }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentCompany.phone }}</el-descriptions-item>
          <el-descriptions-item label="传真号码">{{ currentCompany.fax }}</el-descriptions-item>
          <el-descriptions-item label="企业邮箱">{{ currentCompany.email }}</el-descriptions-item>
          <el-descriptions-item label="企业网站">{{ currentCompany.website }}</el-descriptions-item>
          <el-descriptions-item label="行业类别">{{ currentCompany.industry_category }}</el-descriptions-item>
          <el-descriptions-item label="质量管理体系">{{ currentCompany.quality_system }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="currentCompany.is_active ? 'success' : 'danger'">
              {{ currentCompany.is_active ? '启用' : '禁用' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
        
        <div style="margin-top: 20px;">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="企业地址">{{ currentCompany.address }}</el-descriptions-item>
            <el-descriptions-item label="经营范围">{{ currentCompany.business_scope }}</el-descriptions-item>
            <el-descriptions-item label="主要产品">{{ currentCompany.main_products }}</el-descriptions-item>
            <el-descriptions-item label="企业资质">{{ currentCompany.certifications }}</el-descriptions-item>
            <el-descriptions-item label="备注信息">{{ currentCompany.remarks }}</el-descriptions-item>
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
const currentCompany = ref(null)

// 搜索表单
const searchForm = reactive({
  search: '',
  company_type: '',
  scale: '',
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
  short_name: '',
  company_type: '',
  unified_social_code: '',
  legal_representative: '',
  registered_capital: 0,
  establishment_date: '',
  scale: '',
  address: '',
  postal_code: '',
  phone: '',
  fax: '',
  email: '',
  website: '',
  business_scope: '',
  main_products: '',
  industry_category: '',
  certifications: '',
  quality_system: '',
  is_active: true,
  remarks: ''
})

// 表单引用
const formRef = ref()

// 表单验证规则
const formRules = {
  code: [{ required: true, message: '请输入企业编号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入企业名称', trigger: 'blur' }],
  company_type: [{ required: true, message: '请选择企业类型', trigger: 'change' }],
  unified_social_code: [{ required: true, message: '请输入统一社会信用代码', trigger: 'blur' }],
  legal_representative: [{ required: true, message: '请输入法定代表人', trigger: 'blur' }],
  registered_capital: [{ required: true, message: '请输入注册资本', trigger: 'blur' }],
  establishment_date: [{ required: true, message: '请选择成立日期', trigger: 'change' }],
  scale: [{ required: true, message: '请选择企业规模', trigger: 'change' }],
  address: [{ required: true, message: '请输入企业地址', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
  business_scope: [{ required: true, message: '请输入经营范围', trigger: 'blur' }],
  main_products: [{ required: true, message: '请输入主要产品', trigger: 'blur' }],
  industry_category: [{ required: true, message: '请输入行业类别', trigger: 'blur' }]
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
    
    const response = await baseInfoApi.getCompanies(params)
    tableData.value = response.results
    pagination.total = response.count
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
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

const editCompany = (row) => {
  Object.assign(dialogForm, { ...row })
  dialogVisible.value = true
}

const resetForm = () => {
  Object.assign(dialogForm, {
    id: null,
    code: '',
    name: '',
    short_name: '',
    company_type: '',
    unified_social_code: '',
    legal_representative: '',
    registered_capital: 0,
    establishment_date: '',
    scale: '',
    address: '',
    postal_code: '',
    phone: '',
    fax: '',
    email: '',
    website: '',
    business_scope: '',
    main_products: '',
    industry_category: '',
    certifications: '',
    quality_system: '',
    is_active: true,
    remarks: ''
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
      await baseInfoApi.updateCompany(dialogForm.id, data)
      ElMessage.success('更新成功')
    } else {
      await baseInfoApi.createCompany(data)
      ElMessage.success('添加成功')
    }
    
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('提交失败:', error)
    if (error.errors) {
      // 显示验证错误
      ElMessage.error('表单验证失败，请检查输入')
    } else {
      ElMessage.error('操作失败')
    }
  }
}

const viewDetail = (row) => {
  currentCompany.value = row
  detailVisible.value = true
}

const deleteCompany = async (row) => {
  try {
    await ElMessageBox.confirm('确认删除这家企业吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    
    await baseInfoApi.deleteCompany(row.id)
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
const getCompanyTypeLabel = (type) => {
  const labels = {
    manufacturer: '制造商',
    supplier: '供应商',
    research: '科研机构',
    service: '服务商',
    other: '其他'
  }
  return labels[type] || type
}

const getCompanyTypeTagType = (type) => {
  const types = {
    manufacturer: 'primary',
    supplier: 'success',
    research: 'warning',
    service: 'info',
    other: 'default'
  }
  return types[type] || 'default'
}

const getScaleLabel = (scale) => {
  const labels = {
    large: '大型企业',
    medium: '中型企业',
    small: '小型企业',
    micro: '微型企业'
  }
  return labels[scale] || scale
}

const getScaleTagType = (scale) => {
  const types = {
    large: 'success',
    medium: 'primary',
    small: 'warning',
    micro: 'info'
  }
  return types[scale] || 'default'
}

// 生命周期
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.company-management {
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