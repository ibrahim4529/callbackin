import { createApp } from 'vue'
import { createHead } from "@vueuse/head"
import './style.scss'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import routes from '~pages'
const head = createHead()

const router = createRouter({
    history: createWebHistory(),
    routes,
})
const app = createApp(App)
app.use(router)
app.use(head)
app.mount('#app')
