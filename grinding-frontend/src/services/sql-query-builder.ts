/**
 * SQL查询构建器
 * 专门用于滚磨光整加工案例匹配的数据库查询生成
 */

// 查询配置接口
export interface QueryConfig {
  algorithm: string
  threshold: number
  maxResults: number
}

// 特征配置接口
export interface FeatureConfig {
  key: string
  weight: number
  dataType: string
}

// 目标案例数据接口
export interface TargetCaseData {
  [key: string]: any
}

/**
 * SQL查询构建器类
 */
export class SQLQueryBuilder {
  
  /**
   * 构建加权欧氏距离查询
   * @param targetCase 目标案例数据
   * @param features 特征配置
   * @param config 查询配置
   * @returns SQL查询字符串
   */
  static buildWeightedEuclideanQuery(targetCase: any, features: FeatureConfig[], config: QueryConfig): string {
    const distanceTerms: string[] = []
    const conditions: string[] = []
    
    features.forEach(feature => {
      const targetValue = targetCase[feature.key]
      if (targetValue !== undefined) {
        if (feature.dataType === 'numeric') {
          distanceTerms.push(`${feature.weight} * POWER((${feature.key} - ${targetValue}), 2)`)
        } else {
          distanceTerms.push(`${feature.weight} * CASE WHEN ${feature.key} = '${targetValue}' THEN 0 ELSE 1 END`)
        }
        conditions.push(`${feature.key} IS NOT NULL`)
      }
    })
    
    const similarityScore = `GREATEST(0, 100 - SQRT(${distanceTerms.join(' + ')}) * 10) AS similarity_score`
    
    return `SELECT case_id, material_type, original_grinding_time, grinding_speed, grinding_pressure, media_type, create_time, ${similarityScore} FROM grinding_cases WHERE ${conditions.join(' AND ')} HAVING similarity_score >= ${config.threshold} ORDER BY similarity_score DESC LIMIT ${config.maxResults}`
  }
  
  /**
   * 构建余弦相似度查询
   * @param targetCase 目标案例数据
   * @param features 特征配置
   * @param config 查询配置
   * @returns SQL查询字符串
   */
  static buildCosineSimilarityQuery(
    targetCase: TargetCaseData,
    features: FeatureConfig[],
    config: QueryConfig
  ): string {
    const dotProductTerms: string[] = []
    const targetNormTerms: string[] = []
    const caseNormTerms: string[] = []
    const conditions: string[] = []
    
    features.forEach(feature => {
      const targetValue = targetCase[feature.key]
      if (targetValue !== undefined && feature.dataType === 'numeric') {
        const weightedFeature = `${feature.weight} * ${feature.key}`
        const weightedTarget = `${feature.weight} * ${targetValue}`
        
        dotProductTerms.push(`(${weightedFeature}) * (${weightedTarget})`)
        targetNormTerms.push(`POWER(${weightedTarget}, 2)`)
        caseNormTerms.push(`POWER(${weightedFeature}, 2)`)
        
        conditions.push(`${feature.key} IS NOT NULL AND ${feature.key} > 0`)
      }
    })
    
    if (dotProductTerms.length === 0) {
      throw new Error('余弦相似度需要至少一个数值型特征')
    }
    
    const dotProduct = dotProductTerms.join(' + ')
    const targetNorm = targetNormTerms.join(' + ')
    const caseNorm = caseNormTerms.join(' + ')
    
    const cosineSimilarity = `
      (${dotProduct}) / (SQRT(${targetNorm}) * SQRT(${caseNorm})) * 100 AS similarity_score
    `
    
    const query = `
      WITH normalized_features AS (
        SELECT 
          *,
          ${cosineSimilarity}
        FROM grinding_cases
        WHERE 
          ${conditions.join(' AND ')}
          AND SQRT(${caseNorm}) > 0  -- 避免除零错误
      )
      SELECT 
        case_id,
        material_type,
        original_grinding_time,
        grinding_speed,
        grinding_pressure,
        media_type,
        media_ratio,
        additive_type,
        create_time,
        COALESCE(similarity_score, 0) AS similarity_score
      FROM normalized_features
      WHERE similarity_score >= ${config.threshold}
      ORDER BY similarity_score DESC
      LIMIT ${config.maxResults}
    `
    
    return query.trim()
  }
  
  /**
   * 构建曼哈顿距离查询
   * @param targetCase 目标案例数据
   * @param features 特征配置
   * @param config 查询配置
   * @returns SQL查询字符串
   */
  static buildManhattanDistanceQuery(
    targetCase: TargetCaseData,
    features: FeatureConfig[],
    config: QueryConfig
  ): string {
    const distanceTerms: string[] = []
    const conditions: string[] = []
    
    features.forEach(feature => {
      const targetValue = targetCase[feature.key]
      if (targetValue !== undefined && feature.dataType === 'numeric') {
        distanceTerms.push(`${feature.weight} * ABS(${feature.key} - ${targetValue})`)
        conditions.push(`${feature.key} IS NOT NULL`)
      }
    })
    
    if (distanceTerms.length === 0) {
      throw new Error('曼哈顿距离需要至少一个数值型特征')
    }
    
    const manhattanDistance = distanceTerms.join(' + ')
    const similarityScore = `GREATEST(0, 100 - (${manhattanDistance}) / ${distanceTerms.length}) AS similarity_score`
    
    const query = `
      SELECT 
        case_id,
        material_type,
        original_grinding_time,
        grinding_speed,
        grinding_pressure,
        media_type,
        media_ratio,
        additive_type,
        create_time,
        ${similarityScore}
      FROM grinding_cases
      WHERE 
        ${conditions.join(' AND ')}
      HAVING similarity_score >= ${config.threshold}
      ORDER BY similarity_score DESC
      LIMIT ${config.maxResults}
    `
    
    return query.trim()
  }
  
  /**
   * 构建综合相似度查询（多算法融合）
   * @param targetCase 目标案例数据
   * @param features 特征配置
   * @param config 查询配置
   * @returns SQL查询字符串
   */
  static buildComprehensiveQuery(
    targetCase: TargetCaseData,
    features: FeatureConfig[],
    config: QueryConfig
  ): string {
    // 构建多个相似度算法的结果
    const euclideanTerms: string[] = []
    const cosineTerms: string[] = []
    const manhattanTerms: string[] = []
    const conditions: string[] = []
    
    features.forEach(feature => {
      const targetValue = targetCase[feature.key]
      if (targetValue !== undefined && feature.dataType === 'numeric') {
        // 欧氏距离项
        euclideanTerms.push(`${feature.weight} * POWER(${feature.key} - ${targetValue}, 2)`)
        
        // 余弦相似度项
        cosineTerms.push(`(${feature.weight} * ${feature.key}) * (${feature.weight} * ${targetValue})`)
        
        // 曼哈顿距离项
        manhattanTerms.push(`${feature.weight} * ABS(${feature.key} - ${targetValue})`)
        
        conditions.push(`${feature.key} IS NOT NULL`)
      }
    })
    
    const euclideanSimilarity = `GREATEST(0, 100 - SQRT(${euclideanTerms.join(' + ')}) * 5)`
    const cosineSimilarity = `(${cosineTerms.join(' + ')}) / (SQRT(${cosineTerms.length}) * SQRT(${cosineTerms.length})) * 100`
    const manhattanSimilarity = `GREATEST(0, 100 - (${manhattanTerms.join(' + ')}) / ${manhattanTerms.length})`
    
    // 综合相似度（加权平均）
    const comprehensiveSimilarity = `
      (
        0.4 * (${euclideanSimilarity}) +
        0.3 * (${cosineSimilarity}) +
        0.3 * (${manhattanSimilarity})
      ) AS similarity_score
    `
    
    const query = `
      SELECT 
        case_id,
        material_type,
        original_grinding_time,
        grinding_speed,
        grinding_pressure,
        media_type,
        media_ratio,
        additive_type,
        surface_roughness_before,
        surface_roughness_after,
        create_time,
        ${comprehensiveSimilarity},
        -- 各算法的单独得分
        (${euclideanSimilarity}) AS euclidean_score,
        (${cosineSimilarity}) AS cosine_score,
        (${manhattanSimilarity}) AS manhattan_score
      FROM grinding_cases
      WHERE 
        ${conditions.join(' AND ')}
        AND material_type IS NOT NULL
      HAVING similarity_score >= ${config.threshold}
      ORDER BY similarity_score DESC
      LIMIT ${config.maxResults}
    `
    
    return query.trim()
  }
  
  /**
   * 构建分页查询
   * @param baseQuery 基础查询
   * @param page 页码（从1开始）
   * @param pageSize 每页大小
   * @returns 分页查询字符串
   */
  static buildPaginatedQuery(baseQuery: string, page: number, pageSize: number): string {
    const offset = (page - 1) * pageSize
    
    return `
      WITH paginated_results AS (
        ${baseQuery}
      ),
      total_count AS (
        SELECT COUNT(*) as total FROM paginated_results
      )
      SELECT 
        pr.*,
        tc.total
      FROM paginated_results pr
      CROSS JOIN total_count tc
      LIMIT ${pageSize} OFFSET ${offset}
    `
  }
  
  /**
   * 构建性能优化的查询（用于大数据量）
   * @param targetCase 目标案例数据
   * @param features 特征配置
   * @param config 查询配置
   * @returns 优化的查询字符串
   */
  static buildOptimizedQuery(
    targetCase: TargetCaseData,
    features: FeatureConfig[],
    config: QueryConfig
  ): string {
    // 预过滤条件（减少计算量）
    const preFilters: string[] = []
    
    features.forEach(feature => {
      const targetValue = targetCase[feature.key]
      if (targetValue !== undefined && feature.dataType === 'numeric') {
        // 基于目标值的范围预过滤
        const tolerance = targetValue * 0.5 // 50%容差
        preFilters.push(
          `${feature.key} BETWEEN ${targetValue - tolerance} AND ${targetValue + tolerance}`
        )
      } else if (feature.dataType === 'categorical') {
        // 分类特征的预过滤
        preFilters.push(`${feature.key} = '${targetValue}'`)
      }
    })
    
    // 基础查询
    const baseQuery = this.buildWeightedEuclideanQuery(targetCase, features, config)
    
    // 添加预过滤和索引提示
    const optimizedQuery = `
      ${baseQuery.replace(
        'FROM grinding_cases',
        `FROM grinding_cases /*+ USE_INDEX(grinding_cases, idx_material_time_composite) */`
      ).replace(
        'WHERE',
        `WHERE (${preFilters.slice(0, 2).join(' OR ')}) AND`
      )}
    `
    
    return optimizedQuery
  }
  
  /**
   * 构建索引创建语句
   * @returns 索引创建SQL数组
   */
  static buildIndexCreationStatements(): string[] {
    return [
      `CREATE INDEX idx_material_time_composite 
       ON grinding_cases (material_type, original_grinding_time, create_time)`,
      
      `CREATE INDEX idx_similarity_features 
       ON grinding_cases (grinding_speed, grinding_pressure, surface_roughness_before)`,
      
      `CREATE INDEX idx_dimensional_features 
       ON grinding_cases (dimensional_precision, hardness)`,
      
      `CREATE UNIQUE INDEX idx_case_id 
       ON grinding_cases (case_id)`,
      
      `CREATE INDEX idx_create_time_desc 
       ON grinding_cases (create_time DESC)`,
       
      // 分区表支持
      `ALTER TABLE grinding_cases 
       PARTITION BY RANGE (YEAR(create_time)) (
         PARTITION p2022 VALUES LESS THAN (2023),
         PARTITION p2023 VALUES LESS THAN (2024),
         PARTITION p2024 VALUES LESS THAN (2025),
         PARTITION p_future VALUES LESS THAN MAXVALUE
       )`
    ]
  }
  
  /**
   * 构建表结构创建语句
   * @returns 表创建SQL
   */
  static buildTableCreationStatement(): string {
    return `
      CREATE TABLE grinding_cases (
        case_id VARCHAR(50) PRIMARY KEY,
        material_type VARCHAR(100) NOT NULL,
        original_grinding_time DECIMAL(8,2) NOT NULL,
        grinding_speed INT NOT NULL,
        grinding_pressure DECIMAL(6,2) NOT NULL,
        media_type VARCHAR(50),
        media_ratio VARCHAR(20),
        additive_type VARCHAR(50),
        
        -- 工件特征
        diameter DECIMAL(8,3),
        thickness DECIMAL(8,3),
        length DECIMAL(8,3),
        weight DECIMAL(8,3),
        hardness INT,
        
        -- 表面质量
        surface_roughness_before DECIMAL(6,3),
        surface_roughness_after DECIMAL(6,3),
        dimensional_precision VARCHAR(20),
        
        -- 加工要求
        precision_requirement VARCHAR(20),
        surface_quality_requirement VARCHAR(50),
        deburring_requirement BOOLEAN DEFAULT FALSE,
        
        -- 元数据
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        source VARCHAR(50) DEFAULT 'manual',
        quality_score DECIMAL(3,2) DEFAULT 1.0,
        
        -- 索引
        INDEX idx_material_time (material_type, original_grinding_time),
        INDEX idx_features (grinding_speed, grinding_pressure, hardness),
        INDEX idx_quality (surface_roughness_before, dimensional_precision)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    `
  }
}

/**
 * 查询性能监控类
 */
export class QueryPerformanceMonitor {
  
  /**
   * 监控查询执行时间
   * @param queryName 查询名称
   * @param queryFunction 查询执行函数
   * @returns 查询结果和性能指标
   */
  static async monitorQuery<T>(
    queryName: string,
    queryFunction: () => Promise<T>
  ): Promise<{ result: T; metrics: { duration: number; queryName: string } }> {
    const startTime = performance.now()
    
    try {
      const result = await queryFunction()
      const endTime = performance.now()
      const duration = endTime - startTime
      
      console.log(`Query "${queryName}" executed in ${duration.toFixed(2)}ms`)
      
      return {
        result,
        metrics: { duration, queryName }
      }
    } catch (error) {
      const endTime = performance.now()
      const duration = endTime - startTime
      
      console.error(`Query "${queryName}" failed after ${duration.toFixed(2)}ms:`, error)
      throw error
    }
  }
}

// 导出查询构建器
export default SQLQueryBuilder 