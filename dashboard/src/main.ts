import { createApp } from 'vue'
import { createHead } from "@vueuse/head"
import './style.css'
import App from './App.vue'
const head = createHead()
import router from './router'

const app = createApp(App)
app.use(router)
app.use(head)
app.mount('#app')
