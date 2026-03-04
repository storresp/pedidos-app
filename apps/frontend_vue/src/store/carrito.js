// store/carrito.js
// Estado global del carrito compartido entre PaginaProductos y PaginaCheckout
import { ref } from 'vue'

export const carrito = ref([])

export function agregarAlCarrito(producto) {
    carrito.value.push(producto)
}

export function vaciarCarrito() {
    carrito.value = []
}
