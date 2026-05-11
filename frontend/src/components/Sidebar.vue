<template>
  <aside class="sidebar" :class="{ collapsed: !visible }">
    <div class="sidebar-header">
      <h3 class="sidebar-title">文档目录</h3>
      <button class="icon-btn" @click="$emit('close')" title="收起">
        <i class="fas fa-times"></i>
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
      <div v-else-if="filteredTree.length === 0" class="sidebar-empty">
        <i class="fas fa-folder-open"></i> 暂无文档
      </div>
      <TreeNode
        v-for="node in filteredTree"
        :key="node.path"
        :node="node"
        :active-path="activePath"
        :depth="0"
        @select="(path) => $emit('select', path)"
      />
    </div>
  </aside>
  <div v-if="visible" class="sidebar-overlay" @click="$emit('close')"></div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { fetchTree } from '../api/index.js'
import TreeNode from './TreeNode.vue'

const props = defineProps({
  visible: { type: Boolean, default: true },
  activePath: { type: String, default: '' }
})

const emit = defineEmits(['select', 'close'])

const tree = ref([])
const loading = ref(true)
const filterText = ref('')

async function loadTree() {
  loading.value = true
  try {
    const data = await fetchTree()
    tree.value = data.tree || []
  } catch (e) {
    console.error('Failed to load tree:', e)
    tree.value = []
  } finally {
    loading.value = false
  }
}

watch(() => props.visible, (val) => {
  if (val && tree.value.length === 0) {
    loadTree()
  }
})

// Load on first mount if visible
if (props.visible) {
  loadTree()
}

function filterNodes(nodes, query) {
  if (!query) return nodes
  const q = query.toLowerCase()
  const result = []
  for (const node of nodes) {
    if (node.type === 'file') {
      if (node.name.toLowerCase().includes(q)) {
        result.push(node)
      }
    } else if (node.type === 'directory') {
      const filteredChildren = filterNodes(node.children || [], q)
      if (filteredChildren.length > 0 || node.name.toLowerCase().includes(q)) {
        result.push({ ...node, children: filteredChildren })
      }
    }
  }
  return result
}

const filteredTree = computed(() => filterNodes(tree.value, filterText.value))
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 60px;
  left: 0;
  bottom: 0;
  width: 280px;
  background: #fafbfc;
  border-right: 1px solid #e8edf2;
  display: flex;
  flex-direction: column;
  z-index: 90;
  transition: transform 0.25s ease;
}

.sidebar.collapsed {
  transform: translateX(-100%);
}

.sidebar-overlay {
  display: none;
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
}

.icon-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  border-radius: 6px;
  color: #999;
  cursor: pointer;
  transition: all 0.15s;
}

.icon-btn:hover {
  background: #e8edf2;
  color: #555;
}

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

@media (max-width: 768px) {
  .sidebar {
    width: 100%;
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
}
</style>
