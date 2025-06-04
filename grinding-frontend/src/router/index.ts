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
        meta: { allowedRoles: ['system_admin'] },
        children: [
          {
            path: 'settings',
            name: 'SystemSettings',
            component: () => import('@/views/system/SettingsView.vue')
          },
          {
            path: 'users',
            name: 'UserManagement',
            component: () => import('@/views/system/UsersView.vue')
          },
          {
            path: 'statistics',
            name: 'Statistics',
            component: () => import('@/views/system/StatisticsView.vue')
          }
        ]
      },
      // 工艺工程师路由
      {
        path: 'process',
        meta: { allowedRoles: ['process_engineer'] },
        children: [
          {
            path: 'library',
            name: 'ProcessLibrary',
            component: () => import('@/views/process/LibraryView.vue')
          }
          // TODO: 添加其他工艺相关页面
          // {
          //   path: 'optimization',
          //   name: 'ProcessOptimization',
          //   component: () => import('@/views/process/OptimizationView.vue')
          // },
          // {
          //   path: 'cases',
          //   name: 'ProcessCases',
          //   component: () => import('@/views/process/CasesView.vue')
          // }
        ]
      },
      // 设备操作员路由
      {
        path: 'equipment',
        meta: { allowedRoles: ['equipment_operator'] },
        children: [
          {
            path: 'operation',
            name: 'EquipmentOperation',
            component: () => import('@/views/equipment/EquipmentOperationView.vue')
          }
          // TODO: 添加其他设备相关页面
          // {
          //   path: 'monitor',
          //   name: 'EquipmentMonitor',
          //   component: () => import('@/views/equipment/MonitorView.vue')
          // },
          // {
          //   path: 'records',
          //   name: 'EquipmentRecords',
          //   component: () => import('@/views/equipment/RecordsView.vue')
          // }
        ]
      },
      // 质量检测员路由
      {
        path: 'quality',
        meta: { allowedRoles: ['quality_inspector'] },
        children: [
          {
            path: 'inspection',
            name: 'QualityInspection',
            component: () => import('@/views/quality/QualityInspectionView.vue')
          }
          // TODO: 添加其他质量相关页面
          // {
          //   path: 'reports',
          //   name: 'QualityReports',
          //   component: () => import('@/views/quality/ReportsView.vue')
          // }
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