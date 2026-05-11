<template>
  <div class="app">
    <DocHeader
      :menus="menus"
      :current-menu="currentMenu"
      @toggle-search="searchVisible = !searchVisible"
      @toggle-sidebar="sidebarVisible = !sidebarVisible"
      @select-menu="handleMenuSelect"
      @select-doc="selectDoc"
    />
    <div class="main-layout" :style="mainLayoutStyle">
      <Sidebar
        :visible="sidebarVisible"
        :active-path="activePath"
        :sidebar-width="sidebarWidth"
        @select="selectDoc"
        @close="sidebarVisible = false"
        @toggle="sidebarVisible = !sidebarVisible"
        @update:sidebar-width="onSidebarWidthUpdate"
      />
      <DocContent :doc-path="activePath" />
    </div>
    <SearchModal
      :visible="searchVisible"
      @close="searchVisible = false"
      @select="selectDoc"
    />
    <button
      v-if="!sidebarVisible"
      class="sidebar-toggle-float"
      @click="sidebarVisible = true"
      title="展开侧栏"
    >
      <span class="toggle-icon">
        <span class="hamburger-icon">
          <span class="h-line"></span>
          <span class="h-line"></span>
          <span class="h-line"></span>
        </span>
        <i class="fas fa-chevron-right"></i>
      </span>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import DocHeader from './components/DocHeader.vue'
import Sidebar from './components/Sidebar.vue'
import DocContent from './components/DocContent.vue'
import SearchModal from './components/SearchModal.vue'
import { fetchMenus } from './api/index.js'

const menus = ref([])
const currentMenu = ref('')
const activePath = ref('')
const sidebarVisible = ref(true)
const searchVisible = ref(false)

// Sidebar width state lifted up for layout coordination
const STORAGE_KEY = 'doc-web-sidebar-width'
const sidebarWidth = ref(280)

onMounted(async () => {
  try {
    const data = await fetchMenus()
    menus.value = data.menus || []
  } catch (e) {
    console.error('Failed to load menus:', e)
  }
  // Restore saved sidebar width
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      const w = parseInt(saved, 10)
      if (w >= 200 && w <= 500) sidebarWidth.value = w
    }
  } catch (e) {}
})

function onSidebarWidthUpdate(w) {
  sidebarWidth.value = w
  try { localStorage.setItem(STORAGE_KEY, String(w)) } catch (e) {}
}

function handleMenuSelect(menu) {
  currentMenu.value = menu.key
}

function selectDoc(path) {
  activePath.value = path
  if (window.innerWidth <= 768) {
    sidebarVisible.value = false
  }
}

const mainLayoutStyle = computed(() => {
  if (!sidebarVisible.value) return {}
  // On mobile the sidebar overlays full-width, no padding needed
  return { paddingLeft: sidebarWidth.value + 'px' }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #333;
  background: #f2f3f7;
}

.app {
  min-height: 100vh;
}

.main-layout {
  display: flex;
  padding-top: 64px;
  padding-left: 0;
  min-height: 100vh;
  background: #fff;
}

@media (max-width: 768px) {
  .main-layout {
    padding-left: 0 !important;
  }
}

.sidebar-toggle-float {
  position: fixed;
  top: 76px;
  left: 10px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  border: 1px solid #e2e6ed;
  border-radius: 10px;
  color: #7a8294;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  z-index: 85;
  transition: box-shadow 0.2s, color 0.2s, border-color 0.2s;
  font-size: 13px;
}

.sidebar-toggle-float:hover {
  color: #1e6df2;
  border-color: #1e6df2;
  box-shadow: 0 4px 12px rgba(30, 109, 242, 0.15);
}

@media (max-width: 768px) {
  .sidebar-toggle-float {
    top: 66px;
    width: 32px;
    height: 32px;
  }
}

.hamburger-icon {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 3px;
  width: 14px;
  pointer-events: none;
}

.toggle-icon {
  display: flex;
  align-items: center;
  gap: 2px;
  pointer-events: none;
}

.toggle-icon .fa-chevron-right {
  font-size: 11px;
}

.h-line {
  display: block;
  height: 2px;
  border-radius: 2px;
  background: currentColor;
}

.h-line:nth-child(1) { width: 100%; }
.h-line:nth-child(2) { width: 9px; }
.h-line:nth-child(3) { width: 100%; }
</style>