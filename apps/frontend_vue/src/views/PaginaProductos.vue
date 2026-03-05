<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Productos from '../components/productos.vue'
import ResumenCarrito from '../components/ResumenCarrito.vue'
import { carrito, agregarAlCarrito } from '../store/carrito.js'

const router = useRouter()

const listaProductos = ref([])
const cargando = ref(true)
const errorProductos = ref('')

// Si estamos en desarrollo local apunta a localhost:8000, 
// si estamos en producción/Kubernetes usa la ruta relativa controlada por Ingress
const BASE_URL = import.meta.env.DEV ? 'http://localhost:8000/pedidos/api' : '/pedidos/api'

async function cargarProductos() {
  cargando.value = true
  errorProductos.value = ''
  try {
    const res = await fetch(`${BASE_URL}/products/`)
    if (!res.ok) throw new Error(`Error ${res.status}`)
    const data = await res.json()
    // La API devuelve { id, name, price, is_active, created_at }
    // Filtramos solo los activos y mapeamos al formato interno
    listaProductos.value = data
      .filter(p => p.is_active)
      .map(p => ({
        id: p.id,
        nombre: p.name,
        precio: parseFloat(p.price)
      }))
  } catch (e) {
    errorProductos.value = 'No se pudieron cargar los productos. ¿Está el servidor activo?'
  } finally {
    cargando.value = false
  }
}

function irACheckout() {
  router.push({ name: 'checkout' })
}

onMounted(cargarProductos)
</script>

<template>
  <div class="layout-principal">

    <!-- Grid de productos -->
    <div class="grid-area">

      <!-- Estado: cargando -->
      <div v-if="cargando" class="estado-carga">
        <div class="spinner"></div>
        <p>Cargando productos...</p>
      </div>

      <!-- Estado: error -->
      <div v-else-if="errorProductos" class="estado-error">
        <span>⚠️</span>
        <p>{{ errorProductos }}</p>
        <button class="btn-reintentar" @click="cargarProductos">🔄 Reintentar</button>
      </div>

      <!-- Grid normal -->
      <div v-else class="grid-productos">
        <Productos
          v-for="producto in listaProductos"
          :key="producto.id"
          :id="producto.id"
          :nombre="producto.nombre"
          :precio="producto.precio"
          @agregar="agregarAlCarrito"
        />
      </div>
    </div>

    <!-- Sidebar del carrito -->
    <aside class="sidebar-carrito">
      <ResumenCarrito
        :productos="carrito"
        @continuar="irACheckout"
      />
    </aside>

  </div>
</template>

<style scoped>
.layout-principal {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 1.5rem;
  padding: 2rem;
}

.grid-area {
  flex: 1;
}

.grid-productos {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.2rem;
}

.sidebar-carrito {
  width: 260px;
  flex-shrink: 0;
  position: sticky;
  top: 1.5rem;
  margin-right: 1rem;
}

/* ── Estado de carga ── */
.estado-carga,
.estado-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.95rem;
  text-align: center;
}

.estado-error { color: #ff7b7b; }

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 200, 80, 0.15);
  border-top-color: #ffc850;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.btn-reintentar {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 200, 80, 0.3);
  border-radius: 8px;
  color: #ffc850;
  padding: 8px 16px;
  font-size: 0.88rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-reintentar:hover {
  background: rgba(255, 200, 80, 0.1);
}
</style>
