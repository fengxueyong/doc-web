<template>
  <div v-if="visible" class="search-overlay" @click.self="$emit('close')">
    <div class="search-modal">
      <div class="search-input-wrapper">
        <i class="fas fa-search"></i>
        <input
          ref="inputRef"
          v-model="query"
          type="text"
          placeholder="搜索文档..."
          class="search-input"
          @input="doSearch"
        />
        <button class="search-close" @click="$emit('close')">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="search-results">
        <div v-if="searching" class="search-status">
          <i class="fas fa-spinner fa-spin"></i> 搜索中...
        </div>
        <div v-else-if="query && results.length === 0" class="search-status">
          未找到匹配的文档
        </div>
        <a
          v-for="item in results"
          :key="item.path"
          class="search-result-item"
          @click="selectResult(item)"
        >
          <i class="fas fa-file-lines"></i>
          <span>{{ item.name }}</span>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { searchDocs } from '../api/index.js'

const props = defineProps({
  visible: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'select'])

const query = ref('')
const results = ref([])
const searching = ref(false)
const inputRef = ref(null)

watch(() => props.visible, async (val) => {
  if (val) {
    query.value = ''
    results.value = []
    await nextTick()
    inputRef.value?.focus()
  }
})

let searchTimer = null
async function doSearch() {
  if (searchTimer) clearTimeout(searchTimer)
  if (!query.value.trim()) {
    results.value = []
    return
  }
  searchTimer = setTimeout(async () => {
    searching.value = true
    try {
      const data = await searchDocs(query.value.trim())
      results.value = data.results || []
    } catch (e) {
      results.value = []
    } finally {
      searching.value = false
    }
  }, 300)
}

function selectResult(item) {
  emit('select', item.path)
  emit('close')
}
</script>

<style scoped>
.search-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 200;
  display: flex;
  justify-content: center;
  padding-top: 120px;
}

.search-modal {
  width: 100%;
  max-width: 560px;
  max-height: 60vh;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.search-input-wrapper {
  position: relative;
  padding: 16px 20px;
  border-bottom: 1px solid #e8edf2;
}

.search-input-wrapper i {
  position: absolute;
  left: 32px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
}

.search-input {
  width: 100%;
  padding: 10px 40px 10px 36px;
  border: 1px solid #e0e4e8;
  border-radius: 8px;
  font-size: 15px;
  outline: none;
  color: #333;
}

.search-input:focus {
  border-color: #1e6df2;
}

.search-close {
  position: absolute;
  right: 28px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 4px;
  font-size: 16px;
}

.search-results {
  flex: 1;
  overflow-y: auto;
  padding: 8px 0;
}

.search-status {
  padding: 32px;
  text-align: center;
  color: #999;
}

.search-result-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 24px;
  cursor: pointer;
  color: #333;
  font-size: 14px;
  text-decoration: none;
  transition: background 0.12s;
}

.search-result-item:hover {
  background: #f0f6ff;
  color: #1e6df2;
}

.search-result-item i {
  color: #999;
  width: 16px;
}
</style>
