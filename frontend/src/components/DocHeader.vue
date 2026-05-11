<template>
  <header class="doc-header">
    <div class="header-bg"></div>
    <div class="header-inner">
      <div class="header-left">
        <div class="logo" @click="$emit('select-doc', '')">
          <!-- Open book logo -->
          <svg viewBox="0 0 36 36" width="36" height="36">
            <defs>
              <linearGradient id="hlg" x1="0" y1="0" x2="36" y2="36">
                <stop offset="0%" stop-color="#4f46e5"/>
                <stop offset="100%" stop-color="#7c3aed"/>
              </linearGradient>
            </defs>
            <path d="M4 8h13v21L4 27V8z" fill="url(#hlg)"/>
            <path d="M19 8h13v21L19 27V8z" fill="url(#hlg)" opacity="0.85"/>
            <line x1="18" y1="8" x2="18" y2="27" stroke="#fff" stroke-width="1.5" opacity="0.6"/>
            <line x1="8" y1="14" x2="14" y2="14" stroke="#fff" stroke-width="1.3" stroke-linecap="round" opacity="0.8"/>
            <line x1="8" y1="18" x2="14" y2="18" stroke="#fff" stroke-width="1.3" stroke-linecap="round" opacity="0.8"/>
            <line x1="8" y1="22" x2="13" y2="22" stroke="#fff" stroke-width="1.3" stroke-linecap="round" opacity="0.5"/>
            <line x1="22" y1="14" x2="28" y2="14" stroke="#fff" stroke-width="1.3" stroke-linecap="round" opacity="0.8"/>
            <line x1="22" y1="18" x2="28" y2="18" stroke="#fff" stroke-width="1.3" stroke-linecap="round" opacity="0.8"/>
            <line x1="22" y1="22" x2="27" y2="22" stroke="#fff" stroke-width="1.3" stroke-linecap="round" opacity="0.5"/>
          </svg>
          <span class="logo-text">知墨</span>
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
          <i :class="menu.icon" class="nav-icon"></i>
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
  height: 64px;
  font-family: 'Noto Serif SC', 'Songti SC', 'SimSun', 'STSong', serif;
  border-bottom: 1px solid rgba(79, 70, 229, 0.12);
  box-shadow: 0 2px 12px rgba(79, 70, 229, 0.06);
}

.header-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #eef1ff 0%, #e0e7ff 50%, #ede9fe 100%);
  z-index: -1;
}

/* Subtle decorative dots */
.header-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle at 20% 50%, rgba(79, 70, 229, 0.03) 1px, transparent 1px);
  background-size: 24px 24px;
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  height: 100%;
  padding: 0 24px;
  display: flex;
  align-items: center;
  gap: 32px;
  position: relative;
  z-index: 1;
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
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 2px;
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  font-size: 20px;
  font-weight: 600;
  color: #4a4a6a;
  border-radius: 8px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.15s;
  white-space: nowrap;
  letter-spacing: 0.5px;
}

.nav-item:hover {
  color: #4f46e5;
  background: rgba(79, 70, 229, 0.08);
}

.nav-item.active {
  color: #4f46e5;
  background: rgba(79, 70, 229, 0.1);
  font-weight: 600;
}

.nav-icon {
  font-size: 14px;
  width: 18px;
  text-align: center;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon-btn {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: rgba(79, 70, 229, 0.06);
  border-radius: 10px;
  color: #5a5a7a;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.15s;
}

.icon-btn:hover {
  background: rgba(79, 70, 229, 0.12);
  color: #4f46e5;
}

.sidebar-toggle {
  display: none;
}

@media (max-width: 768px) {
  .doc-header { height: 56px; }
  .header-inner { padding: 0 16px; gap: 16px; }
  .header-nav { gap: 0; overflow-x: auto; }
  .nav-item { padding: 6px 10px; font-size: 16px; }
  .sidebar-toggle { display: flex; }
}
</style>
