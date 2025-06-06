<template>
  <nav class="navigation">
    <div class="nav-header">
      <h1 class="logo">滚磨光整加工数据库平台</h1>
    </div>
    <div class="nav-menu">
      <!-- 系统设置 -->
      <div class="nav-group">
        <div class="nav-group-header" @click="toggleGroup('system')">
          <div class="nav-group-title">
            <i class="fas fa-cogs"></i>
            <span>系统设置</span>
          </div>
          <i class="fas fa-chevron-down" :class="{ 'rotated': expandedGroups.system }"></i>
        </div>
        <div class="nav-group-content" v-show="expandedGroups.system">
          <router-link to="/system/params" class="nav-item">
            <span>系统参数管理</span>
          </router-link>
          <router-link to="/system/permissions" class="nav-item">
            <span>系统权限管理</span>
          </router-link>
          <router-link to="/system/users" class="nav-item">
            <span>系统用户管理</span>
          </router-link>
          <router-link to="/system/logs" class="nav-item">
            <span>系统日志管理</span>
          </router-link>
        </div>
      </div>
      <!-- 基础信息库 -->
      <div class="nav-group">
        <div class="nav-group-header" @click="toggleGroup('base')">
          <div class="nav-group-title">
            <i class="fas fa-database"></i>
            <span>基础信息库</span>
          </div>
          <i class="fas fa-chevron-down" :class="{ 'rotated': expandedGroups.base }"></i>
        </div>
        <div class="nav-group-content" v-show="expandedGroups.base">
          <router-link to="/base-info/companies" class="nav-item">
            <span>企业信息数据库</span>
          </router-link>
          <router-link to="/base-info/departments" class="nav-item">
            <span>部门信息数据库</span>
          </router-link>
          <router-link to="/base-info/personnel" class="nav-item">
            <span>人员信息数据库</span>
          </router-link>
          <router-link to="/base-info/standards" class="nav-item">
            <span>标准规范数据库</span>
          </router-link>
        </div>
      </div>
      <!-- 物料数据库 -->
      <div class="nav-group">
        <div class="nav-group-header" @click="toggleGroup('material')">
          <div class="nav-group-title">
            <i class="fas fa-boxes"></i>
            <span>物料数据库</span>
          </div>
          <i class="fas fa-chevron-down" :class="{ 'rotated': expandedGroups.material }"></i>
        </div>
        <div class="nav-group-content" v-show="expandedGroups.material">
          <router-link to="/material/parts" class="nav-item">
            <span>零件信息数据库</span>
          </router-link>
          <router-link to="/material/equipment" class="nav-item">
            <span>滚磨设备数据库</span>
          </router-link>
          <router-link to="/material/blocks" class="nav-item">
            <span>滚抛磨块数据库</span>
          </router-link>
          <router-link to="/material/chemicals" class="nav-item">
            <span>化学剂数据库</span>
          </router-link>
          <router-link to="/material/fixtures" class="nav-item">
            <span>工装信息数据库</span>
          </router-link>
        </div>
      </div>
      <!-- 工艺数据库 -->
      <div class="nav-group">
        <div class="nav-group-header" @click="toggleGroup('process')">
          <div class="nav-group-title">
            <i class="fas fa-book"></i>
            <span>工艺数据库</span>
          </div>
          <i class="fas fa-chevron-down" :class="{ 'rotated': expandedGroups.process }"></i>
        </div>
        <div class="nav-group-content" v-show="expandedGroups.process">
          <!-- 工艺实例数据库 -->
          <div class="nav-sub-group">
            <div class="nav-sub-header" @click="toggleGroup('processInstances')">
              <span>工艺实例数据库</span>
              <i class="fas fa-chevron-down" :class="{ 'rotated': expandedGroups.processInstances }"></i>
            </div>
            <div class="nav-sub-content" v-show="expandedGroups.processInstances">
              <!-- 光整需求导入项目 -->
              <div class="nav-sub-sub-group">
                <div class="nav-sub-sub-header" @click="toggleGroup('polishingRequirements')">
                  <span>光整需求导入项目</span>
                  <i class="fas fa-chevron-down" :class="{ 'rotated': expandedGroups.polishingRequirements }"></i>
                </div>
                <div class="nav-sub-sub-content" v-show="expandedGroups.polishingRequirements">
                  <!-- 统计报表在光整需求导入项目下 -->
                  <div class="nav-sub-sub-group">
                    <div class="nav-sub-sub-header" @click="toggleGroup('statistics')">
                      <span>统计报表</span>
                      <i class="fas fa-chevron-down" :class="{ 'rotated': expandedGroups.statistics }"></i>
                    </div>
                    <div class="nav-sub-sub-content" v-show="expandedGroups.statistics">
                      <router-link to="/process/statistics/polishing-requirements" class="nav-sub-sub-item">
                        <span>光整需求统计</span>
                      </router-link>
                      <router-link to="/process/statistics/process-analysis" class="nav-sub-sub-item">
                        <span>工艺分析报表</span>
                      </router-link>
                      <router-link to="/process/statistics/efficiency" class="nav-sub-sub-item">
                        <span>效率统计报表</span>
                      </router-link>
                    </div>
                  </div>
                  <router-link to="/process/polishing/requirement-entry" class="nav-sub-sub-item">
                    <span>光整需求录入</span>
                  </router-link>
                  <router-link to="/process/polishing/requirement-management" class="nav-sub-sub-item">
                    <span>光整需求管理</span>
                  </router-link>
                  <router-link to="/process/polishing/requirement-analysis" class="nav-sub-sub-item">
                    <span>光整需求分析</span>
                  </router-link>
                </div>
              </div>
              
              <!-- 光整工艺录入（工艺师、管理员）作为并列的三级项目 -->
              <router-link to="/process/polishing/process-entry-engineering" class="nav-sub-item">
                <span>光整工艺录入（工艺师）</span>
              </router-link>
              <router-link to="/process/polishing/process-entry-admin" class="nav-sub-item">
                <span>光整工艺录入（管理员）</span>
              </router-link>
              
              <!-- 光整工艺审核作为并列的三级项目 -->
              <div class="nav-sub-sub-group">
                <div class="nav-sub-sub-header" @click="toggleGroup('processReview')">
                  <span>光整工艺审核</span>
                  <i class="fas fa-chevron-down" :class="{ 'rotated': expandedGroups.processReview }"></i>
                </div>
                <div class="nav-sub-sub-content" v-show="expandedGroups.processReview">
                  <router-link to="/process/review/pending" class="nav-sub-sub-item">
                    <span>待审核工艺</span>
                  </router-link>
                  <router-link to="/process/review/approved" class="nav-sub-sub-item">
                    <span>已审核工艺</span>
                  </router-link>
                  <router-link to="/process/review/rejected" class="nav-sub-sub-item">
                    <span>驳回工艺</span>
                  </router-link>
                </div>
              </div>
              
              <!-- 历史审核记录作为并列的三级项目 -->
              <div class="nav-sub-sub-group">
                <div class="nav-sub-sub-header" @click="toggleGroup('historyRecords')">
                  <span>历史审核记录</span>
                  <i class="fas fa-chevron-down" :class="{ 'rotated': expandedGroups.historyRecords }"></i>
                </div>
                <div class="nav-sub-sub-content" v-show="expandedGroups.historyRecords">
                  <router-link to="/process/history/all" class="nav-sub-sub-item">
                    <span>全部审核记录</span>
                  </router-link>
                  <router-link to="/process/history/by-date" class="nav-sub-sub-item">
                    <span>按日期查询</span>
                  </router-link>
                  <router-link to="/process/history/by-user" class="nav-sub-sub-item">
                    <span>按用户查询</span>
                  </router-link>
                </div>
              </div>
              
              <router-link to="/process/instances/management" class="nav-sub-item">
                <span>工艺案例管理</span>
              </router-link>
            </div>
          </div>
          
          <!-- 原有菜单项保持不变 -->
          <router-link to="/process/case-data" class="nav-item">
            <span>工艺案例数据库</span>
          </router-link>
          <router-link to="/process/expert" class="nav-item">
            <span>工艺专家知识库</span>
          </router-link>
          <router-link to="/process/analysis" class="nav-item">
            <span>工艺分析与评价</span>
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

const expandedGroups = reactive({
  system: true,
  base: false,
  material: false,
  process: false,
  analysis: false,
  processInstances: false,
  polishingRequirements: false,
  statistics: false,
  processReview: false,
  historyRecords: false
})

const toggleGroup = (groupName: keyof typeof expandedGroups) => {
  expandedGroups[groupName] = !expandedGroups[groupName]
}
</script>

<style scoped>
.navigation {
  width: 250px;
  height: 100vh;
  background-color: #2c3e50;
  color: #fff;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
}

.nav-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 1rem;
  color: #fff;
}

.nav-menu {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
}

.nav-group {
  margin: 0.5rem 0;
}

.nav-group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
  background-color: rgba(255, 255, 255, 0.05);
}

.nav-group-header:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-group-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
}

.nav-group-header .fas.fa-chevron-down {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  transition: transform 0.2s ease;
}

.nav-group-header .fas.fa-chevron-down.rotated {
  transform: rotate(180deg);
}

.nav-group-content {
  background-color: rgba(0, 0, 0, 0.1);
  border-left: 2px solid rgba(255, 255, 255, 0.1);
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1.5rem 0.75rem 2rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.2s;
  gap: 0.75rem;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.nav-item.router-link-active {
  background-color: rgba(255, 255, 255, 0.15);
  color: #fff;
  border-left: 4px solid #42b983;
}

.nav-item i {
  width: 1.25rem;
  text-align: center;
  font-size: 0.9rem;
}

.nav-sub-group {
  margin: 0.25rem 0;
}

.nav-sub-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 1.5rem 0.5rem 2rem;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.8);
}

.nav-sub-header:hover {
  background-color: rgba(255, 255, 255, 0.05);
  color: #fff;
}

.nav-sub-header .fas.fa-chevron-down {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.5);
  transition: transform 0.2s ease;
}

.nav-sub-header .fas.fa-chevron-down.rotated {
  transform: rotate(180deg);
}

.nav-sub-content {
  background-color: rgba(0, 0, 0, 0.15);
  border-left: 2px solid rgba(255, 255, 255, 0.05);
}

.nav-sub-item {
  display: flex;
  align-items: center;
  padding: 0.5rem 1.5rem 0.5rem 2.5rem;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.2s;
  font-size: 0.8rem;
}

.nav-sub-item:hover {
  background-color: rgba(255, 255, 255, 0.08);
  color: #fff;
}

.nav-sub-item.router-link-active {
  background-color: rgba(255, 255, 255, 0.12);
  color: #fff;
  border-left: 3px solid #42b983;
}

.nav-sub-sub-group {
  margin: 0.25rem 0;
}

.nav-sub-sub-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 1rem 0.5rem 2rem;
  cursor: pointer;
  transition: all 0.2s;
  background-color: rgba(255, 255, 255, 0.03);
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.8);
}

.nav-sub-sub-header:hover {
  background-color: rgba(255, 255, 255, 0.08);
  color: #fff;
}

.nav-sub-sub-header .fas.fa-chevron-down {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.5);
  transition: transform 0.2s ease;
}

.nav-sub-sub-header .fas.fa-chevron-down.rotated {
  transform: rotate(180deg);
}

.nav-sub-sub-content {
  background-color: rgba(0, 0, 0, 0.2);
  border-left: 2px solid rgba(255, 255, 255, 0.08);
  margin-left: 1rem;
}

.nav-sub-sub-item {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem 0.5rem 2.5rem;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.2s;
  font-size: 0.8rem;
  gap: 0.5rem;
}

.nav-sub-sub-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.nav-sub-sub-item.router-link-active {
  background-color: rgba(255, 255, 255, 0.15);
  color: #fff;
  border-left: 3px solid #42b983;
}

@media (max-width: 768px) {
  .navigation {
    width: 100%;
    height: auto;
    position: relative;
  }

  .nav-menu {
    padding: 0.5rem;
  }

  .nav-group-header {
    padding: 0.5rem 1rem;
  }

  .nav-item {
    padding: 0.5rem 1rem 0.5rem 1.5rem;
  }
}
</style> 