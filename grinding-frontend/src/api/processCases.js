import request from '@/utils/request'

const BASE_URL = '/api/v1/process-cases'

// 工艺实例相关API
export const processCaseApi = {
  // 获取工艺实例列表
  getCases: (params) => {
    return request({
      url: `${BASE_URL}/cases/`,
      method: 'get',
      params
    })
  },
  
  // 获取工艺实例详情
  getCase: (id) => {
    return request({
      url: `${BASE_URL}/cases/${id}/`,
      method: 'get'
    })
  },
  
  // 创建工艺实例
  createCase: (data) => {
    return request({
      url: `${BASE_URL}/cases/`,
      method: 'post',
      data
    })
  },
  
  // 更新工艺实例
  updateCase: (id, data) => {
    return request({
      url: `${BASE_URL}/cases/${id}/`,
      method: 'put',
      data
    })
  },
  
  // 删除工艺实例
  deleteCase: (id) => {
    return request({
      url: `${BASE_URL}/cases/${id}/`,
      method: 'delete'
    })
  },
  
  // 获取工艺实例统计信息
  getStatistics: () => {
    return request({
      url: `${BASE_URL}/cases/statistics/`,
      method: 'get'
    })
  }
}

// 工序模板相关API
export const processTemplateApi = {
  // 获取工序模板列表
  getTemplates: (params) => {
    return request({
      url: `${BASE_URL}/templates/`,
      method: 'get',
      params
    })
  },
  
  // 获取工序模板详情
  getTemplate: (id) => {
    return request({
      url: `${BASE_URL}/templates/${id}/`,
      method: 'get'
    })
  },
  
  // 创建工序模板
  createTemplate: (data) => {
    return request({
      url: `${BASE_URL}/templates/`,
      method: 'post',
      data
    })
  },
  
  // 更新工序模板
  updateTemplate: (id, data) => {
    return request({
      url: `${BASE_URL}/templates/${id}/`,
      method: 'put',
      data
    })
  },
  
  // 删除工序模板
  deleteTemplate: (id) => {
    return request({
      url: `${BASE_URL}/templates/${id}/`,
      method: 'delete'
    })
  },
  
  // 按类型获取模板
  getTemplatesByType: (type) => {
    return request({
      url: `${BASE_URL}/templates/by_type/`,
      method: 'get',
      params: { type }
    })
  }
}

// 专家知识库相关API
export const expertKnowledgeApi = {
  // 获取专家知识列表
  getKnowledge: (params) => {
    return request({
      url: `${BASE_URL}/knowledge/`,
      method: 'get',
      params
    })
  },
  
  // 获取专家知识详情
  getKnowledgeDetail: (id) => {
    return request({
      url: `${BASE_URL}/knowledge/${id}/`,
      method: 'get'
    })
  },
  
  // 创建专家知识
  createKnowledge: (data) => {
    return request({
      url: `${BASE_URL}/knowledge/`,
      method: 'post',
      data
    })
  },
  
  // 更新专家知识
  updateKnowledge: (id, data) => {
    return request({
      url: `${BASE_URL}/knowledge/${id}/`,
      method: 'put',
      data
    })
  },
  
  // 删除专家知识
  deleteKnowledge: (id) => {
    return request({
      url: `${BASE_URL}/knowledge/${id}/`,
      method: 'delete'
    })
  },
  
  // 获取热门知识
  getPopularKnowledge: () => {
    return request({
      url: `${BASE_URL}/knowledge/popular/`,
      method: 'get'
    })
  }
}

// 试验数据相关API
export const experimentDataApi = {
  // 获取试验数据列表
  getExperiments: (params) => {
    return request({
      url: `${BASE_URL}/experiments/`,
      method: 'get',
      params
    })
  },
  
  // 获取试验数据详情
  getExperiment: (id) => {
    return request({
      url: `${BASE_URL}/experiments/${id}/`,
      method: 'get'
    })
  },
  
  // 创建试验数据
  createExperiment: (data) => {
    return request({
      url: `${BASE_URL}/experiments/`,
      method: 'post',
      data
    })
  },
  
  // 更新试验数据
  updateExperiment: (id, data) => {
    return request({
      url: `${BASE_URL}/experiments/${id}/`,
      method: 'put',
      data
    })
  },
  
  // 删除试验数据
  deleteExperiment: (id) => {
    return request({
      url: `${BASE_URL}/experiments/${id}/`,
      method: 'delete'
    })
  },
  
  // 开始试验
  startExperiment: (id) => {
    return request({
      url: `${BASE_URL}/experiments/${id}/start_experiment/`,
      method: 'post'
    })
  },
  
  // 完成试验
  completeExperiment: (id) => {
    return request({
      url: `${BASE_URL}/experiments/${id}/complete_experiment/`,
      method: 'post'
    })
  }
} 