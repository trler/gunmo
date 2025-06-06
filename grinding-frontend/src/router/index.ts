import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'
import type { UserType } from '@/types/auth'
import MainLayout from '@/layouts/MainLayout.vue'

// 路由元数据类型
interface RouteMeta {
  requiresAuth: boolean
  allowedRoles?: UserType[]
}

// 路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { requiresAuth: false }
  },
  // 需要认证的路由
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/DashboardView.vue')
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/ProfileView.vue')
      },
      // 系统管理员路由
      {
        path: 'system',
        meta: { allowedRoles: ['system_admin', 'fullstack_engineer'] },
        children: [
          {
            path: 'params',
            name: 'SystemParams',
            component: () => import('@/views/system/SystemParamsView.vue'),
            meta: { title: '系统参数管理' }
          },
          {
            path: 'permissions',
            name: 'SystemPermissions',
            component: () => import('@/views/system/SystemPermissionsView.vue'),
            meta: { title: '系统权限管理' }
          },
          {
            path: 'users',
            name: 'SystemUsers',
            component: () => import('@/views/system/SystemUsersView.vue'),
            meta: { title: '系统用户管理' }
          },
          {
            path: 'logs',
            name: 'SystemLogs',
            component: () => import('@/views/system/SystemLogsView.vue'),
            meta: { title: '系统日志管理' }
          },
          {
            path: 'settings',
            name: 'SystemSettings',
            component: () => import('@/views/system/SettingsView.vue'),
            meta: { title: '系统设置' }
          },
          {
            path: 'statistics',
            name: 'Statistics',
            component: () => import('@/views/system/StatisticsView.vue'),
            meta: { title: '系统统计' }
          }
        ]
      },
      // 工艺工程师路由
      {
        path: 'process',
        meta: { allowedRoles: ['process_engineer', 'fullstack_engineer'] },
        children: [
          {
            path: 'library',
            name: 'ProcessLibrary',
            component: () => import('@/views/process/LibraryView.vue')
          },
          {
            path: 'blocks',
            name: 'BlockInfo',
            component: () => import('@/views/process/BlockInfoView.vue')
          },
          // 工艺实例数据库相关路由
          {
            path: 'instances/management',
            name: 'ProcessInstancesManagement',
            component: () => import('@/views/process/instances/ProcessInstancesManagementView.vue'),
            meta: { title: '工艺案例管理', requiresAuth: true }
          },
          // 光整需求录入相关路由
          {
            path: 'polishing/requirement-entry',
            name: 'PolishingRequirementEntry',
            component: () => import('@/views/process/polishing/RequirementEntryView.vue'),
            meta: { title: '光整需求录入', requiresAuth: true }
          },
          {
            path: 'polishing/requirement-management',
            name: 'PolishingRequirementManagement',
            component: () => import('@/views/process/polishing/RequirementManagementView.vue'),
            meta: { title: '光整需求管理', requiresAuth: true }
          },
          {
            path: 'polishing/requirement-analysis',
            name: 'PolishingRequirementAnalysis',
            component: () => import('@/views/process/polishing/RequirementAnalysisView.vue'),
            meta: { title: '光整需求分析', requiresAuth: true }
          },
          // 光整工艺录入路由
          {
            path: 'polishing/process-entry-engineering',
            name: 'PolishingProcessEntryEngineering',
            component: () => import('@/views/process/polishing/ProcessEntryEngineeringView.vue'),
            meta: { title: '光整工艺录入(工艺师)', requiresAuth: true }
          },
          {
            path: 'polishing/process-entry-admin',
            name: 'PolishingProcessEntryAdmin',
            component: () => import('@/views/process/polishing/ProcessEntryAdminView.vue'),
            meta: { title: '光整工艺录入(管理员)', requiresAuth: true }
          },
          // 统计报表路由
          {
            path: 'statistics/polishing-requirements',
            name: 'PolishingRequirementsStatistics',
            component: () => import('@/views/process/statistics/PolishingRequirementsStatisticsView.vue'),
            meta: { title: '光整需求统计', requiresAuth: true }
          },
          {
            path: 'statistics/process-analysis',
            name: 'ProcessAnalysisStatistics',
            component: () => import('@/views/process/statistics/ProcessAnalysisStatisticsView.vue'),
            meta: { title: '工艺分析报表', requiresAuth: true }
          },
          {
            path: 'statistics/efficiency',
            name: 'EfficiencyStatistics',
            component: () => import('@/views/process/statistics/EfficiencyStatisticsView.vue'),
            meta: { title: '效率统计报表', requiresAuth: true }
          },
          // 工艺审核路由
          {
            path: 'review/pending',
            name: 'ProcessReviewPending',
            component: () => import('@/views/process/review/PendingReviewView.vue'),
            meta: { title: '待审核工艺', requiresAuth: true }
          },
          {
            path: 'review/approved',
            name: 'ProcessReviewApproved',
            component: () => import('@/views/process/review/ApprovedReviewView.vue'),
            meta: { title: '已审核工艺', requiresAuth: true }
          },
          {
            path: 'review/rejected',
            name: 'ProcessReviewRejected',
            component: () => import('@/views/process/review/RejectedReviewView.vue'),
            meta: { title: '驳回工艺', requiresAuth: true }
          },
          // 历史审核记录路由
          {
            path: 'history/all',
            name: 'ProcessHistoryAll',
            component: () => import('@/views/process/history/AllHistoryView.vue'),
            meta: { title: '全部审核记录', requiresAuth: true }
          },
          {
            path: 'history/by-date',
            name: 'ProcessHistoryByDate',
            component: () => import('@/views/process/history/HistoryByDateView.vue'),
            meta: { title: '按日期查询', requiresAuth: true }
          },
          {
            path: 'history/by-user',
            name: 'ProcessHistoryByUser',
            component: () => import('@/views/process/history/HistoryByUserView.vue'),
            meta: { title: '按用户查询', requiresAuth: true }
          },
          // 原有路由保持不变
          {
            path: 'case-data',
            name: 'ProcessCaseData',
            component: () => import('@/views/process/ProcessCaseDataView.vue'),
            meta: { title: '工艺案例数据库', requiresAuth: true }
          },
          {
            path: 'expert',
            name: 'ProcessExpert',
            component: () => import('@/views/process/ProcessExpertView.vue'),
            meta: { title: '工艺专家知识库', requiresAuth: true }
          },
          {
            path: 'analysis',
            name: 'ProcessAnalysis',
            component: () => import('@/views/process/ProcessAnalysisView.vue'),
            meta: { title: '工艺分析与评价', requiresAuth: true }
          }
        ]
      },
      // 物料信息管理路由组
      {
        path: 'material',
        children: [
          {
            path: 'parts',
            name: 'MaterialParts',
            component: () => import('@/views/equipment/EquipmentInfoView.vue'),
            meta: { title: '零件信息数据库', requiresAuth: true }
          },
          {
            path: 'equipment',
            name: 'MaterialEquipment',
            component: () => import('@/views/equipment/EquipmentInfoView.vue'),
            meta: { title: '滚磨设备数据库', requiresAuth: true }
          },
          {
            path: 'blocks',
            name: 'MaterialBlocks',
            component: () => import('@/views/process/BlockInfoView.vue'),
            meta: { title: '滚抛磨块数据库', requiresAuth: true }
          },
          {
            path: 'chemicals',
            name: 'MaterialChemicals',
            component: () => import('@/views/equipment/ChemicalView.vue'),
            meta: { title: '化学剂数据库', requiresAuth: true }
          },
          {
            path: 'fixtures',
            name: 'MaterialFixtures',
            component: () => import('@/views/equipment/FixtureView.vue'),
            meta: { title: '工装信息数据库', requiresAuth: true }
          }
        ]
      },
      // 基础信息库路由
      {
        path: 'base-info',
        children: [
          {
            path: '',
            name: 'BaseInfoIndex',
            component: () => import('@/views/base-info/BaseInfoIndex.vue'),
            meta: { title: '基础信息库', requiresAuth: true }
          },
          {
            path: 'companies',
            name: 'CompanyManagement',
            component: () => import('@/views/base-info/CompanyManagement.vue'),
            meta: { title: '企业信息管理', requiresAuth: true }
          },
          {
            path: 'departments',
            name: 'DepartmentManagement',
            component: () => import('@/views/base-info/DepartmentManagement.vue'),
            meta: { title: '部门信息管理', requiresAuth: true }
          },
          {
            path: 'personnel',
            name: 'PersonnelManagement',
            component: () => import('@/views/base-info/PersonnelManagement.vue'),
            meta: { title: '人员信息管理', requiresAuth: true }
          },
          {
            path: 'standards',
            name: 'StandardManagement',
            component: () => import('@/views/base-info/StandardManagement.vue'),
            meta: { title: '标准规范管理', requiresAuth: true }
          }
        ]
      },
      // 质量检测员路由
      {
        path: 'quality',
        meta: { allowedRoles: ['quality_inspector', 'fullstack_engineer'] },
        children: [
          {
            path: 'inspection',
            name: 'QualityInspection',
            component: () => import('@/views/quality/QualityInspectionView.vue')
          },
          {
            path: 'reports',
            name: 'QualityReports',
            component: () => import('@/views/quality/QualityReportsView.vue')
          }
        ]
      }
    ]
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue'),
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  const requiresAuth = to.meta.requiresAuth as boolean
  const allowedRoles = to.meta.allowedRoles as UserType[] | undefined

  // 检查是否需要认证
  if (requiresAuth) {
    // 如果用户未登录，重定向到登录页
    if (!userStore.isAuthenticated) {
      next({ 
        path: '/login', 
        query: { redirect: to.fullPath } 
      })
      return
    }

    // 检查用户角色权限
    if (allowedRoles && userStore.user) {
      const hasRole = allowedRoles.includes(userStore.user.user_type)
      if (!hasRole) {
        // 如果用户没有权限，重定向到仪表盘
        next({ path: '/dashboard' })
        return
      }
    }
  }

  // 如果已登录用户访问登录页，重定向到仪表盘
  if (to.path === '/login' && userStore.isAuthenticated) {
    next({ path: '/dashboard' })
    return
  }

  next()
})

export default router 