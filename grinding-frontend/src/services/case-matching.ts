/**
 * 案例匹配服务
 * 用于滚磨光整加工案例的智能匹配和相似度计算
 */

// 案例特征接口
export interface CaseFeature {
  key: string
  label: string
  value: any
  weight: number
  type: 'numeric' | 'categorical' | 'boolean'
  unit?: string
}

// 案例数据接口
export interface CaseData {
  id: string
  name: string
  features: Record<string, any>
  metadata: {
    createTime: string
    updateTime: string
    source: string
    quality: number
  }
}

// 相似度计算结果接口
export interface SimilarityResult {
  caseId: string
  similarity: number
  matchedFeatures: string[]
  weightedScore: number
  details: {
    featureScores: Record<string, number>
    normalizedScore: number
  }
}

// 权重配置接口
export interface WeightConfig {
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

/**
 * 案例匹配服务类
 */
export class CaseMatchingService {
  
  private weightConfig: WeightConfig | null = null
  private caseDatabase: CaseData[] = []
  
  /**
   * 加载权重配置
   * @param config 权重配置或从localStorage加载
   */
  loadWeightConfig(config?: WeightConfig): void {
    if (config) {
      this.weightConfig = config
    } else {
      // 从localStorage加载
      const stored = localStorage.getItem('caseWeightConfig')
      if (stored) {
        try {
          this.weightConfig = JSON.parse(stored)
        } catch (error) {
          console.error('权重配置加载失败:', error)
          this.weightConfig = null
        }
      }
    }
  }
  
  /**
   * 获取当前权重配置
   */
  getWeightConfig(): WeightConfig | null {
    return this.weightConfig
  }
  
  /**
   * 设置案例数据库
   * @param cases 案例数据数组
   */
  setCaseDatabase(cases: CaseData[]): void {
    this.caseDatabase = cases
  }
  
  /**
   * 计算两个案例之间的特征相似度
   * @param feature1 案例1的特征值
   * @param feature2 案例2的特征值
   * @param featureType 特征类型
   * @returns 相似度分数 (0-1)
   */
  private calculateFeatureSimilarity(
    feature1: any, 
    feature2: any, 
    featureType: 'numeric' | 'categorical' | 'boolean'
  ): number {
    if (feature1 === undefined || feature2 === undefined) {
      return 0
    }
    
    switch (featureType) {
      case 'boolean':
        return feature1 === feature2 ? 1 : 0
        
      case 'categorical':
        return feature1 === feature2 ? 1 : 0
        
      case 'numeric':
        // 使用归一化的欧氏距离
        const val1 = Number(feature1)
        const val2 = Number(feature2)
        
        if (isNaN(val1) || isNaN(val2)) {
          return 0
        }
        
        // 假设数值范围为 [0, max]，计算相对差异
        const maxVal = Math.max(val1, val2, 100) // 设置一个最小基准值
        const diff = Math.abs(val1 - val2)
        return Math.max(0, 1 - diff / maxVal)
        
      default:
        return 0
    }
  }
  
  /**
   * 计算案例相似度
   * @param targetCase 目标案例
   * @param candidateCase 候选案例
   * @returns 相似度结果
   */
  calculateSimilarity(targetCase: CaseData, candidateCase: CaseData): SimilarityResult {
    if (!this.weightConfig) {
      throw new Error('权重配置未加载，请先配置特征权重')
    }
    
    const featureScores: Record<string, number> = {}
    const matchedFeatures: string[] = []
    let totalWeightedScore = 0
    let totalWeight = 0
    
    // 遍历所有配置的特征权重
    for (const group of this.weightConfig.groups) {
      for (const feature of group.features) {
        const targetValue = targetCase.features[feature.key]
        const candidateValue = candidateCase.features[feature.key]
        
        // 根据特征类型判断相似度计算方法
        let featureType: 'numeric' | 'categorical' | 'boolean' = 'numeric'
        
        // 简单的类型推断
        if (typeof targetValue === 'boolean' || typeof candidateValue === 'boolean') {
          featureType = 'boolean'
        } else if (typeof targetValue === 'string' || typeof candidateValue === 'string') {
          featureType = 'categorical'
        }
        
        const similarity = this.calculateFeatureSimilarity(
          targetValue, 
          candidateValue, 
          featureType
        )
        
        featureScores[feature.key] = similarity
        
        if (similarity > 0.7) { // 认为相似度大于0.7的特征为匹配特征
          matchedFeatures.push(feature.label)
        }
        
        totalWeightedScore += similarity * feature.weight
        totalWeight += feature.weight
      }
    }
    
    // 归一化加权分数
    const normalizedScore = totalWeight > 0 ? totalWeightedScore / totalWeight : 0
    
    return {
      caseId: candidateCase.id,
      similarity: Math.round(normalizedScore * 100), // 转换为百分比
      matchedFeatures,
      weightedScore: totalWeightedScore,
      details: {
        featureScores,
        normalizedScore
      }
    }
  }
  
  /**
   * 查找相似案例
   * @param targetCase 目标案例
   * @param minSimilarity 最小相似度阈值 (0-100)
   * @param maxResults 最大返回结果数
   * @returns 相似案例列表，按相似度降序排列
   */
  findSimilarCases(
    targetCase: CaseData, 
    minSimilarity: number = 70, 
    maxResults: number = 10
  ): SimilarityResult[] {
    const results: SimilarityResult[] = []
    
    for (const candidateCase of this.caseDatabase) {
      if (candidateCase.id === targetCase.id) {
        continue // 跳过自己
      }
      
      try {
        const similarity = this.calculateSimilarity(targetCase, candidateCase)
        
        if (similarity.similarity >= minSimilarity) {
          results.push(similarity)
        }
      } catch (error) {
        console.warn(`计算案例 ${candidateCase.id} 相似度失败:`, error)
      }
    }
    
    // 按相似度降序排列
    results.sort((a, b) => b.similarity - a.similarity)
    
    // 限制返回结果数量
    return results.slice(0, maxResults)
  }
  
  /**
   * 批量案例匹配
   * @param targetCases 目标案例数组
   * @param options 匹配选项
   * @returns 批量匹配结果
   */
  batchMatch(
    targetCases: CaseData[], 
    options: {
      minSimilarity?: number
      maxResults?: number
      parallel?: boolean
    } = {}
  ): Record<string, SimilarityResult[]> {
    const { minSimilarity = 70, maxResults = 10, parallel = true } = options
    const results: Record<string, SimilarityResult[]> = {}
    
    if (parallel && targetCases.length > 1) {
      // 并行处理（模拟）
      targetCases.forEach(targetCase => {
        results[targetCase.id] = this.findSimilarCases(targetCase, minSimilarity, maxResults)
      })
    } else {
      // 串行处理
      for (const targetCase of targetCases) {
        results[targetCase.id] = this.findSimilarCases(targetCase, minSimilarity, maxResults)
      }
    }
    
    return results
  }
  
  /**
   * 获取特征重要性排序
   * @returns 特征重要性列表
   */
  getFeatureImportance(): { feature: string, weight: number, group: string }[] {
    if (!this.weightConfig) {
      return []
    }
    
    const importance: { feature: string, weight: number, group: string }[] = []
    
    for (const group of this.weightConfig.groups) {
      for (const feature of group.features) {
        importance.push({
          feature: feature.label,
          weight: feature.weight,
          group: group.name
        })
      }
    }
    
    // 按权重降序排列
    return importance.sort((a, b) => b.weight - a.weight)
  }
  
  /**
   * 生成匹配报告
   * @param targetCase 目标案例
   * @param similarCases 相似案例结果
   * @returns 匹配报告
   */
  generateMatchReport(
    targetCase: CaseData, 
    similarCases: SimilarityResult[]
  ): {
    summary: {
      totalCandidates: number
      matchedCases: number
      averageSimilarity: number
      topSimilarity: number
    }
    recommendations: {
      caseId: string
      similarity: number
      reasons: string[]
      suggestions: string[]
    }[]
    analysis: {
      strongMatches: string[]
      weakMatches: string[]
      missingFeatures: string[]
    }
  } {
    const totalCandidates = this.caseDatabase.length
    const matchedCases = similarCases.length
    const averageSimilarity = matchedCases > 0 
      ? similarCases.reduce((sum, case_) => sum + case_.similarity, 0) / matchedCases 
      : 0
    const topSimilarity = matchedCases > 0 ? similarCases[0].similarity : 0
    
    // 生成推荐
    const recommendations = similarCases.slice(0, 3).map(case_ => ({
      caseId: case_.caseId,
      similarity: case_.similarity,
      reasons: case_.matchedFeatures.slice(0, 3),
      suggestions: this.generateCaseSuggestions(case_)
    }))
    
    // 分析强弱匹配特征
    const allFeatureScores = similarCases.flatMap(case_ => 
      Object.entries(case_.details.featureScores)
    )
    
    const strongMatches = [...new Set(
      allFeatureScores
        .filter(([_, score]) => score > 0.8)
        .map(([feature, _]) => feature)
    )]
    
    const weakMatches = [...new Set(
      allFeatureScores
        .filter(([_, score]) => score < 0.3)
        .map(([feature, _]) => feature)
    )]
    
    // 找出缺失的特征
    const configuredFeatures = this.weightConfig?.groups.flatMap(g => g.features.map(f => f.key)) || []
    const targetFeatures = Object.keys(targetCase.features)
    const missingFeatures = configuredFeatures.filter(f => !targetFeatures.includes(f))
    
    return {
      summary: {
        totalCandidates,
        matchedCases,
        averageSimilarity: Math.round(averageSimilarity),
        topSimilarity
      },
      recommendations,
      analysis: {
        strongMatches,
        weakMatches,
        missingFeatures
      }
    }
  }
  
  /**
   * 为案例生成建议
   * @param similarityResult 相似度结果
   * @returns 建议列表
   */
  private generateCaseSuggestions(similarityResult: SimilarityResult): string[] {
    const suggestions: string[] = []
    
    if (similarityResult.similarity > 90) {
      suggestions.push('高度匹配，可直接参考工艺参数')
    } else if (similarityResult.similarity > 80) {
      suggestions.push('较好匹配，建议适当调整工艺参数')
      suggestions.push('注意验证关键特征的差异')
    } else if (similarityResult.similarity > 70) {
      suggestions.push('部分匹配，需要仔细分析差异特征')
      suggestions.push('建议进行试验验证')
    }
    
    // 根据匹配特征数量给出建议
    if (similarityResult.matchedFeatures.length < 3) {
      suggestions.push('匹配特征较少，建议谨慎参考')
    }
    
    return suggestions
  }
  
  /**
   * 导出匹配结果
   * @param results 匹配结果
   * @param format 导出格式
   * @returns 导出数据
   */
  exportResults(
    results: SimilarityResult[], 
    format: 'json' | 'csv' = 'json'
  ): string {
    if (format === 'json') {
      return JSON.stringify(results, null, 2)
    } else {
      // CSV 格式
      const headers = ['案例ID', '相似度', '匹配特征', '加权分数']
      const rows = results.map(result => [
        result.caseId,
        result.similarity.toString(),
        result.matchedFeatures.join(';'),
        result.weightedScore.toFixed(3)
      ])
      
      return [headers, ...rows].map(row => row.join(',')).join('\n')
    }
  }
}

// 创建全局实例
export const caseMatchingService = new CaseMatchingService()

// 导出类型和服务
export default {
  CaseMatchingService,
  caseMatchingService
} 