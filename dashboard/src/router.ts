import { createRouter, createWebHistory } from 'vue-router'
import routes from '~pages'
import { useLocalStorage } from '@vueuse/core'


const router = createRouter({
    history: createWebHistory(),
    routes,
})

const isAuthed = () => {
    const token = useLocalStorage('token', null)
    return !!token.value
}

router.beforeEach((to, _, next) => {
    if (to.path === '/login' && isAuthed()) {
        next({ path: '/dashboard' })
    }
    else if (to.meta.requiresAuth && !isAuthed()) {
        next({ path: '/login' })
    }
    next()
})

export default router