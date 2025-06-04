# 滚磨光整加工管理系统

## 项目简介
滚磨光整加工管理系统是一个专门为滚磨光整加工行业设计的智能化管理解决方案。系统集成了设备管理、工艺数据管理、用户管理等功能，旨在提高生产效率、优化工艺流程、实现智能化管理。

## 主要功能
1. 设备管理
   - 设备信息管理
   - 设备状态监控
   - 设备维护记录
   - 设备告警管理

2. 工艺数据管理
   - 工艺参数记录
   - 加工过程监控
   - 数据统计分析
   - 质量追溯

3. 用户管理
   - 用户认证授权
   - 角色权限管理
   - 用户信息管理
   - 操作日志记录

## 技术栈
### 前端
- Vue 3
- TypeScript
- Vite
- Pinia
- Vue Router
- Element Plus
- Axios

### 后端
- Django
- Django REST framework
- JWT认证
- PostgreSQL
- Redis

## 开发环境要求
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+

## 快速开始
1. 克隆项目
```bash
git clone https://github.com/your-username/rolling-polishing-system.git
cd rolling-polishing-system
```

2. 后端设置
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

3. 前端设置
```bash
cd grinding-frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 部署说明
1. 后端部署
   - 使用 Gunicorn 作为 WSGI 服务器
   - 配置 Nginx 作为反向代理
   - 设置环境变量和配置文件

2. 前端部署
   - 构建生产版本：`npm run build`
   - 配置 Nginx 托管静态文件
   - 设置 API 代理

## 项目结构
```
rolling-polishing-system/
├── grinding_platform/          # 后端项目
│   ├── users/                 # 用户管理
│   ├── equipment/            # 设备管理
│   ├── process_data/         # 工艺数据管理
│   └── grinding_platform/    # 项目配置
├── grinding-frontend/         # 前端项目
│   ├── src/
│   │   ├── components/       # 组件
│   │   ├── views/           # 页面
│   │   ├── stores/          # 状态管理
│   │   ├── router/          # 路由配置
│   │   └── types/           # 类型定义
│   └── public/              # 静态资源
└── docs/                    # 项目文档
```

## 贡献指南
1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证
MIT License

## 联系方式
- 项目维护者：[您的名字]
- 邮箱：[您的邮箱]
- 项目主页：[项目地址] 