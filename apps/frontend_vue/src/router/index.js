import { createRouter, createWebHistory } from 'vue-router'
import PaginaProductos from '../views/PaginaProductos.vue'
import PaginaCheckout from '../views/PaginaCheckout.vue'
import PaginaAdmin from '../views/PaginaAdmin.vue'

const routes = [
    {
        path: '/',
        name: 'productos',
        component: PaginaProductos
    },
    {
        path: '/checkout',
        name: 'checkout',
        component: PaginaCheckout
    },
    {
        // Endpoint exclusivo para administradores
        path: '/admin',
        name: 'admin',
        component: PaginaAdmin
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
