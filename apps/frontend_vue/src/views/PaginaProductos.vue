<script setup>
import { useRouter } from 'vue-router'
import Productos from '../components/productos.vue'
import ResumenCarrito from '../components/ResumenCarrito.vue'
import { carrito, agregarAlCarrito } from '../store/carrito.js'

const router = useRouter()

const listaProductos = [
  { id: 1, nombre: 'Laptop',    precio: 2500 },
  { id: 2, nombre: 'Mouse',     precio: 80   },
  { id: 3, nombre: 'Teclado',   precio: 150  },
  { id: 4, nombre: 'Monitor',   precio: 900  },
  { id: 5, nombre: 'Audífonos', precio: 200  },
  { id: 6, nombre: 'Webcam',    precio: 120  }
]

function irACheckout() {
  router.push({ name: 'checkout' })
}
</script>

<template>
  <div class="layout-principal">

    <!-- Grid de productos -->
    <div class="grid-productos">
      <Productos
        v-for="producto in listaProductos"
        :key="producto.id"
        :nombre="producto.nombre"
        :precio="producto.precio"
        @agregar="agregarAlCarrito"
      />
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

.grid-productos {
  flex: 1;
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
</style>
