import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import About from '@/views/About.vue'
import History from '@/views/History.vue'
import Forecast from '@/views/Forecast.vue'
import FileForecast from '@/views/FileForecast.vue'
import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import Swal from 'sweetalert2'
const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/about', name: 'About', component: About },
  { path: '/history', name: 'History', component: History, meta: { requiresAuth: true } },
  { path: '/forecast', name: 'Forecast', component: Forecast },
  { path: '/fileforecast', name: 'FileForecast', component: FileForecast }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 🚧 Bảo vệ route cần đăng nhập
router.beforeEach(
  (to: RouteLocationNormalized, _from: RouteLocationNormalized, next: NavigationGuardNext) => {
    const token = localStorage.getItem('access_token')

    if (to.meta.requiresAuth && !token) {
      Swal.fire({
        icon: 'info',
        title: 'Bạn chưa đăng nhập',
        text: 'Vui lòng đăng nhập để truy cập trang này.',
        showConfirmButton: false,
        timer: 2000
      })
      return
      // return next('/') // Chuyển hướng về home (hoặc /login)
    }

    next() // Cho phép đi tiếp
  }
)

export default router
