<script setup>
import { useRouter } from 'vue-router'
import FormularioPedido from '../components/FormularioPedido.vue'
import ResumenCarrito from '../components/ResumenCarrito.vue'
import { carrito, vaciarCarrito } from '../store/carrito.js'

const router = useRouter()

function volver() {
  router.push({ name: 'productos' })
}

function pedidoConfirmado(datos) {
  // datos = { nombre, correo }
  // El formulario ya guardó (o simuló guardar) el pedido.
  // Aquí puedes vaciar el carrito después de confirmar.
  vaciarCarrito()
}
</script>

<template>
  <div class="checkout-page">

    <!-- Botón volver -->
    <div class="barra-nav">
      <button class="btn-volver" @click="volver">← Volver a Productos</button>
    </div>

    <!-- Layout: formulario izquierda + resumen derecha -->
    <div class="checkout-layout">

      <!-- Formulario de datos -->
      <div class="sección-formulario">
        <FormularioPedido
          :productos="carrito"
          @enviar="pedidoConfirmado"
        />
      </div>

      <!-- Resumen del pedido -->
      <aside class="sección-resumen">
        <ResumenCarrito
          :productos="carrito"
          :modo-solo-lectura="true"
        />
      </aside>

    </div>
  </div>
</template>

<style scoped>
.checkout-page {
  padding: 1.5rem 2rem 3rem;
  min-height: calc(100vh - 120px);
}

/* Botón volver */
.barra-nav {
  margin-bottom: 1.8rem;
}

.btn-volver {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 200, 80, 0.25);
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.75);
  padding: 9px 18px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.btn-volver:hover {
  background: rgba(255, 200, 80, 0.1);
  color: #ffc850;
}

/* Layout dos columnas */
.checkout-layout {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 1.5rem;
}

/* Formulario: ocupa el espacio restante */
.sección-formulario {
  flex: 1;
}

/* Resumen: sidebar fijo */
.sección-resumen {
  width: 280px;
  flex-shrink: 0;
  position: sticky;
  top: 1.5rem;
  margin-right: 1rem;
}
</style>
