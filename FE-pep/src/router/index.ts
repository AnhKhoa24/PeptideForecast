import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import About from '@/views/About.vue'
import History from '@/views/History.vue'
import Forecast from '@/views/Forecast.vue'
import FileForecast from '@/views/FileForecast.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/about', name: 'About', component: About },
  { path: '/history', name: 'Contact', component: History },
  { path: '/forecast', name: 'Forecast', component: Forecast },
  { path: '/fileforecast', name: 'FileForecast', component: FileForecast }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
