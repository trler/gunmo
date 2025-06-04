<template>
  <div class="main-layout">
    <Navigation class="nav-sidebar" />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import Navigation from '@/components/Navigation.vue'
</script>

<style scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
}

.nav-sidebar {
  flex-shrink: 0;
}

.main-content {
  flex: 1;
  padding: 2rem;
  margin-left: 250px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .main-layout {
    flex-direction: column;
  }

  .main-content {
    margin-left: 0;
    padding: 1rem;
  }
}
</style> 