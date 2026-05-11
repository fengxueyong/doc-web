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
    <div class="main-layout">
      <Sidebar
        :visible="sidebarVisible"
        :active-path="activePath"
        @select="selectDoc"
        @close="sidebarVisible = false"
      />
      <DocContent :doc-path="activePath" />
    </div>
    <SearchModal
      :visible="searchVisible"
      @close="searchVisible = false"
      @select="selectDoc"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
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

onMounted(async () => {
  try {
    const data = await fetchMenus()
    menus.value = data.menus || []
  } catch (e) {
    console.error('Failed to load menus:', e)
  }
})

function handleMenuSelect(menu) {
  currentMenu.value = menu.key
  // Menus can be used to filter the sidebar or navigate to a section
  // For now, just set the active menu highlight
}

function selectDoc(path) {
  activePath.value = path
  // On mobile, close sidebar after selection
  if (window.innerWidth <= 768) {
    sidebarVisible.value = false
  }
}
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
  background: #fff;
}

.app {
  min-height: 100vh;
}

.main-layout {
  display: flex;
  padding-top: 60px;
  min-height: 100vh;
}
</style>
