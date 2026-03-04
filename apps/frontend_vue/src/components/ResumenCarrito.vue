<script setup>
import { computed } from 'vue'

const props = defineProps({
  productos: Array,
  // En PaginaCheckout se pasa como true para ocultar el botón "Continuar"
  modoSoloLectura: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['continuar'])

const total = computed(() =>
  props.productos.reduce((acc, p) => acc + p.precio, 0)
)
</script>

<template>
  <div class="resumen-container">
    <div class="resumen-header">
      <span class="resumen-icon">🛒</span>
      <h2 class="resumen-titulo">Tu Pedido</h2>
    </div>

    <div class="resumen-body">
      <div v-if="productos.length === 0" class="vacio">
        <span class="vacio-icon">📭</span>
        <p>Tu carrito está vacío</p>
      </div>

      <div v-else class="lista-items">
        <div v-for="(p, i) in productos" :key="i" class="item">
          <span class="item-nombre">{{ p.nombre }}</span>
          <span class="item-precio">${{ p.precio.toLocaleString() }}</span>
        </div>
      </div>
    </div>

    <div class="resumen-footer">
      <div class="total-fila" v-if="productos.length > 0">
        <span class="total-label">Total</span>
        <span class="total-valor">${{ total.toLocaleString() }}</span>
      </div>

      <!-- Botón oculto en modo solo lectura (página checkout) -->
      <button
        v-if="!modoSoloLectura"
        class="btn-finalizar"
        :disabled="productos.length === 0"
        @click="emit('continuar')"
      >
        Continuar →
      </button>
    </div>
  </div>
</template>

<style scoped>
.resumen-container {
  width: 100%;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 200, 80, 0.25);
  border-radius: 18px;
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.resumen-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1.2rem 1.2rem 0.8rem;
  border-bottom: 1px solid rgba(255, 200, 80, 0.15);
}

.resumen-icon { font-size: 1.4rem; }

.resumen-titulo {
  font-size: 1.1rem;
  font-weight: 700;
  color: #ffc850;
  letter-spacing: 0.5px;
}

.resumen-body {
  flex: 1;
  padding: 0.8rem 1.2rem;
  min-height: 140px;
}

.vacio {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  height: 100px;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.9rem;
}

.vacio-icon { font-size: 2rem; }

.lista-items {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 8px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  font-size: 0.88rem;
}

.item-nombre { color: rgba(255, 255, 255, 0.85); font-weight: 500; }
.item-precio { color: #ffc850; font-weight: 700; }

.resumen-footer {
  padding: 0.8rem 1.2rem 1.2rem;
  border-top: 1px solid rgba(255, 200, 80, 0.15);
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.total-fila {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.total-label {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 600;
}

.total-valor {
  font-size: 1.3rem;
  font-weight: 800;
  color: #ffc850;
  text-shadow: 0 0 10px rgba(255, 200, 80, 0.4);
}

.btn-finalizar {
  width: 100%;
  background: linear-gradient(90deg, #7b2ff7, #e040fb);
  border: none;
  padding: 11px 0;
  border-radius: 12px;
  color: white;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.15s;
  letter-spacing: 0.4px;
}

.btn-finalizar:hover:not(:disabled) {
  opacity: 0.88;
  transform: scale(1.02);
}

.btn-finalizar:disabled {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.3);
  cursor: not-allowed;
}
</style>