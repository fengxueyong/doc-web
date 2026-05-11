import axios from 'axios'

const api = axios.create({
  baseURL: '/api'
})

export function fetchTree() {
  return api.get('/tree').then(res => res.data)
}

export function fetchContent(path) {
  return api.get('/content', { params: { path } }).then(res => res.data)
}

export function fetchMenus() {
  return api.get('/menus').then(res => res.data)
}

export function searchDocs(q) {
  return api.get('/search', { params: { q } }).then(res => res.data)
}
