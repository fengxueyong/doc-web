<template>
  <div class="doc-content" ref="contentRef">
    <div v-if="loading" class="content-status">
      <i class="fas fa-spinner fa-spin"></i>
      <p>加载中...</p>
    </div>
    <div v-else-if="error" class="content-status content-error">
      <i class="fas fa-exclamation-circle"></i>
      <p>{{ error }}</p>
    </div>
    <div v-else-if="!content" class="content-status content-welcome">
      <div class="welcome-icon">
        <svg viewBox="0 0 80 80" width="80" height="80">
          <rect width="80" height="80" rx="16" fill="#e8f0fe" />
          <path d="M24 28h32v4H24zm0 10h28v4H24zm0 10h24v4H24z" fill="#1e6df2" opacity="0.6" />
          <path d="M24 28h32v4H24zm0 10h28v4H24zm0 10h24v4H24z" fill="#1e6df2" opacity="0.3" transform="translate(0, 2)" />
        </svg>
      </div>
      <h2>欢迎使用 DocWeb</h2>
      <p>请从左侧文档目录中选择一篇文档开始阅读</p>
    </div>
    <div v-else class="markdown-body" v-html="renderedContent"></div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import { fetchContent } from '../api/index.js'
import '../styles/markdown.css'

const md = new MarkdownIt({
  html: true,
  breaks: true,
  linkify: true,
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return '<pre class="hljs"><code>' +
          hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
          '</code></pre>'
      } catch (__) {}
    }
    return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>'
  }
})

const props = defineProps({
  docPath: { type: String, default: '' }
})

const content = ref('')
const loading = ref(false)
const error = ref('')
const contentRef = ref(null)

const renderedContent = computed(() => {
  if (!content.value) return ''
  return md.render(content.value)
})

async function loadContent(path) {
  if (!path) {
    content.value = ''
    error.value = ''
    return
  }
  loading.value = true
  error.value = ''
  try {
    const data = await fetchContent(path)
    content.value = data.content
  } catch (e) {
    content.value = ''
    if (e.response && e.response.status === 404) {
      error.value = '文档未找到'
    } else {
      error.value = '加载文档失败，请稍后重试'
    }
  } finally {
    loading.value = false
  }
}

watch(() => props.docPath, (path) => {
  loadContent(path)
})
</script>

<style scoped>
.doc-content {
  flex: 1;
  min-height: calc(100vh - 60px);
  padding: 32px 48px 80px;
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
}

.content-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: #999;
  font-size: 15px;
  gap: 12px;
}

.content-status i {
  font-size: 32px;
}

.content-error {
  color: #e74c3c;
}

.content-welcome {
  color: #666;
}

.content-welcome h2 {
  font-size: 24px;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.content-welcome p {
  color: #999;
}

.welcome-icon {
  margin-bottom: 8px;
}

@media (max-width: 768px) {
  .doc-content {
    padding: 24px 20px 60px;
  }
}
</style>
