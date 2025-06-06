import axios from 'axios'

// 创建axios实例
const request = axios.create({
  baseURL: '/api', // 基础URL，会使用vite的proxy代理到后端
  timeout: 10000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json;charset=UTF-8'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 在请求发送之前做一些处理
    // 可以在这里添加token等认证信息
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    console.log('请求发送:', config.method?.toUpperCase(), config.url)
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    console.log('响应接收:', response.config.method?.toUpperCase(), response.config.url, response.status)
    
    // 如果响应状态码是2xx，直接返回data
    return response.data
  },
  error => {
    console.error('响应错误:', error)
    
    // 处理不同的错误状态码
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          localStorage.removeItem('token')
          console.error('未授权访问，请重新登录')
          break
        case 403:
          console.error('访问被拒绝')
          break
        case 404:
          console.error('请求的资源不存在')
          break
        case 500:
          console.error('服务器内部错误')
          break
        default:
          console.error(`请求失败: ${status}`)
      }
      
      // 返回后端的错误信息或默认错误信息
      return Promise.reject(data || { message: '请求失败' })
    } else if (error.request) {
      // 网络错误
      console.error('网络错误，请检查网络连接')
      return Promise.reject({ message: '网络错误，请检查网络连接' })
    } else {
      // 其他错误
      console.error('请求配置错误:', error.message)
      return Promise.reject({ message: error.message })
    }
  }
)

export default request 