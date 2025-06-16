/**
 * 层次分析法 (Analytic Hierarchy Process) 算法工具类
 * 用于滚磨光整加工案例智能优选的权重计算
 */

// 随机一致性指标表
export const RI_TABLE: Record<number, number> = {
  1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 
  6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
}

// 判断矩阵接口
export interface JudgmentMatrix {
  size: number
  data: number[][]
}

// 权重计算结果接口
export interface WeightResult {
  weights: number[]
  lambdaMax: number
  ci: number
  cr: number
  isConsistent: boolean
}

// 特征向量计算接口
export interface FeatureVector {
  vector: number[]
  eigenValue: number
}

/**
 * 层次分析法核心算法类
 */
export class AHPAlgorithm {
  
  /**
   * 验证判断矩阵的有效性
   * @param matrix 判断矩阵
   * @returns 是否有效
   */
  static validateMatrix(matrix: number[][]): boolean {
    const n = matrix.length
    
    // 检查矩阵是否为方阵
    if (!matrix.every(row => row.length === n)) {
      return false
    }
    
    // 检查对角线是否全为1
    for (let i = 0; i < n; i++) {
      if (matrix[i][i] !== 1) {
        return false
      }
    }
    
    // 检查矩阵是否满足倒数关系
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        if (i !== j) {
          const tolerance = 0.001
          if (Math.abs(matrix[i][j] * matrix[j][i] - 1) > tolerance) {
            return false
          }
        }
      }
    }
    
    // 检查所有元素是否为正数
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        if (matrix[i][j] <= 0) {
          return false
        }
      }
    }
    
    return true
  }
  
  /**
   * 使用几何平均法计算特征向量（权重）
   * @param matrix 判断矩阵
   * @returns 归一化的权重向量
   */
  static calculateWeightsByGeometricMean(matrix: number[][]): number[] {
    const n = matrix.length
    const weights: number[] = []
    
    // 计算每行的几何平均值
    for (let i = 0; i < n; i++) {
      let product = 1
      for (let j = 0; j < n; j++) {
        product *= matrix[i][j]
      }
      weights[i] = Math.pow(product, 1 / n)
    }
    
    // 归一化
    const sum = weights.reduce((acc, w) => acc + w, 0)
    return weights.map(w => w / sum)
  }
  
  /**
   * 使用特征向量法计算权重（幂法迭代）
   * @param matrix 判断矩阵
   * @param maxIterations 最大迭代次数
   * @param tolerance 收敛容差
   * @returns 特征向量结果
   */
  static calculateWeightsByEigenVector(
    matrix: number[][], 
    maxIterations: number = 100, 
    tolerance: number = 1e-8
  ): FeatureVector {
    const n = matrix.length
    let vector = new Array(n).fill(1 / n) // 初始向量
    let eigenValue = 0
    
    for (let iter = 0; iter < maxIterations; iter++) {
      const newVector: number[] = new Array(n).fill(0)
      
      // 矩阵向量乘法
      for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
          newVector[i] += matrix[i][j] * vector[j]
        }
      }
      
      // 计算特征值
      eigenValue = newVector.reduce((sum, val) => sum + val, 0) / n
      
      // 归一化
      const sum = newVector.reduce((acc, val) => acc + val, 0)
      const normalizedVector = newVector.map(val => val / sum)
      
      // 检查收敛
      const diff = vector.reduce((maxDiff, val, i) => 
        Math.max(maxDiff, Math.abs(val - normalizedVector[i])), 0
      )
      
      if (diff < tolerance) {
        return { vector: normalizedVector, eigenValue }
      }
      
      vector = normalizedVector
    }
    
    return { vector, eigenValue }
  }
  
  /**
   * 计算最大特征值 λmax
   * @param matrix 判断矩阵
   * @param weights 权重向量
   * @returns 最大特征值
   */
  static calculateLambdaMax(matrix: number[][], weights: number[]): number {
    const n = matrix.length
    let lambdaMax = 0
    
    for (let i = 0; i < n; i++) {
      let sum = 0
      for (let j = 0; j < n; j++) {
        sum += matrix[i][j] * weights[j]
      }
      lambdaMax += sum / weights[i]
    }
    
    return lambdaMax / n
  }
  
  /**
   * 计算一致性指标 CI
   * @param lambdaMax 最大特征值
   * @param n 矩阵阶数
   * @returns 一致性指标
   */
  static calculateCI(lambdaMax: number, n: number): number {
    return (lambdaMax - n) / (n - 1)
  }
  
  /**
   * 计算一致性比率 CR
   * @param ci 一致性指标
   * @param n 矩阵阶数
   * @returns 一致性比率
   */
  static calculateCR(ci: number, n: number): number {
    const ri = RI_TABLE[n] || 1.49
    return ci / ri
  }
  
  /**
   * 完整的权重计算和一致性检验
   * @param matrix 判断矩阵
   * @param method 计算方法 ('geometric' | 'eigenvector')
   * @returns 完整的权重计算结果
   */
  static calculateWeights(
    matrix: number[][], 
    method: 'geometric' | 'eigenvector' = 'geometric'
  ): WeightResult {
    // 验证矩阵
    if (!this.validateMatrix(matrix)) {
      throw new Error('无效的判断矩阵')
    }
    
    const n = matrix.length
    
    // 计算权重
    let weights: number[]
    if (method === 'geometric') {
      weights = this.calculateWeightsByGeometricMean(matrix)
    } else {
      const result = this.calculateWeightsByEigenVector(matrix)
      weights = result.vector
    }
    
    // 计算一致性指标
    const lambdaMax = this.calculateLambdaMax(matrix, weights)
    const ci = this.calculateCI(lambdaMax, n)
    const cr = this.calculateCR(ci, n)
    const isConsistent = cr < 0.1 // 一致性检验标准
    
    return {
      weights,
      lambdaMax,
      ci,
      cr,
      isConsistent
    }
  }
  
  /**
   * 批量计算多个判断矩阵的权重
   * @param matrices 多个判断矩阵
   * @param method 计算方法
   * @returns 多个权重计算结果
   */
  static calculateMultipleWeights(
    matrices: number[][][], 
    method: 'geometric' | 'eigenvector' = 'geometric'
  ): WeightResult[] {
    return matrices.map(matrix => this.calculateWeights(matrix, method))
  }
  
  /**
   * 计算综合权重（层次综合）
   * @param criteriaWeights 准则层权重
   * @param subCriteriaWeights 子准则层权重数组
   * @returns 综合权重
   */
  static calculateComprehensiveWeights(
    criteriaWeights: number[], 
    subCriteriaWeights: number[][]
  ): number[] {
    const result: number[] = []
    
    for (let j = 0; j < subCriteriaWeights[0].length; j++) {
      let sum = 0
      for (let i = 0; i < criteriaWeights.length; i++) {
        sum += criteriaWeights[i] * subCriteriaWeights[i][j]
      }
      result.push(sum)
    }
    
    return result
  }
  
  /**
   * 生成标准的判断矩阵模板
   * @param size 矩阵大小
   * @returns 初始化的判断矩阵（对角线为1，其他为1）
   */
  static generateMatrixTemplate(size: number): number[][] {
    return Array(size).fill(null).map(() => Array(size).fill(1))
  }
  
  /**
   * 从上三角矩阵自动填充下三角矩阵（倒数关系）
   * @param matrix 部分填充的矩阵
   * @returns 完整的判断矩阵
   */
  static fillReciprocalValues(matrix: number[][]): number[][] {
    const n = matrix.length
    const result = matrix.map(row => [...row]) // 深拷贝
    
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        if (i > j && result[i][j] === 0) {
          result[i][j] = 1 / result[j][i]
        } else if (i < j && result[i][j] === 0) {
          result[i][j] = 1 / result[j][i]
        }
      }
    }
    
    return result
  }
  
  /**
   * 检查矩阵的一致性水平
   * @param cr 一致性比率
   * @returns 一致性等级描述
   */
  static getConsistencyLevel(cr: number): string {
    if (cr < 0.05) return '非常好'
    if (cr < 0.1) return '可以接受'
    if (cr < 0.15) return '需要改进'
    return '不可接受'
  }
  
  /**
   * 提供矩阵调整建议
   * @param matrix 判断矩阵
   * @param cr 一致性比率
   * @returns 调整建议
   */
  static getAdjustmentSuggestions(matrix: number[][], cr: number): string[] {
    const suggestions: string[] = []
    
    if (cr >= 0.1) {
      suggestions.push('当前矩阵一致性不佳，建议重新评估判断值')
      
      // 找出可能的问题元素
      const n = matrix.length
      for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
          for (let k = j + 1; k < n; k++) {
            const consistency = matrix[i][j] * matrix[j][k] / matrix[i][k]
            if (Math.abs(consistency - 1) > 2) {
              suggestions.push(`建议检查第${i+1}、${j+1}、${k+1}个要素间的判断关系`)
            }
          }
        }
      }
      
      if (suggestions.length === 1) {
        suggestions.push('尝试将极端判断值（如9）调整为更温和的值（如7或5）')
        suggestions.push('确保传递一致性：如果A>B且B>C，则A>C的程度应该合理')
      }
    }
    
    return suggestions
  }
}

/**
 * 滚磨工艺特征权重配置类
 * 专门用于滚磨光整加工的特征权重管理
 */
export class GrindingFeatureWeights {
  
  /**
   * 滚磨工艺特征分组
   */
  static readonly FEATURE_GROUPS = {
    GEOMETRY: {
      name: 'geometry',
      label: '几何特征',
      features: ['长度', '直径', '厚度', '表面积', '体积']
    },
    MATERIAL: {
      name: 'material', 
      label: '材料特征',
      features: ['硬度', '材质类型', '热处理状态', '表面涂层']
    },
    SURFACE: {
      name: 'surface',
      label: '表面特征', 
      features: ['表面粗糙度', '表面缺陷', '残余应力', '表面硬度']
    },
    PROCESSING: {
      name: 'processing',
      label: '加工要求',
      features: ['精度要求', '表面质量', '去毛刺', '圆角处理', '表面光洁度']
    }
  }
  
  /**
   * 生成滚磨工艺的标准判断矩阵模板
   * @param featureGroup 特征组名称
   * @returns 标准判断矩阵
   */
  static generateStandardMatrix(featureGroup: keyof typeof this.FEATURE_GROUPS): number[][] {
    const group = this.FEATURE_GROUPS[featureGroup]
    const size = group.features.length
    
    // 根据滚磨工艺经验设置一些默认权重关系
    const matrix = AHPAlgorithm.generateMatrixTemplate(size)
    
    // 可以在这里添加基于专家经验的默认判断值
    if (featureGroup === 'SURFACE') {
      // 表面特征中，表面粗糙度通常最重要
      matrix[0][1] = 3 // 表面粗糙度比表面缺陷重要
      matrix[0][2] = 5 // 表面粗糙度比残余应力重要
      matrix[0][3] = 2 // 表面粗糙度比表面硬度稍重要
    }
    
    return AHPAlgorithm.fillReciprocalValues(matrix)
  }
  
  /**
   * 验证滚磨工艺权重配置的合理性
   * @param weights 权重配置
   * @returns 验证结果和建议
   */
  static validateGrindingWeights(weights: Record<string, number>): {
    isValid: boolean
    warnings: string[]
    suggestions: string[]
  } {
    const warnings: string[] = []
    const suggestions: string[] = []
    
    // 检查表面质量相关特征是否有足够权重
    const surfaceRelated = ['表面粗糙度', '表面质量', '表面光洁度']
    const surfaceWeight = surfaceRelated.reduce((sum, feature) => 
      sum + (weights[feature] || 0), 0
    )
    
    if (surfaceWeight < 0.3) {
      warnings.push('表面质量相关特征权重偏低')
      suggestions.push('滚磨工艺主要用于改善表面质量，建议增加表面相关特征的权重')
    }
    
    // 检查几何特征权重是否过高
    const geometryFeatures = ['长度', '直径', '厚度', '表面积']
    const geometryWeight = geometryFeatures.reduce((sum, feature) => 
      sum + (weights[feature] || 0), 0
    )
    
    if (geometryWeight > 0.5) {
      warnings.push('几何特征权重过高')
      suggestions.push('对于滚磨工艺，几何特征影响相对较小，建议降低其权重')
    }
    
    return {
      isValid: warnings.length === 0,
      warnings,
      suggestions
    }
  }
}

// 导出默认实例
export default AHPAlgorithm 