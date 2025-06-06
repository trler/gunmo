import request from '@/utils/request'

const BASE_URL = '/api/v1/polishing-processes'

// 光整工艺管理
export const polishingProcessAPI = {
  // 获取工艺列表
  getProcesses(params) {
    return request.get(`${BASE_URL}/processes/`, { params })
  },

  // 获取工艺详情
  getProcess(id) {
    return request.get(`${BASE_URL}/processes/${id}/`)
  },

  // 创建工艺
  createProcess(data) {
    return request.post(`${BASE_URL}/processes/`, data)
  },

  // 更新工艺
  updateProcess(id, data) {
    return request.put(`${BASE_URL}/processes/${id}/`, data)
  },

  // 删除工艺
  deleteProcess(id) {
    return request.delete(`${BASE_URL}/processes/${id}/`)
  },

  // 获取我的工艺
  getMyProcesses(params) {
    return request.get(`${BASE_URL}/processes/my_processes/`, { params })
  },

  // 获取标准工艺
  getStandardProcesses(params) {
    return request.get(`${BASE_URL}/processes/standard_processes/`, { params })
  },

  // 提交审核
  submitForReview(id) {
    return request.post(`${BASE_URL}/processes/${id}/submit_for_review/`)
  },

  // 获取统计信息
  getStatistics() {
    return request.get(`${BASE_URL}/processes/statistics/`)
  }
}

// 工艺步骤管理
export const processStepAPI = {
  // 获取步骤列表
  getSteps(params) {
    return request.get(`${BASE_URL}/steps/`, { params })
  },

  // 获取步骤详情
  getStep(id) {
    return request.get(`${BASE_URL}/steps/${id}/`)
  },

  // 创建步骤
  createStep(data) {
    return request.post(`${BASE_URL}/steps/`, data)
  },

  // 更新步骤
  updateStep(id, data) {
    return request.put(`${BASE_URL}/steps/${id}/`, data)
  },

  // 删除步骤
  deleteStep(id) {
    return request.delete(`${BASE_URL}/steps/${id}/`)
  }
}

// 工艺审核管理
export const processReviewAPI = {
  // 获取审核列表
  getReviews(params) {
    return request.get(`${BASE_URL}/reviews/`, { params })
  },

  // 创建审核
  createReview(data) {
    return request.post(`${BASE_URL}/reviews/`, data)
  },

  // 更新审核
  updateReview(id, data) {
    return request.put(`${BASE_URL}/reviews/${id}/`, data)
  },

  // 删除审核
  deleteReview(id) {
    return request.delete(`${BASE_URL}/reviews/${id}/`)
  }
}

// 工艺附件管理
export const processAttachmentAPI = {
  // 获取附件列表
  getAttachments(params) {
    return request.get(`${BASE_URL}/attachments/`, { params })
  },

  // 上传附件
  uploadAttachment(data) {
    return request.post(`${BASE_URL}/attachments/`, data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 删除附件
  deleteAttachment(id) {
    return request.delete(`${BASE_URL}/attachments/${id}/`)
  }
}

// 工艺使用记录管理
export const processUsageRecordAPI = {
  // 获取使用记录列表
  getUsageRecords(params) {
    return request.get(`${BASE_URL}/usage-records/`, { params })
  },

  // 创建使用记录
  createUsageRecord(data) {
    return request.post(`${BASE_URL}/usage-records/`, data)
  },

  // 更新使用记录
  updateUsageRecord(id, data) {
    return request.put(`${BASE_URL}/usage-records/${id}/`, data)
  },

  // 删除使用记录
  deleteUsageRecord(id) {
    return request.delete(`${BASE_URL}/usage-records/${id}/`)
  }
}

export default {
  polishingProcessAPI,
  processStepAPI,
  processReviewAPI,
  processAttachmentAPI,
  processUsageRecordAPI
} 