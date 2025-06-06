# 贡献指南

感谢您对滚磨光整加工管理系统的兴趣！我们欢迎所有形式的贡献。

## 如何贡献

### 报告错误
1. 查看已存在的Issues，确保问题尚未被报告
2. 创建新的Issue，包含：
   - 清晰的标题和描述
   - 重现步骤
   - 期望行为vs实际行为
   - 环境信息（操作系统、浏览器版本等）

### 建议功能
1. 创建新的Issue，标记为"enhancement"
2. 详细描述功能需求和使用场景
3. 等待维护者反馈和讨论

### 代码贡献
1. Fork项目
2. 创建功能分支: `git checkout -b feature/your-feature-name`
3. 提交变更: `git commit -am 'Add some feature'`
4. 推送分支: `git push origin feature/your-feature-name`
5. 创建Pull Request

## 开发环境设置

### 后端环境
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 启动开发服务器
python manage.py runserver
```

### 前端环境
```bash
cd grinding-frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 代码规范

### Python代码
- 遵循PEP 8规范
- 使用类型注解
- 编写文档字符串
- 添加单元测试

### TypeScript/Vue代码
- 使用ESLint和Prettier
- 遵循Vue 3 Composition API最佳实践
- 使用TypeScript类型定义
- 组件命名使用PascalCase

## 提交信息规范
```
type(scope): subject

body

footer
```

类型包括：
- feat: 新功能
- fix: 错误修复
- docs: 文档更新
- style: 代码格式化
- refactor: 代码重构
- test: 测试相关
- chore: 构建/工具链

## Pull Request要求
1. 清晰的标题和描述
2. 关联相关的Issue
3. 包含测试（如适用）
4. 更新文档（如适用）
5. 通过所有CI检查

## 联系方式
如有疑问，请通过GitHub Issues联系我们。 