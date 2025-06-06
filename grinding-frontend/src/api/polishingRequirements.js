import request from '@/utils/request'

const BASE_URL = '/api/v1/polishing-requirements'

// 光整需求管理
export const polishingRequirementAPI = {
  // 获取需求列表
  getRequirements(params) {
    return request.get(`${BASE_URL}/requirements/`, { params })
  },

  // 获取需求详情
  getRequirement(id) {
    return request.get(`${BASE_URL}/requirements/${id}/`)
  },

  // 创建需求
  createRequirement(data) {
    return request.post(`${BASE_URL}/requirements/`, data)
  },

  // 更新需求
  updateRequirement(id, data) {
    return request.put(`${BASE_URL}/requirements/${id}/`, data)
  },

  // 删除需求
  deleteRequirement(id) {
    return request.delete(`${BASE_URL}/requirements/${id}/`)
  },

  // 获取我的需求
  getMyRequirements(params) {
    return request.get(`${BASE_URL}/requirements/my_requirements/`, { params })
  },

  // 获取待审核需求
  getPendingReviews(params) {
    return request.get(`${BASE_URL}/requirements/pending_review/`, { params })
  },

  // 提交审核
  submitForReview(id) {
    return request.post(`${BASE_URL}/requirements/${id}/submit_for_review/`)
  },

  // 审核需求
  reviewRequirement(id, data) {
    return request.post(`${BASE_URL}/requirements/${id}/review/`, data)
  },

  // 获取统计信息
  getStatistics() {
    return request.get(`${BASE_URL}/requirements/statistics/`)
  }
}

// 需求评论管理
export const requirementCommentAPI = {
  // 获取评论列表
  getComments(params) {
    return request.get(`${BASE_URL}/comments/`, { params })
  },

  // 创建评论
  createComment(data) {
    return request.post(`${BASE_URL}/comments/`, data)
  },

  // 删除评论
  deleteComment(id) {
    return request.delete(`${BASE_URL}/comments/${id}/`)
  }
}

// 需求附件管理
export const requirementAttachmentAPI = {
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

// 需求模板管理
export const requirementTemplateAPI = {
  // 获取模板列表
  getTemplates(params) {
    return request.get(`${BASE_URL}/templates/`, { params })
  },

  // 获取模板详情
  getTemplate(id) {
    return request.get(`${BASE_URL}/templates/${id}/`)
  },

  // 创建模板
  createTemplate(data) {
    return request.post(`${BASE_URL}/templates/`, data)
  },

  // 更新模板
  updateTemplate(id, data) {
    return request.put(`${BASE_URL}/templates/${id}/`, data)
  },

  // 删除模板
  deleteTemplate(id) {
    return request.delete(`${BASE_URL}/templates/${id}/`)
  }
}

export default {
  polishingRequirementAPI,
  requirementCommentAPI,
  requirementAttachmentAPI,
  requirementTemplateAPI
} 