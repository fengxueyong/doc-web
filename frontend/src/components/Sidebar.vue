<template>
  <aside
    class="sidebar"
    :class="{ collapsed: !visible, resizing: isDragging }"
    :style="{ width: visible ? sidebarWidth + 'px' : '0px' }"
  >
    <div class="sidebar-header">
      <h3 class="sidebar-title">文档目录</h3>
      <button class="toggle-inline" @click="$emit('toggle')" title="收起侧栏">
        <span class="toggle-icon">
          <span class="hamburger-icon">
            <span class="h-line"></span>
            <span class="h-line"></span>
            <span class="h-line"></span>
          </span>
          <i class="fas fa-chevron-left"></i>
        </span>
      </button>
    </div>
    <div class="sidebar-search">
      <i class="fas fa-search"></i>
      <input
        v-model="filterText"
        type="text"
        placeholder="过滤文档..."
        class="sidebar-filter-input"
      />
    </div>
    <div class="sidebar-tree">
      <div v-if="loading" class="sidebar-empty">
        <i class="fas fa-spinner fa-spin"></i> 加载中...
      </div>
      <div v-else-if="filteredCategories.length === 0" class="sidebar-empty">
        <i class="fas fa-folder-open"></i> 暂无文档
      </div>
      <div
        v-for="cat in filteredCategories"
        :key="cat.name"
        class="category-group"
      >
        <div class="category-header" @click="toggleCategory(cat.name)">
          <i :class="cat.icon" class="cat-icon"></i>
          <span class="cat-name" :title="cat.name">{{ cat.name }}</span>
          <i
            class="fas fa-chevron-down cat-chevron"
            :class="{ collapsed: !expanded.has(cat.name) }"
          ></i>
        </div>
        <div v-if="expanded.has(cat.name)" class="cat-children">
          <div
            v-for="doc in cat.children"
            :key="doc.path"
            class="cat-doc"
            :class="{ active: activePath === doc.path }"
            :title="displayName(doc.name)"
            @click="selectDoc(doc)"
          >
            <i class="fas fa-file-lines doc-icon"></i>
            <span class="doc-name">{{ displayName(doc.name) }}</span>
          </div>
        </div>
      </div>
    </div>
    <!-- Drag handle for resizing -->
    <div
      class="resize-handle"
      @mousedown.prevent="startResize"
    ></div>
  </aside>
  <div v-if="visible" class="sidebar-overlay" @click="$emit('close')"></div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'
import { fetchCategorizedTree } from '../api/index.js'

const props = defineProps({
  visible: { type: Boolean, default: true },
  activePath: { type: String, default: '' },
  sidebarWidth: { type: Number, default: 280 }
})

const emit = defineEmits(['select', 'close', 'toggle', 'update:sidebar-width'])

const categories = ref([])
const loading = ref(true)
const filterText = ref('')
const expanded = ref(new Set())

// Resizable state
const isDragging = ref(false)
let startX = 0
let startWidth = 280

function startResize(e) {
  isDragging.value = true
  startX = e.clientX
  startWidth = props.sidebarWidth
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopResize)
}

function onDrag(e) {
  if (!isDragging.value) return
  const diff = e.clientX - startX
  const newWidth = Math.min(500, Math.max(200, startWidth + diff))
  emit('update:sidebar-width', newWidth)
}

function stopResize() {
  isDragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopResize)
}

onUnmounted(stopResize)

function displayName(name) {
  return name.replace(/\.md$/i, '')
}

function toggleCategory(name) {
  if (expanded.value.has(name)) {
    expanded.value.delete(name)
  } else {
    expanded.value.add(name)
  }
  expanded.value = new Set(expanded.value)
}

async function loadCategories() {
  loading.value = true
  try {
    const data = await fetchCategorizedTree()
    categories.value = data.categories || []
    expanded.value = new Set(categories.value.map(c => c.name))
  } catch (e) {
    console.error('Failed to load categories:', e)
    categories.value = []
  } finally {
    loading.value = false
  }
}

watch(() => props.visible, (val) => {
  if (val && categories.value.length === 0) {
    loadCategories()
  }
})

if (props.visible) {
  loadCategories()
}

function selectDoc(doc) {
  emit('select', doc.path)
  if (window.innerWidth <= 768) {
    emit('close')
  }
}

function filterCategories(cats, query) {
  if (!query) return cats
  const q = query.toLowerCase()
  return cats
    .map(cat => {
      const matched = cat.children.filter(doc =>
        doc.name.toLowerCase().includes(q)
      )
      if (matched.length > 0 || cat.name.toLowerCase().includes(q)) {
        return { ...cat, children: matched }
      }
      return null
    })
    .filter(Boolean)
}

const filteredCategories = computed(() => filterCategories(categories.value, filterText.value))
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 64px;
  left: 0;
  bottom: 0;
  background: #eceef3;
  border-right: 1px solid #c8cdd6;
  box-shadow: 1px 0 8px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  z-index: 90;
  transition: transform 0.25s ease;
}

/* Disable transition while resizing for instant feedback */
.sidebar.resizing {
  transition: none;
  user-select: none;
}

.sidebar.collapsed {
  overflow: hidden;
}

.sidebar-overlay {
  display: none;
}

/* ---- Resize Handle ---- */
.resize-handle {
  position: absolute;
  top: 0;
  right: -4px;
  width: 8px;
  height: 100%;
  cursor: col-resize;
  z-index: 10;
  transition: background 0.15s;
}

.resize-handle:hover,
.sidebar.resizing .resize-handle {
  background: rgba(79, 70, 229, 0.2);
}

.resize-handle::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 2px;
  height: 32px;
  background: #c8cdd6;
  border-radius: 2px;
  transition: background 0.15s;
}

.resize-handle:hover::after,
.sidebar.resizing .resize-handle::after {
  background: #4f46e5;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px 12px;
}

.sidebar-title {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a1a;
  white-space: nowrap;
}

.toggle-inline {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #c8cdd6;
  border-radius: 8px;
  background: #f8f9fb;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.toggle-inline:hover {
  background: #fff;
  border-color: #4f46e5;
  color: #4f46e5;
  box-shadow: 0 2px 6px rgba(79, 70, 229, 0.12);
}

.toggle-icon {
  display: flex;
  align-items: center;
  gap: 2px;
  pointer-events: none;
}

.toggle-icon .fa-chevron-left {
  font-size: 11px;
}

.hamburger-icon {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 3px;
  width: 14px;
  pointer-events: none;
}

.h-line {
  display: block;
  height: 2px;
  border-radius: 2px;
  background: currentColor;
  transition: width 0.2s;
}

.h-line:nth-child(1) { width: 100%; }
.h-line:nth-child(2) { width: 9px; }
.h-line:nth-child(3) { width: 100%; }

.sidebar-search {
  position: relative;
  margin: 0 16px 12px;
}

.sidebar-search i {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  font-size: 13px;
}

.sidebar-filter-input {
  width: 100%;
  padding: 8px 12px 8px 32px;
  border: 1px solid #e0e4e8;
  border-radius: 8px;
  font-size: 13px;
  color: #333;
  background: #fff;
  outline: none;
  transition: border-color 0.15s;
}

.sidebar-filter-input:focus {
  border-color: #1e6df2;
}

.sidebar-tree {
  flex: 1;
  overflow-y: auto;
  padding: 0 8px 24px;
  min-width: 0;
}

.sidebar-empty {
  padding: 40px 20px;
  text-align: center;
  color: #999;
  font-size: 14px;
}

.sidebar-empty i {
  display: block;
  margin-bottom: 8px;
  font-size: 24px;
}

/* ---- Category ---- */
.category-group {
  margin-bottom: 2px;
}

.category-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.12s;
  user-select: none;
}

.category-header:hover {
  background: #eef2f5;
}

.cat-icon {
  width: 18px;
  font-size: 15px;
  color: #4f46e5;
  text-align: center;
  flex-shrink: 0;
}

.cat-name {
  flex: 1;
  font-size: 15px;
  font-weight: 600;
  color: #1a1a1a;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cat-count {
  font-size: 11px;
  color: #bbb;
  background: #eef2f5;
  padding: 1px 7px;
  border-radius: 10px;
  font-weight: 500;
  flex-shrink: 0;
}

.cat-chevron {
  font-size: 11px;
  color: #bbb;
  transition: transform 0.2s;
  flex-shrink: 0;
}

.cat-chevron.collapsed {
  transform: rotate(-90deg);
}

/* ---- Children ---- */
.cat-children {
  padding-left: 8px;
}

.cat-doc {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px 6px 28px;
  margin: 1px 0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #444;
  transition: all 0.12s;
  overflow: hidden;
}

.cat-doc:hover {
  background: #eef2f5;
  color: #1a1a1a;
}

.cat-doc.active {
  background: #e8f0fe;
  color: #1e6df2;
  font-weight: 600;
}

.doc-icon {
  width: 14px;
  font-size: 12px;
  color: #bbb;
  flex-shrink: 0;
}

.cat-doc.active .doc-icon {
  color: #1e6df2;
}

.doc-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (max-width: 768px) {
  .sidebar {
    top: 56px;
    width: 100% !important;
    max-width: 320px;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
  }
  .sidebar-overlay {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.3);
    z-index: 89;
  }
  .resize-handle {
    display: none;
  }
}
</style>
