<template>
  <div class="settings-view">
    <div class="page-header">
      <h1>系统设置</h1>
      <div class="header-actions">
        <el-button type="primary" @click="handleSaveSettings">
          <i class="fas fa-save"></i> 保存设置
        </el-button>
      </div>
    </div>

    <el-tabs v-model="activeTab" class="settings-tabs">
      <!-- 基本设置 -->
      <el-tab-pane label="基本设置" name="basic">
        <el-form
          ref="basicFormRef"
          :model="basicSettings"
          :rules="basicRules"
          label-width="120px"
          class="settings-form"
        >
          <el-form-item label="系统名称" prop="systemName">
            <el-input v-model="basicSettings.systemName" />
          </el-form-item>
          <el-form-item label="系统描述" prop="description">
            <el-input
              v-model="basicSettings.description"
              type="textarea"
              :rows="3"
            />
          </el-form-item>
          <el-form-item label="系统Logo">
            <el-upload
              class="logo-uploader"
              action="/api/system/upload-logo"
              :show-file-list="false"
              :on-success="handleLogoSuccess"
              :before-upload="beforeLogoUpload"
            >
              <img v-if="basicSettings.logo" :src="basicSettings.logo" class="logo" />
              <el-icon v-else class="logo-uploader-icon"><Plus /></el-icon>
            </el-upload>
          </el-form-item>
          <el-form-item label="系统主题" prop="theme">
            <el-select v-model="basicSettings.theme">
              <el-option label="浅色" value="light" />
              <el-option label="深色" value="dark" />
              <el-option label="跟随系统" value="system" />
            </el-select>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 安全设置 -->
      <el-tab-pane label="安全设置" name="security">
        <el-form
          ref="securityFormRef"
          :model="securitySettings"
          :rules="securityRules"
          label-width="120px"
          class="settings-form"
        >
          <el-form-item label="密码策略" prop="passwordPolicy">
            <el-checkbox-group v-model="securitySettings.passwordPolicy">
              <el-checkbox label="uppercase">必须包含大写字母</el-checkbox>
              <el-checkbox label="lowercase">必须包含小写字母</el-checkbox>
              <el-checkbox label="number">必须包含数字</el-checkbox>
              <el-checkbox label="special">必须包含特殊字符</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="最小密码长度" prop="minPasswordLength">
            <el-input-number
              v-model="securitySettings.minPasswordLength"
              :min="6"
              :max="20"
            />
          </el-form-item>
          <el-form-item label="登录失败锁定">
            <el-switch v-model="securitySettings.loginLockEnabled" />
          </el-form-item>
          <el-form-item
            v-if="securitySettings.loginLockEnabled"
            label="最大失败次数"
            prop="maxLoginAttempts"
          >
            <el-input-number
              v-model="securitySettings.maxLoginAttempts"
              :min="3"
              :max="10"
            />
          </el-form-item>
          <el-form-item
            v-if="securitySettings.loginLockEnabled"
            label="锁定时间(分钟)"
            prop="lockoutDuration"
          >
            <el-input-number
              v-model="securitySettings.lockoutDuration"
              :min="5"
              :max="60"
            />
          </el-form-item>
          <el-form-item label="会话超时(分钟)" prop="sessionTimeout">
            <el-input-number
              v-model="securitySettings.sessionTimeout"
              :min="5"
              :max="1440"
            />
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 通知设置 -->
      <el-tab-pane label="通知设置" name="notification">
        <el-form
          ref="notificationFormRef"
          :model="notificationSettings"
          label-width="120px"
          class="settings-form"
        >
          <el-form-item label="邮件通知">
            <el-switch v-model="notificationSettings.emailEnabled" />
          </el-form-item>
          <template v-if="notificationSettings.emailEnabled">
            <el-form-item label="SMTP服务器" prop="smtpServer">
              <el-input v-model="notificationSettings.smtpServer" />
            </el-form-item>
            <el-form-item label="SMTP端口" prop="smtpPort">
              <el-input-number v-model="notificationSettings.smtpPort" />
            </el-form-item>
            <el-form-item label="发件人邮箱" prop="senderEmail">
              <el-input v-model="notificationSettings.senderEmail" />
            </el-form-item>
            <el-form-item label="邮箱密码" prop="emailPassword">
              <el-input
                v-model="notificationSettings.emailPassword"
                type="password"
                show-password
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleTestEmail">
                测试邮件发送
              </el-button>
            </el-form-item>
          </template>

          <el-divider />

          <el-form-item label="系统通知">
            <el-checkbox-group v-model="notificationSettings.systemNotifications">
              <el-checkbox label="user_login">用户登录</el-checkbox>
              <el-checkbox label="user_logout">用户登出</el-checkbox>
              <el-checkbox label="password_change">密码修改</el-checkbox>
              <el-checkbox label="role_change">角色变更</el-checkbox>
              <el-checkbox label="system_error">系统错误</el-checkbox>
            </el-checkbox-group>
          </el-form-item>

          <el-form-item label="通知方式">
            <el-checkbox-group v-model="notificationSettings.notificationMethods">
              <el-checkbox label="email">邮件</el-checkbox>
              <el-checkbox label="sms">短信</el-checkbox>
              <el-checkbox label="system">系统内</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 备份设置 -->
      <el-tab-pane label="备份设置" name="backup">
        <el-form
          ref="backupFormRef"
          :model="backupSettings"
          label-width="120px"
          class="settings-form"
        >
          <el-form-item label="自动备份">
            <el-switch v-model="backupSettings.autoBackupEnabled" />
          </el-form-item>
          <template v-if="backupSettings.autoBackupEnabled">
            <el-form-item label="备份频率" prop="backupFrequency">
              <el-select v-model="backupSettings.backupFrequency">
                <el-option label="每天" value="daily" />
                <el-option label="每周" value="weekly" />
                <el-option label="每月" value="monthly" />
              </el-select>
            </el-form-item>
            <el-form-item label="备份时间" prop="backupTime">
              <el-time-picker
                v-model="backupSettings.backupTime"
                format="HH:mm"
                placeholder="选择时间"
              />
            </el-form-item>
            <el-form-item label="保留备份数" prop="backupRetention">
              <el-input-number
                v-model="backupSettings.backupRetention"
                :min="1"
                :max="30"
              />
            </el-form-item>
            <el-form-item label="备份内容">
              <el-checkbox-group v-model="backupSettings.backupItems">
                <el-checkbox label="database">数据库</el-checkbox>
                <el-checkbox label="files">文件</el-checkbox>
                <el-checkbox label="logs">日志</el-checkbox>
                <el-checkbox label="settings">系统设置</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </template>

          <el-divider />

          <el-form-item>
            <el-button type="primary" @click="handleBackupNow">
              立即备份
            </el-button>
            <el-button type="success" @click="handleRestoreBackup">
              恢复备份
            </el-button>
          </el-form-item>

          <el-table
            v-if="backupList.length > 0"
            :data="backupList"
            style="width: 100%"
            border
          >
            <el-table-column prop="filename" label="备份文件" />
            <el-table-column prop="size" label="大小" width="120">
              <template #default="{ row }">
                {{ formatFileSize(row.size) }}
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="180">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button-group>
                  <el-button
                    type="primary"
                    size="small"
                    @click="handleDownloadBackup(row)"
                  >
                    下载
                  </el-button>
                  <el-button
                    type="success"
                    size="small"
                    @click="handleRestoreBackup(row)"
                  >
                    恢复
                  </el-button>
                  <el-button
                    type="danger"
                    size="small"
                    @click="handleDeleteBackup(row)"
                  >
                    删除
                  </el-button>
                </el-button-group>
              </template>
            </el-table-column>
          </el-table>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import axiosInstance from '@/api/axios'

// 状态
const activeTab = ref('basic')
const basicFormRef = ref<FormInstance>()
const securityFormRef = ref<FormInstance>()
const notificationFormRef = ref<FormInstance>()
const backupFormRef = ref<FormInstance>()

// 基本设置
const basicSettings = reactive({
  systemName: '',
  description: '',
  logo: '',
  theme: 'light'
})

// 安全设置
const securitySettings = reactive({
  passwordPolicy: ['uppercase', 'lowercase', 'number'],
  minPasswordLength: 8,
  loginLockEnabled: true,
  maxLoginAttempts: 5,
  lockoutDuration: 30,
  sessionTimeout: 120
})

// 通知设置
const notificationSettings = reactive({
  emailEnabled: false,
  smtpServer: '',
  smtpPort: 587,
  senderEmail: '',
  emailPassword: '',
  systemNotifications: ['user_login', 'system_error'],
  notificationMethods: ['email', 'system']
})

// 备份设置
const backupSettings = reactive({
  autoBackupEnabled: true,
  backupFrequency: 'daily',
  backupTime: new Date(2000, 0, 1, 2, 0),
  backupRetention: 7,
  backupItems: ['database', 'files', 'settings']
})

const backupList = ref([])

// 表单验证规则
const basicRules: FormRules = {
  systemName: [
    { required: true, message: '请输入系统名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { max: 200, message: '不能超过 200 个字符', trigger: 'blur' }
  ],
  theme: [
    { required: true, message: '请选择系统主题', trigger: 'change' }
  ]
}

const securityRules: FormRules = {
  minPasswordLength: [
    { required: true, message: '请设置最小密码长度', trigger: 'change' }
  ],
  maxLoginAttempts: [
    { required: true, message: '请设置最大失败次数', trigger: 'change' }
  ],
  lockoutDuration: [
    { required: true, message: '请设置锁定时间', trigger: 'change' }
  ],
  sessionTimeout: [
    { required: true, message: '请设置会话超时时间', trigger: 'change' }
  ]
}

// 方法
const fetchSettings = async () => {
  try {
    const response = await axiosInstance.get('/system/settings/')
    const settings = response.data

    // 更新基本设置
    Object.assign(basicSettings, settings.basic)
    Object.assign(securitySettings, settings.security)
    Object.assign(notificationSettings, settings.notification)
    Object.assign(backupSettings, settings.backup)
  } catch (error) {
    console.error('获取系统设置失败:', error)
    ElMessage.error('获取系统设置失败')
  }
}

const fetchBackupList = async () => {
  try {
    const response = await axiosInstance.get('/system/backups/')
    backupList.value = response.data
  } catch (error) {
    console.error('获取备份列表失败:', error)
    ElMessage.error('获取备份列表失败')
  }
}

const handleSaveSettings = async () => {
  try {
    const settings = {
      basic: basicSettings,
      security: securitySettings,
      notification: notificationSettings,
      backup: backupSettings
    }

    await axiosInstance.put('/system/settings/', settings)
    ElMessage.success('保存设置成功')
  } catch (error) {
    console.error('保存设置失败:', error)
    ElMessage.error('保存设置失败')
  }
}

const handleTestEmail = async () => {
  try {
    await axiosInstance.post('/system/test-email/', {
      smtpServer: notificationSettings.smtpServer,
      smtpPort: notificationSettings.smtpPort,
      senderEmail: notificationSettings.senderEmail,
      emailPassword: notificationSettings.emailPassword
    })
    ElMessage.success('测试邮件发送成功')
  } catch (error) {
    console.error('发送测试邮件失败:', error)
    ElMessage.error('发送测试邮件失败')
  }
}

const handleBackupNow = async () => {
  try {
    await axiosInstance.post('/system/backup/')
    ElMessage.success('备份创建成功')
    fetchBackupList()
  } catch (error) {
    console.error('创建备份失败:', error)
    ElMessage.error('创建备份失败')
  }
}

const handleRestoreBackup = async (backup: any) => {
  try {
    await ElMessageBox.confirm(
      '恢复备份将覆盖当前数据，是否继续？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await axiosInstance.post(`/system/restore/${backup.id}/`)
    ElMessage.success('备份恢复成功')
    // 可能需要重新加载页面
    window.location.reload()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('恢复备份失败:', error)
      ElMessage.error('恢复备份失败')
    }
  }
}

const handleDownloadBackup = async (backup: any) => {
  try {
    const response = await axiosInstance.get(`/system/backup/${backup.id}/download/`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', backup.filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('下载备份失败:', error)
    ElMessage.error('下载备份失败')
  }
}

const handleDeleteBackup = async (backup: any) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个备份吗？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await axiosInstance.delete(`/system/backup/${backup.id}/`)
    ElMessage.success('备份删除成功')
    fetchBackupList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除备份失败:', error)
      ElMessage.error('删除备份失败')
    }
  }
}

const beforeLogoUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件！')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB！')
    return false
  }
  return true
}

const handleLogoSuccess = (response: any) => {
  basicSettings.logo = response.url
  ElMessage.success('Logo 上传成功')
}

// 工具函数
const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 生命周期钩子
onMounted(() => {
  fetchSettings()
  fetchBackupList()
})
</script>

<style scoped>
.settings-view {
  padding: 1rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.page-header h1 {
  margin: 0;
  font-size: 1.75rem;
  color: #2c3e50;
}

.settings-tabs {
  background-color: #fff;
  padding: 1rem;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.settings-form {
  max-width: 800px;
  margin: 0 auto;
}

.logo-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 178px;
  height: 178px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo-uploader:hover {
  border-color: #409eff;
}

.logo-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
  line-height: 178px;
}

.logo {
  width: 178px;
  height: 178px;
  display: block;
  object-fit: contain;
}

@media (max-width: 768px) {
  .settings-view {
    padding: 0.5rem;
  }

  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .settings-form {
    padding: 0;
  }

  .logo-uploader {
    width: 120px;
    height: 120px;
  }

  .logo-uploader-icon {
    width: 120px;
    height: 120px;
    line-height: 120px;
  }

  .logo {
    width: 120px;
    height: 120px;
  }
}
</style> 