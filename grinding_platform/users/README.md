# 滚磨光整加工行业用户管理系统

## 概述

这是一个专为滚磨光整加工行业设计的用户管理系统，支持多种用户类型和行业角色管理。

## 用户类型

系统支持以下用户类型：

1. **系统管理员** (`system_admin`) - 系统全局管理权限
2. **工艺工程师** (`process_engineer`) - 负责工艺设计和优化
3. **设备操作员** (`equipment_operator`) - 负责设备操作和维护
4. **质量检测员** (`quality_inspector`) - 负责产品质量检测
5. **企业管理员** (`enterprise_admin`) - 企业级管理权限

## 用户字段

### 基本字段
- `username` - 用户名（必填）
- `email` - 邮箱地址
- `first_name` - 名
- `last_name` - 姓
- `password` - 密码

### 行业专用字段
- `user_type` - 用户类型（见上述用户类型）
- `company` - 企业名称
- `department` - 部门
- `industry_role` - 产业链角色（如：供应商、制造商、科研机构）
- `phone` - 联系电话

## API 接口

### 用户注册
```
POST /api/users/register/

请求体：
{
    "username": "test_user",
    "email": "test@example.com", 
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "张",
    "last_name": "三",
    "user_type": "equipment_operator",
    "company": "某某滚磨设备有限公司",
    "department": "生产部",
    "industry_role": "制造商",
    "phone": "13800138000"
}

响应：
{
    "message": "用户注册成功",
    "user": {
        "id": 1,
        "username": "test_user",
        "email": "test@example.com",
        "user_type": "equipment_operator",
        "user_type_display": "设备操作员",
        "company": "某某滚磨设备有限公司",
        "department": "生产部",
        "industry_role": "制造商",
        "phone": "13800138000",
        ...
    }
}
```

### 用户登录（JWT）
```
POST /api/users/login/

请求体：
{
    "username": "test_user",
    "password": "password123"
}

响应：
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "test_user",
        "user_type": "equipment_operator",
        "user_type_display": "设备操作员",
        "company": "某某滚磨设备有限公司",
        ...
    }
}
```

### JWT Token 刷新
```
POST /api/users/token/refresh/

请求体：
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}

响应：
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 获取当前用户信息
```
GET /api/users/me/
Authorization: Bearer <access_token>

响应：
{
    "id": 1,
    "username": "test_user",
    "email": "test@example.com",
    "user_type": "equipment_operator",
    "user_type_display": "设备操作员",
    "company": "某某滚磨设备有限公司",
    "department": "生产部",
    "industry_role": "制造商",
    ...
}
```

### 更新用户信息
```
PATCH /api/users/me/
Authorization: Bearer <access_token>

请求体：
{
    "department": "技术部",
    "phone": "13900139000"
}

响应：
{
    "message": "用户信息更新成功",
    "user": {
        ...更新后的用户信息
    }
}
```

### 用户登出
```
POST /api/users/logout/
Authorization: Bearer <access_token>

请求体：
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}

响应：
{
    "message": "成功登出"
}
```

### 用户配置文件
```
GET /api/users/profile/
Authorization: Bearer <access_token>

响应：
{
    "user": {
        ...用户信息
    },
    "avatar": null,
    "bio": "",
    "preferences": {}
}
```

## JWT Token 包含的自定义声明

JWT access token 包含以下自定义字段：
- `user_type` - 用户类型代码
- `user_type_display` - 用户类型显示名称
- `company` - 企业名称
- `department` - 部门
- `industry_role` - 产业链角色
- `username` - 用户名
- `email` - 邮箱

## 权限说明

- 大部分API需要JWT认证
- 注册和登录接口允许匿名访问
- 用户只能查看和修改自己的信息

## 数据库迁移

在部署前，请运行以下命令创建数据库表：

```bash
python manage.py makemigrations users
python manage.py migrate
```

## 管理后台

系统提供了Django管理后台界面，可以方便地管理用户：

1. 访问 `/admin/`
2. 使用超级用户登录
3. 可以按用户类型、企业、部门等筛选用户
4. 支持批量操作和用户搜索

## 注意事项

1. 所有密码必须至少8位字符
2. 用户名必须唯一
3. 建议在生产环境中配置更强的密码验证规则
4. JWT token 有效期为30分钟，refresh token 有效期为1天 