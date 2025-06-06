<template>
  <div class="nickname-container">
    <el-card class="nickname-card">
      <template #header>
        <div class="card-header">
          <h2>
            <el-icon><EditPen /></el-icon>
            修改昵称
          </h2>
          <p class="subtitle">设置您的显示昵称，让其他用户更容易识别您</p>
        </div>
      </template>

      <el-form
        ref="nicknameFormRef"
        :model="nicknameForm"
        :rules="formRules"
        label-width="120px"
        class="nickname-form"
      >
        <el-form-item label="当前昵称" class="current-info">
          <el-input
            :value="currentNickname"
            disabled
            placeholder="暂无昵称"
          >
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="新昵称" prop="nickname">
          <el-input
            v-model="nicknameForm.nickname"
            placeholder="请输入新昵称（2-20个字符）"
            clearable
            maxlength="20"
            show-word-limit
          >
            <template #prefix>
              <el-icon><EditPen /></el-icon>
            </template>
          </el-input>
          <div class="form-tip">
            <el-icon><InfoFilled /></el-icon>
            昵称将显示在用户列表和相关页面中，建议使用真实姓名或易识别的名称
          </div>
        </el-form-item>

        <el-form-item label="显示预览">
          <div class="preview-area">
            <div class="preview-item">
              <el-avatar :size="40">
                <el-icon><User /></el-icon>
              </el-avatar>
              <div class="preview-info">
                <div class="preview-nickname">
                  {{ nicknameForm.nickname || '新昵称预览' }}
                </div>
                <div class="preview-username">@{{ user?.username }}</div>
              </div>
            </div>
          </div>
        </el-form-item>

        <el-form-item>
          <div class="form-actions">
            <el-button
              type="primary"
              @click="handleSubmit"
              :loading="loading"
              size="large"
            >
              <el-icon><Check /></el-icon>
              保存修改
            </el-button>
            <el-button
              @click="handleReset"
              size="large"
            >
              <el-icon><RefreshLeft /></el-icon>
              重置
            </el-button>
            <el-button
              @click="handleCancel"
              size="large"
            >
              <el-icon><Close /></el-icon>
              取消
            </el-button>
          </div>
        </el-form-item>
      </el-form>

      <!-- 昵称历史记录 -->
      <el-card class="history-card" shadow="never">
        <template #header>
          <div class="card-header-small">
            <el-icon><Clock /></el-icon>
            <span>昵称历史</span>
          </div>
        </template>
        <el-timeline>
          <el-timeline-item
            v-for="(record, index) in nicknameHistory"
            :key="index"
            :timestamp="record.date"
            placement="top"
          >
            <el-tag v-if="index === 0" type="success" size="small">当前</el-tag>
            <span class="history-nickname">{{ record.nickname || '无昵称' }}</span>
          </el-timeline-item>
        </el-timeline>
      </el-card>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import {
  EditPen,
  User,
  InfoFilled,
  Check,
  RefreshLeft,
  Close,
  Clock
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const nicknameFormRef = ref<FormInstance>()
const loading = ref(false)

// 获取当前用户信息
const user = computed(() => userStore.user)

// 昵称表单
const nicknameForm = reactive({
  nickname: ''
})

// 表单验证规则
const formRules: FormRules = {
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 20, message: '昵称长度在 2 到 20 个字符', trigger: 'blur' },
    {
      pattern: /^[\u4e00-\u9fa5a-zA-Z0-9_\-\s]+$/,
      message: '昵称只能包含中文、英文、数字、下划线、连字符和空格',
      trigger: 'blur'
    }
  ]
}

// 当前昵称（从用户配置文件获取）
const currentNickname = computed(() => {
  return userStore.userProfile?.full_name || user.value?.first_name + ' ' + user.value?.last_name || ''
})

// 昵称历史记录（模拟数据，实际应从后端获取）
const nicknameHistory = ref([
  {
    nickname: currentNickname.value,
    date: '2024-01-15 10:30:00'
  },
  {
    nickname: '张三',
    date: '2024-01-10 14:20:00'
  },
  {
    nickname: 'ZhangSan',
    date: '2024-01-05 09:15:00'
  }
])

// 提交表单
const handleSubmit = async () => {
  if (!nicknameFormRef.value) return

  try {
    await nicknameFormRef.value.validate()
    
    await ElMessageBox.confirm(
      `确定要将昵称修改为 "${nicknameForm.nickname}" 吗？`,
      '确认修改',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    loading.value = true

    // 更新用户配置文件中的 full_name 字段作为昵称
    await userStore.updateUserProfile({
      full_name: nicknameForm.nickname
    })

    ElMessage.success('昵称修改成功！')

    // 更新历史记录
    nicknameHistory.value.unshift({
      nickname: nicknameForm.nickname,
      date: new Date().toLocaleString()
    })

    // 重置表单
    nicknameForm.nickname = ''
  } catch (error) {
    if (error !== 'cancel') {
      console.error('修改昵称失败:', error)
      ElMessage.error('修改昵称失败，请重试')
    }
  } finally {
    loading.value = false
  }
}

// 重置表单
const handleReset = () => {
  nicknameForm.nickname = currentNickname.value
}

// 取消修改
const handleCancel = () => {
  router.go(-1)
}

// 初始化
onMounted(async () => {
  try {
    // 获取用户配置文件
    await userStore.fetchUserProfile()
    
    // 设置当前昵称到表单
    if (currentNickname.value) {
      nicknameForm.nickname = currentNickname.value
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
})
</script>

<style scoped>
.nickname-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.nickname-card {
  margin-bottom: 20px;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0 0 10px 0;
  color: #303133;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.subtitle {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.nickname-form {
  padding: 20px 0;
}

.current-info :deep(.el-input__inner) {
  background-color: #f5f7fa !important;
  color: #909399 !important;
}

.form-tip {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
  line-height: 1.4;
}

.preview-area {
  border: 1px dashed #dcdfe6;
  border-radius: 6px;
  padding: 20px;
  background-color: #fafafa;
}

.preview-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.preview-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.preview-nickname {
  font-weight: 500;
  color: #303133;
  font-size: 16px;
}

.preview-username {
  color: #909399;
  font-size: 14px;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 20px;
}

.history-card {
  margin-top: 20px;
  background-color: #fafbfc;
}

.card-header-small {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: #606266;
}

.history-nickname {
  margin-left: 8px;
  font-weight: 500;
}

:deep(.el-timeline-item__timestamp) {
  color: #909399;
  font-size: 12px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}

:deep(.el-input__inner) {
  border-radius: 6px;
}

:deep(.el-button) {
  border-radius: 6px;
}

@media (max-width: 768px) {
  .nickname-container {
    padding: 10px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  :deep(.el-form-item__label) {
    text-align: left !important;
  }
}
</style> 