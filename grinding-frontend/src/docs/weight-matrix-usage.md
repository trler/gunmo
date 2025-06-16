# 滚磨光整加工案例智能优选 - 权重设置与判断矩阵系统

## 系统概述

本系统基于**层次分析法(AHP - Analytic Hierarchy Process)**实现滚磨光整加工案例的智能权重配置，支持特征重要性的科学量化和案例相似度的精确计算。

## 功能特点

### 1. 动态判断矩阵生成
- ✅ 根据案例特征录入区的有效字段自动生成判断矩阵
- ✅ 支持多层次特征分组（准则层、尺寸层、加工前特征层、加工要求层）
- ✅ 实时矩阵尺寸调整（如选择5个特征生成5×5矩阵）

### 2. 1-9标度法支持
- ✅ 标准AHP判断标度（1=同等重要，9=极端重要）
- ✅ 自动倒数关系填充（A[i,j] = 1/A[j,i]）
- ✅ 输入约束验证（仅允许1-9整数）

### 3. 权重计算算法
- ✅ **几何平均法**：快速准确的权重计算
- ✅ **特征向量法**：高精度的幂法迭代计算
- ✅ 权重归一化处理

### 4. 一致性检验
- ✅ 自动计算CR值（一致性比率）
- ✅ CR < 0.1 判定为通过检验
- ✅ 实时状态显示："权重计算中..." → "CR=0.08，通过检验"

## 使用流程

### 步骤1：特征选择
```typescript
// 在界面中选择需要分析的特征
const selectedFeatures = {
  criteria: ['A', 'A1', 'A2', 'A3'],    // 准则层
  dimension: ['A1', 'A11', 'A12'],       // 尺寸层
  preprocessing: ['A2', 'A21', 'A22'],   // 加工前特征层
  requirements: ['A3', 'A31', 'A32']     // 加工要求层
}
```

### 步骤2：填写判断矩阵
在生成的矩阵中，按1-9标度填写特征间的相对重要性：

| 标度 | 含义 |
|------|------|
| 1 | 两个因素同等重要 |
| 3 | 前者比后者稍微重要 |
| 5 | 前者比后者明显重要 |
| 7 | 前者比后者强烈重要 |
| 9 | 前者比后者极端重要 |
| 2,4,6,8 | 相邻判断的中值 |

### 步骤3：权重计算
```typescript
import { AHPAlgorithm } from '@/utils/ahp-algorithm'

// 计算权重
const result = AHPAlgorithm.calculateWeights(matrix, 'geometric')
console.log('权重:', result.weights)
console.log('一致性比率:', result.cr)
console.log('是否一致:', result.isConsistent)
```

### 步骤4：一致性检验
- CR < 0.1：一致性可以接受 ✅
- CR ≥ 0.1：一致性不佳，需要调整矩阵 ⚠️

### 步骤5：应用到案例匹配
```typescript
import { caseMatchingService } from '@/services/case-matching'

// 应用权重配置
caseMatchingService.loadWeightConfig(weightConfig)

// 计算案例相似度
const similarCases = caseMatchingService.findSimilarCases(
  targetCase, 
  70,  // 最小相似度阈值
  10   // 最大返回结果数
)
```

## 算法核心

### 权重计算（几何平均法）
```typescript
// 计算每行几何平均值
for (let i = 0; i < n; i++) {
  let product = 1
  for (let j = 0; j < n; j++) {
    product *= matrix[i][j]
  }
  weights[i] = Math.pow(product, 1/n)
}

// 归一化
const sum = weights.reduce((acc, w) => acc + w, 0)
return weights.map(w => w / sum)
```

### 一致性检验
```typescript
// 计算最大特征值
const lambdaMax = calculateLambdaMax(matrix, weights)

// 计算一致性指标
const CI = (lambdaMax - n) / (n - 1)

// 计算一致性比率
const CR = CI / RI[n]  // RI为随机一致性指标
```

## 数据衔接方案

### 1. 权重配置存储
```typescript
// 权重配置格式
interface WeightConfig {
  groups: {
    name: string
    features: {
      key: string
      label: string
      weight: number
    }[]
  }[]
  timestamp: number
}

// 存储到localStorage
localStorage.setItem('caseWeightConfig', JSON.stringify(weightConfig))
```

### 2. 案例匹配集成
```typescript
// 加载权重配置
caseMatchingService.loadWeightConfig()

// 计算加权相似度
const similarity = caseMatchingService.calculateSimilarity(case1, case2)
/*
返回结果：
{
  caseId: "case_001",
  similarity: 85,           // 百分比相似度
  matchedFeatures: [...],   // 匹配的特征列表
  weightedScore: 0.85,      // 加权分数
  details: {
    featureScores: {...},   // 各特征相似度
    normalizedScore: 0.85   // 归一化分数
  }
}
*/
```

### 3. 实时状态反馈
```vue
<template>
  <el-tag v-if="group.calculating" type="warning">
    <i class="fas fa-spinner fa-spin"></i>
    权重计算中...
  </el-tag>
  
  <el-tag v-else-if="group.weights.length > 0" type="success">
    <i class="fas fa-check"></i>
    CR={{ group.cr.toFixed(3) }}，{{ group.cr < 0.1 ? '通过检验' : '需要调整' }}
  </el-tag>
</template>
```

## 滚磨工艺特色功能

### 1. 专业特征分组
```typescript
const GRINDING_FEATURES = {
  GEOMETRY: ['长度', '直径', '厚度', '表面积'],
  MATERIAL: ['硬度', '材质类型', '热处理状态'],  
  SURFACE: ['表面粗糙度', '表面缺陷', '残余应力'],
  PROCESSING: ['精度要求', '表面质量', '去毛刺']
}
```

### 2. 工艺经验集成
```typescript
// 基于专家经验的默认权重关系
if (featureGroup === 'SURFACE') {
  matrix[0][1] = 3  // 表面粗糙度比表面缺陷重要
  matrix[0][2] = 5  // 表面粗糙度比残余应力重要
}
```

### 3. 合理性验证
```typescript
// 检查表面质量相关特征权重
const surfaceWeight = ['表面粗糙度', '表面质量', '表面光洁度']
  .reduce((sum, feature) => sum + weights[feature], 0)

if (surfaceWeight < 0.3) {
  warnings.push('滚磨工艺主要用于改善表面质量，建议增加表面相关特征的权重')
}
```

## 界面控件设计

### 1. 矩阵输入控件
- **el-input-number**：限制1-9整数输入
- **倒数值显示**：自动显示下三角矩阵的倒数值
- **对角线锁定**：对角线固定为1，不可编辑

### 2. 权重可视化
- **进度条显示**：直观展示各特征权重占比
- **排序列表**：按权重大小排序显示
- **颜色编码**：高权重绿色，低权重蓝色

### 3. 状态指示器
- **计算状态**：旋转图标 + "权重计算中..."
- **一致性标签**：颜色编码的CR值显示
- **建议提示**：智能调整建议

## 最佳实践

### 1. 特征选择建议
- 选择3-9个关键特征（矩阵阶数适中）
- 确保特征间有明显的重要性差异
- 避免过度细分导致判断困难

### 2. 判断矩阵填写技巧
- 先确定最重要和最不重要的特征
- 采用相对比较的思维方式
- 保持判断的传递一致性

### 3. 一致性优化方法
- CR > 0.1时，检查传递一致性
- 调整极端值（如将9改为7）
- 重新评估模糊判断

## 技术架构

```
WeightMatrixView.vue (界面层)
    ↓
AHPAlgorithm.ts (算法层)
    ↓  
CaseMatchingService.ts (服务层)
    ↓
localStorage / API (存储层)
```

## 扩展功能

### 1. 专家知识库
- 预置滚磨工艺专家判断矩阵
- 支持多专家意见融合
- 行业标准权重模板

### 2. 智能优化
- 基于历史数据的权重学习
- 遗传算法优化判断矩阵
- 自适应一致性调整

### 3. 可视化增强
- 权重热力图显示
- 敏感性分析图表
- 交互式矩阵编辑器

---

**开发完成功能：**
✅ 动态判断矩阵生成  
✅ 1-9标度法输入验证  
✅ 几何平均法权重计算  
✅ 一致性检验（CR值）  
✅ 实时状态显示  
✅ 权重配置导出导入  
✅ 案例匹配服务集成  
✅ 滚磨工艺特色功能  

系统已可通过导航：**工艺数据库 → 工艺案例数据库 → 案例推理系统 → 权重设置与判断矩阵** 访问使用。 