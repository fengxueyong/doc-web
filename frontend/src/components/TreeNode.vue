<template>
  <div class="tree-node">
    <div
      class="tree-item"
      :class="{ active: isActive, directory: node.type === 'directory' }"
      :style="{ paddingLeft: (depth * 16 + 12) + 'px' }"
      @click="handleClick"
    >
      <span class="tree-icon">
        <i v-if="node.type === 'directory'" :class="expanded ? 'fas fa-chevron-down' : 'fas fa-chevron-right'"></i>
        <i v-else class="fas fa-file-lines"></i>
      </span>
      <span class="tree-name" :title="node.name.replace('.md', '')">
        {{ displayName }}
      </span>
    </div>
    <div v-if="node.type === 'directory' && expanded && node.children" class="tree-children">
      <TreeNode
        v-for="child in node.children"
        :key="child.path"
        :node="child"
        :active-path="activePath"
        :depth="depth + 1"
        @select="(p) => $emit('select', p)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  node: { type: Object, required: true },
  activePath: { type: String, default: '' },
  depth: { type: Number, default: 0 }
})

const emit = defineEmits(['select'])

const expanded = ref(props.depth < 1)

const displayName = computed(() => {
  const name = props.node.name
  return props.node.type === 'file' ? name.replace(/\.md$/i, '') : name
})

const isActive = computed(() => {
  return props.node.type === 'file' && props.node.path === props.activePath
})

function handleClick() {
  if (props.node.type === 'directory') {
    expanded.value = !expanded.value
  } else {
    emit('select', props.node.path)
  }
}
</script>

<style scoped>
.tree-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  margin: 1px 0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #444;
  transition: all 0.12s;
  user-select: none;
}

.tree-item:hover {
  background: #eef2f5;
  color: #1a1a1a;
}

.tree-item.active {
  background: #e8f0fe;
  color: #1e6df2;
  font-weight: 600;
}

.tree-icon {
  width: 16px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  color: #999;
}

.tree-item.active .tree-icon {
  color: #1e6df2;
}

.tree-item.directory:hover .tree-icon {
  color: #666;
}

.tree-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
