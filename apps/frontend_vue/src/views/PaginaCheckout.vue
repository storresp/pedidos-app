<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import FormularioPedido from '../components/FormularioPedido.vue'
import ResumenCarrito from '../components/ResumenCarrito.vue'
import { carrito, vaciarCarrito } from '../store/carrito.js'

const router = useRouter()

const enviando = ref(false)
const enviado = ref(false)
const errorMsg = ref('')

const BASE_URL = 'http://localhost:8000/pedidos/api'

function volver() {
  router.push({ name: 'productos' })
}

// ── Aquí se hace el POST a la base de datos (Backend Django) ──
async function guardarPedidoEnBD(datosCliente) {
  if (!carrito.value || carrito.value.length === 0) {
    errorMsg.value = 'El carrito está vacío.'
    return
  }

  enviando.value = true
  errorMsg.value = ''

  try {
    // 1. Preparamos los items tal cual como necesita el backend: [{ product_id, quantity }]
    const items = carrito.value.map(p => ({
      product_id: Number(p.id),
      quantity: 1
    }))

    // 2. Realizamos la solicitud POST enviando: nombre, correo, e items.
    const res = await fetch(`${BASE_URL}/orders/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        nombre: datosCliente.nombre,
        correo: datosCliente.correo,
        items: items
      })
    })

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}))
      throw new Error(errData?.detail || `Error devuelto por el servidor (${res.status})`)
    }

    // 3. Resultado Exitoso
    enviado.value = true
    vaciarCarrito() // Limpiamos el carrito luego de guardalo en la base de datos

  } catch (err) {
    // 4. Manejo de errores
    console.error("Error al guardar pedido en BD:", err)
    errorMsg.value = err.message || 'Error al conectar con la base de datos.'
  } finally {
    enviando.value = false
  }
}
</script>

<template>
  <div class="checkout-page">

    <!-- Botón volver -->
    <div class="barra-nav">
      <button class="btn-volver" @click="volver" v-if="!enviado">← Volver a Productos</button>
      <button class="btn-volver btn-exito" @click="volver" v-else>← Hacer un nuevo pedido</button>
    </div>

    <!-- Layout: formulario izquierda + resumen derecha -->
    <div class="checkout-layout">

      <!-- Formulario de datos -->
      <div class="sección-formulario">
        <FormularioPedido
          :enviando="enviando"
          :enviado="enviado"
          :error-msg="errorMsg"
          @enviar="guardarPedidoEnBD"
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

.btn-exito {
  border-color: rgba(80, 220, 120, 0.4);
  color: #50dc78;
}
.btn-exito:hover {
  background: rgba(80, 220, 120, 0.1);
  color: #fff;
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
