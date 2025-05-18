import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'

import { useAuth } from './composables/useAuth'

const app = createApp(App)

const { saveToken, fetchUserInfo } = useAuth()

// Kiểm tra token sau khi Google redirect xong (nếu dùng dạng redirect)
const params = new URLSearchParams(window.location.search)
const token = params.get('access_token')
if (token) {
  saveToken(token)
  fetchUserInfo()
  window.history.replaceState({}, document.title, '/')
} else {
  fetchUserInfo()
}

app.use(router)
app.mount('#app')
