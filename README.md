# 滚磨光整加工案例推理系统

[![Vue](https://img.shields.io/badge/Vue-3.x-green.svg)](https://vuejs.org/)
[![Django](https://img.shields.io/badge/Django-4.2-blue.svg)](https://www.djangoproject.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

基于Vue3 + Django + JWT认证的前后端分离智能制造系统，专注于滚磨光整加工工艺的案例智能推理与优选。

## 🎯 项目概述

本系统是一个专业的滚磨光整加工案例智能推理平台，集成了案例特征录入、权重设置、特征权重计算和案例推理等核心功能模块，基于层次分析法(AHP)实现智能案例匹配与工艺参数推荐。

## ✨ 核心功能

### 🔧 案例推理系统
- **案例特征录入** - 完整的加工案例数据录入和管理
- **权重设置与判断矩阵** - 基于AHP的科学权重配置 
- **计算特征权重** - 层次分析法权重计算与一致性检验
- **案例推理结果** - 智能案例匹配与可视化展示

### 📊 工艺数据管理
- **工艺案例数据库** - 案例录入、查询、修改、删除
- **工艺专家知识库** - 专家经验知识管理
- **工艺分析与评价** - 工艺参数分析评估

### 🏭 物料信息管理
- **零件信息数据库** - 零件材质、规格管理
- **滚磨设备数据库** - 设备参数配置
- **滚抛磨块数据库** - 磨块类型规格管理
- **化学剂数据库** - 化学剂配方管理
- **工装信息数据库** - 工装夹具信息

### 👥 系统管理
- **用户权限管理** - 多角色权限控制
- **基础信息库** - 企业、部门、人员管理
- **系统设置** - 系统参数配置

## 🛠 技术架构

### 前端技术栈
- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全的JavaScript超集
- **Element Plus** - Vue3组件库
- **Vite** - 现代化构建工具
- **Vue Router** - 官方路由管理器
- **Axios** - HTTP客户端

### 后端技术栈
- **Django 4.2** - Python Web框架
- **Django REST Framework** - REST API框架
- **Django Simple JWT** - JWT认证
- **Django CORS Headers** - 跨域处理
- **MySQL** - 关系型数据库

### 核心算法
- **层次分析法(AHP)** - 权重计算与一致性检验
- **相似度算法** - 欧氏距离、余弦相似度、曼哈顿距离
- **案例匹配算法** - 基于权重的智能案例检索

## 📁 项目结构

```
vue-django-jwt-auth/
├── grinding-frontend/          # Vue3前端项目
│   ├── src/
│   │   ├── views/             # 页面组件
│   │   │   ├── process/       # 工艺管理模块
│   │   │   ├── equipment/     # 设备管理
│   │   │   ├── base-info/     # 基础信息
│   │   │   └── ...
│   │   ├── components/        # 公共组件
│   │   ├── services/          # API服务
│   │   ├── router/           # 路由配置
│   │   └── docs/             # 技术文档
│   ├── package.json
│   └── ...
├── grinding_platform/         # Django后端项目
│   ├── grinding_platform/    # Django配置
│   ├── users/                # 用户模块
│   ├── process_cases/        # 工艺案例模块
│   ├── equipment/            # 设备管理模块
│   ├── base_info/           # 基础信息模块
│   ├── manage.py
│   └── ...
├── requirements.txt          # Python依赖
├── README.md                # 项目说明
└── ...
```

## 🚀 快速开始

### 环境要求
- **Node.js** >= 16.0.0
- **Python** >= 3.8
- **MySQL** >= 8.0

### 后端安装与运行

1. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **数据库配置**
```bash
cd grinding_platform
python manage.py makemigrations
python manage.py migrate
```

4. **创建超级用户**
```bash
python manage.py createsuperuser
```

5. **启动开发服务器**
```bash
python manage.py runserver
```

后端API服务运行在: `http://localhost:8000`

### 前端安装与运行

1. **安装依赖**
```bash
cd grinding-frontend
npm install
```

2. **启动开发服务器**
```bash
npm run dev
```

前端应用运行在: `http://localhost:5173`

3. **生产构建**
```bash
npm run build
```

## 🎮 系统使用

### 访问路径
1. **案例推理系统主入口**: `工艺数据库 → 工艺案例数据库 → 案例推理系统`
2. **直接URL访问**: `/process/case-reasoning`

### 案例推理流程
1. **案例特征录入** - 录入待处理工件的特征参数
2. **权重设置与判断矩阵** - 使用AHP方法设置特征权重
3. **计算特征权重** - 自动计算并验证权重一致性
4. **案例推理结果** - 获取智能匹配的相似案例和推荐方案

## 🔧 主要特性

### 🎯 智能推理算法
- **多种相似度算法**: 加权欧氏距离、余弦相似度、曼哈顿距离、综合相似度
- **AHP层次分析法**: 科学的权重配置与一致性检验
- **案例智能匹配**: 基于权重的高精度案例检索

### 📊 数据可视化
- **权重分布饼图**: 直观显示特征权重分布
- **相似度评分**: 实时计算案例匹配度
- **推荐级别标签**: 彩色标签区分推荐等级

### ⚡ 性能优化
- **数据库索引优化**: 支持大量案例高速检索
- **分页查询**: 大数据量分页展示
- **虚拟滚动**: 前端性能优化
- **多级缓存**: 提升响应速度

## 📝 API文档

系统提供完整的RESTful API，主要端点包括：

### 认证相关
- `POST /api/token/` - 获取JWT令牌
- `POST /api/token/refresh/` - 刷新JWT令牌
- `POST /api/users/register/` - 用户注册
- `POST /api/users/login/` - 用户登录

### 工艺数据管理
- `GET/POST /api/process-data/` - 工艺数据管理
- `GET/PUT/DELETE /api/process-data/{id}/` - 工艺数据详情操作

### 设备管理
- `GET/POST /api/equipment/` - 设备管理
- `GET/PUT/DELETE /api/equipment/{id}/` - 设备详情操作

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👨‍💻 作者

**智能制造案例推理系统开发团队**

- 系统架构: 前后端分离架构 + JWT认证
- 前端技术: Vue3 + TypeScript + Element Plus
- 后端技术: Django + DRF + MySQL
- 核心算法: AHP层次分析法 + 多种相似度算法

## 🔗 相关链接

- [Vue.js 官方文档](https://vuejs.org/)
- [Django 官方文档](https://docs.djangoproject.com/)
- [Element Plus 组件库](https://element-plus.org/)
- [Django REST Framework](https://www.django-rest-framework.org/)

## 🙏 致谢

感谢所有为这个项目贡献代码、提出建议和报告问题的开发者！

---

⭐ 如果这个项目对您有帮助，请给我们一个Star！ 