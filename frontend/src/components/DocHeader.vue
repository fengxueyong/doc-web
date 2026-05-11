<template>
  <header class="doc-header">
    <div class="header-inner">
      <div class="header-left">
        <div class="logo" @click="$emit('select-doc', '')">
          <svg viewBox="0 0 36 36" width="36" height="36">
            <rect width="36" height="36" rx="9" fill="#1e6df2" />
            <text x="18" y="24" text-anchor="middle" fill="white" font-size="20" font-weight="bold">D</text>
          </svg>
          <span class="logo-text">DocWeb</span>
        </div>
      </div>
      <nav class="header-nav">
        <a
          v-for="menu in menus"
          :key="menu.key"
          class="nav-item"
          :class="{ active: currentMenu === menu.key }"
          @click="selectMenu(menu)"
        >
          {{ menu.label }}
        </a>
      </nav>
      <div class="header-right">
        <button class="icon-btn search-btn" @click="$emit('toggle-search')" title="搜索">
          <i class="fas fa-search"></i>
        </button>
        <button class="icon-btn sidebar-toggle" @click="$emit('toggle-sidebar')" title="切换侧边栏">
          <i class="fas fa-bars"></i>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
defineProps({
  menus: { type: Array, default: () => [] },
  currentMenu: { type: String, default: '' }
})

const emit = defineEmits(['toggle-search', 'toggle-sidebar', 'select-menu', 'select-doc'])

function selectMenu(menu) {
  emit('select-menu', menu)
}
</script>

<style scoped>
.doc-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #e8edf2;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  height: 100%;
  padding: 0 24px;
  display: flex;
  align-items: center;
  gap: 32px;
}

.header-left {
  flex-shrink: 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: #1a1a1a;
  letter-spacing: -0.3px;
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
}

.nav-item {
  padding: 8px 14px;
  font-size: 14px;
  font-weight: 500;
  color: #555;
  border-radius: 6px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.15s;
  white-space: nowrap;
}

.nav-item:hover {
  color: #1e6df2;
  background: #f0f6ff;
}

.nav-item.active {
  color: #1e6df2;
  background: #f0f6ff;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  border-radius: 8px;
  color: #666;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.15s;
}

.icon-btn:hover {
  background: #f0f6ff;
  color: #1e6df2;
}

.sidebar-toggle {
  display: none;
}

@media (max-width: 768px) {
  .header-inner { padding: 0 16px; gap: 16px; }
  .header-nav { gap: 0; overflow-x: auto; }
  .nav-item { padding: 6px 10px; font-size: 13px; }
  .sidebar-toggle { display: flex; }
}
</style>
