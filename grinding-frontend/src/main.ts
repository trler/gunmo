import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import router from './router'
import axiosInstance from './api/axios'

import './assets/main.css'

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 全局错误处理
app.config.errorHandler = (err, vm, info) => {
  console.error('全局错误:', err)
  console.error('错误信息:', info)
}

// 全局警告处理
app.config.warnHandler = (msg, vm, trace) => {
  console.warn('全局警告:', msg)
  console.warn('警告追踪:', trace)
}

// 将axios实例挂载到全局
app.config.globalProperties.$axios = axiosInstance

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app') 