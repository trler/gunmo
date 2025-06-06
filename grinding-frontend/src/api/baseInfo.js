import request from '@/utils/request'

const BASE_URL = '/api/v1/base-info'

// 企业信息相关API
export const companyApi = {
  // 获取企业列表
  getCompanies: (params) => {
    return request({
      url: `${BASE_URL}/companies/`,
      method: 'get',
      params
    })
  },
  
  // 获取企业详情
  getCompany: (id) => {
    return request({
      url: `${BASE_URL}/companies/${id}/`,
      method: 'get'
    })
  },
  
  // 创建企业
  createCompany: (data) => {
    return request({
      url: `${BASE_URL}/companies/`,
      method: 'post',
      data
    })
  },
  
  // 更新企业
  updateCompany: (id, data) => {
    return request({
      url: `${BASE_URL}/companies/${id}/`,
      method: 'put',
      data
    })
  },
  
  // 删除企业
  deleteCompany: (id) => {
    return request({
      url: `${BASE_URL}/companies/${id}/`,
      method: 'delete'
    })
  },
  
  // 获取企业统计信息
  getStatistics: () => {
    return request({
      url: `${BASE_URL}/companies/statistics/`,
      method: 'get'
    })
  }
}

// 部门信息相关API
export const departmentApi = {
  // 获取部门列表
  getDepartments: (params) => {
    return request({
      url: `${BASE_URL}/departments/`,
      method: 'get',
      params
    })
  },
  
  // 获取部门详情
  getDepartment: (id) => {
    return request({
      url: `${BASE_URL}/departments/${id}/`,
      method: 'get'
    })
  },
  
  // 创建部门
  createDepartment: (data) => {
    return request({
      url: `${BASE_URL}/departments/`,
      method: 'post',
      data
    })
  },
  
  // 更新部门
  updateDepartment: (id, data) => {
    return request({
      url: `${BASE_URL}/departments/${id}/`,
      method: 'put',
      data
    })
  },
  
  // 删除部门
  deleteDepartment: (id) => {
    return request({
      url: `${BASE_URL}/departments/${id}/`,
      method: 'delete'
    })
  },
  
  // 获取部门树形结构
  getDepartmentTree: (companyId) => {
    return request({
      url: `${BASE_URL}/departments/tree/`,
      method: 'get',
      params: { company_id: companyId }
    })
  }
}

// 人员信息相关API
export const personnelApi = {
  // 获取人员列表
  getPersonnel: (params) => {
    return request({
      url: `${BASE_URL}/personnel/`,
      method: 'get',
      params
    })
  },
  
  // 获取人员详情
  getPersonnelDetail: (id) => {
    return request({
      url: `${BASE_URL}/personnel/${id}/`,
      method: 'get'
    })
  },
  
  // 创建人员
  createPersonnel: (data) => {
    return request({
      url: `${BASE_URL}/personnel/`,
      method: 'post',
      data
    })
  },
  
  // 更新人员
  updatePersonnel: (id, data) => {
    return request({
      url: `${BASE_URL}/personnel/${id}/`,
      method: 'put',
      data
    })
  },
  
  // 删除人员
  deletePersonnel: (id) => {
    return request({
      url: `${BASE_URL}/personnel/${id}/`,
      method: 'delete'
    })
  },
  
  // 获取人员统计信息
  getStatistics: () => {
    return request({
      url: `${BASE_URL}/personnel/statistics/`,
      method: 'get'
    })
  },
  
  // 按部门获取人员
  getPersonnelByDepartment: (departmentId) => {
    return request({
      url: `${BASE_URL}/personnel/by_department/`,
      method: 'get',
      params: { department_id: departmentId }
    })
  }
}

// 标准规范相关API
export const standardApi = {
  // 获取标准列表
  getStandards: (params) => {
    return request({
      url: `${BASE_URL}/standards/`,
      method: 'get',
      params
    })
  },
  
  // 获取标准详情
  getStandard: (id) => {
    return request({
      url: `${BASE_URL}/standards/${id}/`,
      method: 'get'
    })
  },
  
  // 创建标准
  createStandard: (data) => {
    return request({
      url: `${BASE_URL}/standards/`,
      method: 'post',
      data
    })
  },
  
  // 更新标准
  updateStandard: (id, data) => {
    return request({
      url: `${BASE_URL}/standards/${id}/`,
      method: 'put',
      data
    })
  },
  
  // 删除标准
  deleteStandard: (id) => {
    return request({
      url: `${BASE_URL}/standards/${id}/`,
      method: 'delete'
    })
  },
  
  // 获取标准统计信息
  getStatistics: () => {
    return request({
      url: `${BASE_URL}/standards/statistics/`,
      method: 'get'
    })
  },
  
  // 按分类搜索标准
  searchByClassification: (classification) => {
    return request({
      url: `${BASE_URL}/standards/search_by_classification/`,
      method: 'get',
      params: { classification }
    })
  }
}

// 统一导出基础信息API
export const baseInfoApi = {
  // 企业相关
  getCompanies: companyApi.getCompanies,
  getCompany: companyApi.getCompany,
  createCompany: companyApi.createCompany,
  updateCompany: companyApi.updateCompany,
  deleteCompany: companyApi.deleteCompany,
  getCompanyStatistics: companyApi.getStatistics,
  
  // 部门相关
  getDepartments: departmentApi.getDepartments,
  getDepartment: departmentApi.getDepartment,
  createDepartment: departmentApi.createDepartment,
  updateDepartment: departmentApi.updateDepartment,
  deleteDepartment: departmentApi.deleteDepartment,
  getDepartmentTree: departmentApi.getDepartmentTree,
  
  // 人员相关
  getPersonnel: personnelApi.getPersonnel,
  getPersonnelDetail: personnelApi.getPersonnelDetail,
  createPersonnel: personnelApi.createPersonnel,
  updatePersonnel: personnelApi.updatePersonnel,
  deletePersonnel: personnelApi.deletePersonnel,
  getPersonnelStatistics: personnelApi.getStatistics,
  getPersonnelByDepartment: personnelApi.getPersonnelByDepartment,
  
  // 标准相关
  getStandards: standardApi.getStandards,
  getStandard: standardApi.getStandard,
  createStandard: standardApi.createStandard,
  updateStandard: standardApi.updateStandard,
  deleteStandard: standardApi.deleteStandard,
  getStandardStatistics: standardApi.getStatistics,
  searchStandardsByClassification: standardApi.searchByClassification
}

export default baseInfoApi 