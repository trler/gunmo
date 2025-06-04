# 磨削平台管理系统 - 前端

基于Vue3 + TypeScript + Vite构建的滚磨光整加工行业管理系统前端应用。

## 技术栈

- **框架**: Vue 3 (Composition API)
- **语言**: TypeScript
- **构建工具**: Vite
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **HTTP客户端**: Axios
- **工具库**: @vueuse/core

## 项目结构

```
grinding-frontend/
├── public/                 # 静态资源
├── src/
│   ├── api/               # API接口封装
│   │   ├── client.ts      # Axios配置
│   │   └── auth.ts        # 认证API
│   ├── assets/            # 样式文件
│   │   ├── base.css       # 基础样式
│   │   └── main.css       # 主样式
│   ├── components/        # 通用组件
│   ├── composables/       # 组合式函数
│   ├── router/            # 路由配置
│   │   └── index.ts       # 路由定义
│   ├── stores/            # 状态管理
│   │   └── user.ts        # 用户状态
│   ├── types/             # 类型定义
│   │   └── user.ts        # 用户类型
│   ├── views/             # 页面视图
│   │   └── HomeView.vue   # 首页
│   ├── App.vue            # 根组件
│   └── main.ts            # 应用入口
├── index.html             # HTML模板
├── package.json           # 依赖配置
├── tsconfig.json          # TypeScript配置
├── vite.config.ts         # Vite配置
└── README.md              # 项目说明
```

## 开发环境设置

### 安装依赖

```bash
cd grinding-frontend
npm install
```

### 启动开发服务器

```bash
npm run dev
```

应用将在 http://localhost:3000 启动

### 构建生产版本

```bash
npm run build
```

### 预览生产版本

```bash
npm run preview
```

## API配置

前端应用配置了代理，所有 `/api` 开头的请求都会被代理到后端服务器 `http://127.0.0.1:8000`。

## 功能特性

### 已实现功能

- ✅ 用户认证系统（登录/注册/登出）
- ✅ JWT令牌自动刷新
- ✅ 路由守卫
- ✅ 响应式设计
- ✅ 全局状态管理
- ✅ API错误处理

### 待实现功能

- 🔄 登录/注册页面
- 🔄 用户个人资料页面
- 🔄 控制台仪表板
- 🔄 工艺数据管理
- 🔄 设备管理
- 🔄 404页面

## 用户类型

系统支持以下用户类型：

- `system_admin` - 系统管理员
- `process_engineer` - 工艺工程师
- `equipment_operator` - 设备操作员
- `quality_inspector` - 质量检测员
- `enterprise_admin` - 企业管理员

## 开发指南

### 添加新页面

1. 在 `src/views/` 目录创建新的Vue组件
2. 在 `src/router/index.ts` 添加路由配置
3. 如需认证，添加 `meta: { requiresAuth: true }`

### 添加新API

1. 在 `src/types/` 定义相关类型
2. 在 `src/api/` 创建API模块
3. 在需要的组件或store中使用

### 状态管理

使用Pinia进行状态管理，store位于 `src/stores/` 目录。

## 注意事项

- 确保后端Django服务器在 http://127.0.0.1:8000 运行
- 开发时前端服务器运行在 http://localhost:3000
- 所有API请求都会自动添加JWT令牌（如果存在）
- 令牌过期时会自动尝试刷新 