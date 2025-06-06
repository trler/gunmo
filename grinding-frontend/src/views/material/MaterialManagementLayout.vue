<template>
  <div class="material-management-layout">
    <el-container>
      <el-aside width="220px">
        <div class="sidebar-header">
          <h3>物料信息管理</h3>
        </div>
        <el-menu
          :router="true"
          :default-active="$route.path"
          class="material-management-menu"
        >
          <el-menu-item index="/material-management/blocks">
            <el-icon><Box /></el-icon>
            <span>磨块信息管理</span>
          </el-menu-item>
          <el-menu-item index="/material-management/equipment">
            <el-icon><Monitor /></el-icon>
            <span>设备信息管理</span>
          </el-menu-item>
          <el-menu-item index="/material-management/chemicals">
            <el-icon><Collection /></el-icon>
            <span>化学剂管理</span>
          </el-menu-item>
          <el-menu-item index="/material-management/fixtures">
            <el-icon><Tools /></el-icon>
            <span>工装管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { Monitor, Tools, Collection, Box } from '@element-plus/icons-vue'
</script>

<style scoped>
.material-management-layout {
  height: 100vh;
  background-color: #f5f7fa;
}

.el-container {
  height: 100%;
}

.el-aside {
  background-color: #ffffff;
  border-right: solid 1px #e6e6e6;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1);
  min-height: 100vh;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e6e6e6;
  background-color: #f8f9fa;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.material-management-menu {
  border-right: none;
  width: 100%;
  min-height: calc(100vh - 80px);
  background-color: #ffffff;
}

.material-management-menu .el-menu-item {
  color: #666;
  font-size: 15px;
  font-weight: 500;
  height: 48px;
  display: flex;
  align-items: center;
  border-radius: 4px;
  margin: 8px 12px;
  padding-left: 18px !important;
}

.material-management-menu .el-menu-item:hover {
  background-color: #f5f7fa;
  color: #409eff;
}

.material-management-menu .el-menu-item.is-active {
  background-color: #e6f7ff;
  color: #409eff;
  border-right: 3px solid #409eff;
}

.material-management-menu .el-icon {
  margin-right: 10px;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
  overflow-y: auto;
}
</style> 