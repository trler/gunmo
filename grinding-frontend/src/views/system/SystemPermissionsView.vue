<template>
  <div class="system-permissions">
    <el-row :gutter="20">
      <!-- 角色列表 -->
      <el-col :span="8">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>角色列表</span>
              <el-button type="primary" @click="handleAddRole">
                <el-icon><Plus /></el-icon>添加角色
              </el-button>
            </div>
          </template>
          <el-table
            :data="roleList"
            style="width: 100%"
            v-loading="roleLoading"
            @row-click="handleRoleSelect"
            highlight-current-row
          >
            <el-table-column prop="name" label="角色名称" />
            <el-table-column prop="code" label="角色编码" />
            <el-table-column prop="status" label="状态" width="80">
              <template #default="scope">
                <el-tag :type="scope.row.status === '1' ? 'success' : 'danger'">
                  {{ scope.row.status === '1' ? '启用' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="scope">
                <el-button type="primary" link @click.stop="handleEditRole(scope.row)">
                  编辑
                </el-button>
                <el-button type="danger" link @click.stop="handleDeleteRole(scope.row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <!-- 权限分配 -->
      <el-col :span="16">
        <el-card class="box-card" v-if="currentRole">
          <template #header>
            <div class="card-header">
              <span>权限分配 - {{ currentRole.name }}</span>
              <el-button type="primary" @click="handleSavePermissions">保存权限</el-button>
            </div>
          </template>
          <el-tree
            ref="permissionTree"
            :data="permissionList"
            :props="defaultProps"
            show-checkbox
            node-key="id"
            :default-checked-keys="checkedPermissions"
            v-loading="permissionLoading"
          >
            <template #default="{ node, data }">
              <span class="custom-tree-node">
                <span>{{ node.label }}</span>
                <span class="permission-type" v-if="data.type">
                  <el-tag size="small" :type="data.type === 'menu' ? 'success' : 'warning'">
                    {{ data.type === 'menu' ? '菜单' : '按钮' }}
                  </el-tag>
                </span>
              </span>
            </template>
          </el-tree>
        </el-card>
        <el-empty v-else description="请选择角色" />
      </el-col>
    </el-row>

    <!-- 角色表单对话框 -->
    <el-dialog
      v-model="roleDialogVisible"
      :title="roleDialogType === 'add' ? '添加角色' : '编辑角色'"
      width="500px"
    >
      <el-form
        ref="roleFormRef"
        :model="roleForm"
        :rules="roleRules"
        label-width="100px"
      >
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="roleForm.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色编码" prop="code">
          <el-input v-model="roleForm.code" placeholder="请输入角色编码" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="roleForm.status">
            <el-radio label="1">启用</el-radio>
            <el-radio label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="roleForm.remark"
            type="textarea"
            placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="roleDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitRole">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

// 角色列表数据
const roleLoading = ref(false)
const roleList = ref([])
const currentRole = ref<any>(null)
const checkedPermissions = ref<string[]>([])

// 权限树数据
const permissionLoading = ref(false)
const permissionList = ref([])
const permissionTree = ref()
const defaultProps = {
  children: 'children',
  label: 'name'
}

// 角色表单对话框
const roleDialogVisible = ref(false)
const roleDialogType = ref<'add' | 'edit'>('add')
const roleFormRef = ref<FormInstance>()
const roleForm = reactive({
  id: '',
  name: '',
  code: '',
  status: '1',
  remark: ''
})

// 角色表单验证规则
const roleRules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入角色编码', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
})

// 获取角色列表
const getRoleList = async () => {
  roleLoading.value = true
  try {
    // TODO: 调用后端API获取数据
    // const res = await getRoleList()
    // roleList.value = res.data

    // 模拟数据
    roleList.value = [
      {
        id: '1',
        name: '超级管理员',
        code: 'SUPER_ADMIN',
        status: '1',
        remark: '系统超级管理员'
      },
      {
        id: '2',
        name: '普通用户',
        code: 'USER',
        status: '1',
        remark: '普通用户'
      }
    ]
  } catch (error) {
    console.error('获取角色列表失败:', error)
    ElMessage.error('获取角色列表失败')
  } finally {
    roleLoading.value = false
  }
}

// 获取权限列表
const getPermissionList = async () => {
  permissionLoading.value = true
  try {
    // TODO: 调用后端API获取数据
    // const res = await getPermissionList()
    // permissionList.value = res.data

    // 模拟数据
    permissionList.value = [
      {
        id: '1',
        name: '系统管理',
        type: 'menu',
        children: [
          {
            id: '1-1',
            name: '系统参数',
            type: 'menu',
            children: [
              {
                id: '1-1-1',
                name: '查看参数',
                type: 'button'
              },
              {
                id: '1-1-2',
                name: '编辑参数',
                type: 'button'
              }
            ]
          },
          {
            id: '1-2',
            name: '权限管理',
            type: 'menu',
            children: [
              {
                id: '1-2-1',
                name: '查看权限',
                type: 'button'
              },
              {
                id: '1-2-2',
                name: '分配权限',
                type: 'button'
              }
            ]
          }
        ]
      }
    ]
  } catch (error) {
    console.error('获取权限列表失败:', error)
    ElMessage.error('获取权限列表失败')
  } finally {
    permissionLoading.value = false
  }
}

// 获取角色权限
const getRolePermissions = async (roleId: string) => {
  try {
    // TODO: 调用后端API获取数据
    // const res = await getRolePermissions(roleId)
    // checkedPermissions.value = res.data

    // 模拟数据
    checkedPermissions.value = ['1-1-1', '1-2-1']
  } catch (error) {
    console.error('获取角色权限失败:', error)
    ElMessage.error('获取角色权限失败')
  }
}

// 选择角色
const handleRoleSelect = async (row: any) => {
  currentRole.value = row
  await getRolePermissions(row.id)
}

// 添加角色
const handleAddRole = () => {
  roleDialogType.value = 'add'
  roleForm.id = ''
  roleForm.name = ''
  roleForm.code = ''
  roleForm.status = '1'
  roleForm.remark = ''
  roleDialogVisible.value = true
}

// 编辑角色
const handleEditRole = (row: any) => {
  roleDialogType.value = 'edit'
  Object.assign(roleForm, row)
  roleDialogVisible.value = true
}

// 删除角色
const handleDeleteRole = (row: any) => {
  ElMessageBox.confirm(
    '确认删除该角色吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      // TODO: 调用后端API删除数据
      // await deleteRole(row.id)
      ElMessage.success('删除成功')
      getRoleList()
      if (currentRole.value?.id === row.id) {
        currentRole.value = null
        checkedPermissions.value = []
      }
    } catch (error) {
      console.error('删除角色失败:', error)
      ElMessage.error('删除角色失败')
    }
  })
}

// 提交角色表单
const handleSubmitRole = async () => {
  if (!roleFormRef.value) return
  await roleFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // TODO: 调用后端API保存数据
        // if (roleDialogType.value === 'add') {
        //   await addRole(roleForm)
        // } else {
        //   await updateRole(roleForm)
        // }
        ElMessage.success(roleDialogType.value === 'add' ? '添加成功' : '修改成功')
        roleDialogVisible.value = false
        getRoleList()
      } catch (error) {
        console.error('保存角色失败:', error)
        ElMessage.error('保存角色失败')
      }
    }
  })
}

// 保存权限
const handleSavePermissions = async () => {
  if (!currentRole.value || !permissionTree.value) return
  try {
    const checkedKeys = permissionTree.value.getCheckedKeys()
    const halfCheckedKeys = permissionTree.value.getHalfCheckedKeys()
    const permissionIds = [...checkedKeys, ...halfCheckedKeys]
    
    // TODO: 调用后端API保存数据
    // await saveRolePermissions(currentRole.value.id, permissionIds)
    ElMessage.success('保存成功')
  } catch (error) {
    console.error('保存权限失败:', error)
    ElMessage.error('保存权限失败')
  }
}

onMounted(() => {
  getRoleList()
  getPermissionList()
})
</script>

<style scoped>
.system-permissions {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.custom-tree-node {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.permission-type {
  margin-left: 10px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 