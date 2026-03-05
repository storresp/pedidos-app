<script setup>
import { ref, onMounted, computed } from 'vue'

const BASE_URL = 'http://localhost:8000/pedidos/api'

const pedidos    = ref([])
const cargando   = ref(true)
const errorMsg   = ref('')
const busqueda   = ref('')
const pedidoAbierto = ref(null)  // ID del pedido con detalle expandido

// ── Normalizar respuesta de la API al formato interno ──────────────
// La API devuelve:
// { id, customer: { name, email }, items: [{ product: { name, price }, quantity, unit_price, line_total }], total, created_at }
// Lo mapeamos a: { id, nombre, correo, fecha, productos: [{ nombre, precio }], total }
function normalizarPedido(p) {
  return {
    id: p.id,
    nombre: p.customer?.name ?? '—',
    correo: p.customer?.email ?? '—',
    fecha: p.created_at,
    status: p.status,
    total: parseFloat(p.total),
    productos: (p.items ?? []).map(item => ({
      nombre: item.product?.name ?? '—',
      precio: parseFloat(item.unit_price),
      cantidad: item.quantity,
    }))
  }
}

// ── Totales calculados por pedido ──────────────────────────────────
function totalPedido(productos) {
  return productos.reduce((acc, p) => acc + p.precio * p.cantidad, 0)
}

// ── Filtro de búsqueda por nombre o correo ─────────────────────────
const pedidosFiltrados = computed(() => {
  const q = busqueda.value.toLowerCase().trim()
  if (!q) return pedidos.value
  return pedidos.value.filter(p =>
    p.nombre.toLowerCase().includes(q) ||
    p.correo.toLowerCase().includes(q)
  )
})

// ── Estadísticas del header ────────────────────────────────────────
const totalPedidos  = computed(() => pedidos.value.length)
const totalIngresos = computed(() =>
  pedidos.value.reduce((acc, p) => acc + p.total, 0)
)

// ── Formato de fecha ───────────────────────────────────────────────
function formatFecha(iso) {
  return new Date(iso).toLocaleString('es-ES', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

// ── Badge de status ────────────────────────────────────────────────
const statusClases = {
  PENDING:   'badge-pending',
  PAID:      'badge-paid',
  CANCELLED: 'badge-cancelled',
}
const statusLabels = {
  PENDING:   'Pendiente',
  PAID:      'Pagado',
  CANCELLED: 'Cancelado',
}

// ── Carga de pedidos desde la API ──────────────────────────────────
async function cargarPedidos() {
  cargando.value = true
  errorMsg.value = ''

  try {
    const res = await fetch(`${BASE_URL}/orders/`)
    if (!res.ok) throw new Error(`Error ${res.status}`)
    const data = await res.json()
    pedidos.value = data.map(normalizarPedido)
  } catch (e) {
    errorMsg.value = 'No se pudo conectar con el servidor. ¿Está el backend activo?'
  } finally {
    cargando.value = false
  }
}

function toggleDetalle(id) {
  pedidoAbierto.value = pedidoAbierto.value === id ? null : id
}

onMounted(cargarPedidos)
</script>

<template>
  <div class="admin-page">

    <!-- Título de sección -->
    <div class="admin-header">
      <div class="admin-titulo-bloque">
        <span class="admin-badge">ADMIN</span>
        <h2 class="admin-titulo">Panel de Pedidos</h2>
      </div>

      <!-- Tarjetas de estadísticas -->
      <div class="stats-cards">
        <div class="stat-card">
          <span class="stat-valor">{{ totalPedidos }}</span>
          <span class="stat-label">Pedidos totales</span>
        </div>
        <div class="stat-card destacada">
          <span class="stat-valor">${{ totalIngresos.toLocaleString() }}</span>
          <span class="stat-label">Ingresos totales</span>
        </div>
      </div>
    </div>

    <!-- Barra de búsqueda y refrescar -->
    <div class="toolbar">
      <input
        v-model="busqueda"
        type="text"
        placeholder="🔍 Buscar por nombre o correo..."
        class="input-busqueda"
      />
      <button class="btn-refrescar" @click="cargarPedidos" :disabled="cargando">
        {{ cargando ? '⏳ Cargando...' : '🔄 Refrescar' }}
      </button>
    </div>

    <!-- Estado: cargando -->
    <div v-if="cargando" class="estado-msg">
      <div class="spinner"></div>
      <p>Cargando pedidos...</p>
    </div>

    <!-- Estado: error -->
    <div v-else-if="errorMsg" class="estado-msg error">
      <span class="estado-icon">⚠️</span>
      <p>{{ errorMsg }}</p>
    </div>

    <!-- Estado: sin resultados -->
    <div v-else-if="pedidosFiltrados.length === 0" class="estado-msg">
      <span class="estado-icon">📭</span>
      <p>No se encontraron pedidos.</p>
    </div>

    <!-- Tabla de pedidos -->
    <div v-else class="tabla-wrapper">
      <table class="tabla-pedidos">
        <thead>
          <tr>
            <th>#</th>
            <th>Cliente</th>
            <th>Correo</th>
            <th>Fecha</th>
            <th>Status</th>
            <th>Productos</th>
            <th>Total</th>
            <th>Detalle</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="pedido in pedidosFiltrados" :key="pedido.id">
            <!-- Fila principal -->
            <tr class="fila-pedido" @click="toggleDetalle(pedido.id)">
              <td class="celda-id">#{{ pedido.id }}</td>
              <td class="celda-nombre">{{ pedido.nombre }}</td>
              <td class="celda-correo">{{ pedido.correo }}</td>
              <td class="celda-fecha">{{ formatFecha(pedido.fecha) }}</td>
              <td>
                <span class="badge-status" :class="statusClases[pedido.status]">
                  {{ statusLabels[pedido.status] ?? pedido.status }}
                </span>
              </td>
              <td class="celda-count">
                <span class="badge-count">{{ pedido.productos.length }} items</span>
              </td>
              <td class="celda-total">${{ pedido.total.toLocaleString() }}</td>
              <td class="celda-accion">
                <span class="chevron" :class="{ abierto: pedidoAbierto === pedido.id }">▼</span>
              </td>
            </tr>

            <!-- Fila de detalle expandible -->
            <tr v-if="pedidoAbierto === pedido.id" class="fila-detalle">
              <td colspan="8">
                <div class="detalle-container">
                  <p class="detalle-titulo">Productos del pedido:</p>
                  <div class="detalle-items">
                    <div v-for="(p, i) in pedido.productos" :key="i" class="detalle-item">
                      <span class="detalle-nombre">{{ p.nombre }}</span>
                      <span class="detalle-qty">x{{ p.cantidad }}</span>
                      <span class="detalle-precio">${{ (p.precio * p.cantidad).toLocaleString() }}</span>
                    </div>
                  </div>
                  <div class="detalle-total">
                    <span>Total del pedido:</span>
                    <span class="detalle-total-valor">${{ pedido.total.toLocaleString() }}</span>
                  </div>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

  </div>
</template>

<style scoped>
.admin-page {
  padding: 2rem;
  min-height: calc(100vh - 120px);
}

/* ─── Header del admin ─── */
.admin-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1.8rem;
}

.admin-titulo-bloque {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.admin-badge {
  background: linear-gradient(90deg, #7b2ff7, #e040fb);
  color: white;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  padding: 4px 10px;
  border-radius: 6px;
}

.admin-titulo {
  font-size: 1.8rem;
  font-weight: 800;
  color: #ffc850;
  text-shadow: 0 0 16px rgba(255, 200, 80, 0.4);
}

/* ─── Stats cards ─── */
.stats-cards {
  display: flex;
  gap: 1rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 200, 80, 0.2);
  border-radius: 14px;
  padding: 1rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
  backdrop-filter: blur(6px);
  min-width: 130px;
  text-align: center;
}

.stat-card.destacada {
  border-color: rgba(255, 200, 80, 0.5);
  background: rgba(255, 200, 80, 0.07);
}

.stat-valor {
  font-size: 1.6rem;
  font-weight: 800;
  color: #ffc850;
}

.stat-label {
  font-size: 0.78rem;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: 0.3px;
}

/* ─── Toolbar ─── */
.toolbar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.input-busqueda {
  flex: 1;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 200, 80, 0.2);
  border-radius: 10px;
  padding: 11px 16px;
  font-size: 0.95rem;
  color: #fff;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input-busqueda::placeholder { color: rgba(255, 255, 255, 0.3); }

.input-busqueda:focus {
  border-color: rgba(255, 200, 80, 0.55);
  box-shadow: 0 0 0 3px rgba(255, 200, 80, 0.08);
}

.btn-refrescar {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 200, 80, 0.25);
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.8);
  padding: 10px 20px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  white-space: nowrap;
}

.btn-refrescar:hover:not(:disabled) {
  background: rgba(255, 200, 80, 0.1);
  color: #ffc850;
}

.btn-refrescar:disabled { opacity: 0.5; cursor: not-allowed; }

/* ─── Estados ─── */
.estado-msg {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 4rem 0;
  color: rgba(255, 255, 255, 0.45);
  font-size: 1rem;
}

.estado-msg.error { color: #ff7b7b; }
.estado-icon { font-size: 2.5rem; }

/* Spinner */
.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 200, 80, 0.15);
  border-top-color: #ffc850;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ─── Tabla ─── */
.tabla-wrapper {
  overflow-x: auto;
  border-radius: 16px;
  border: 1px solid rgba(255, 200, 80, 0.2);
  backdrop-filter: blur(8px);
}

.tabla-pedidos {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.92rem;
}

thead tr {
  background: rgba(255, 200, 80, 0.08);
}

th {
  padding: 14px 16px;
  text-align: left;
  font-size: 0.78rem;
  font-weight: 700;
  color: rgba(255, 200, 80, 0.8);
  letter-spacing: 0.8px;
  text-transform: uppercase;
  border-bottom: 1px solid rgba(255, 200, 80, 0.15);
}

/* Filas de datos */
.fila-pedido {
  cursor: pointer;
  transition: background 0.15s;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.fila-pedido:hover {
  background: rgba(123, 47, 247, 0.15);
}

td {
  padding: 14px 16px;
  color: rgba(255, 255, 255, 0.82);
  vertical-align: middle;
}

.celda-id      { color: rgba(255, 255, 255, 0.4); font-size: 0.82rem; }
.celda-nombre  { font-weight: 600; color: #fff; }
.celda-correo  { color: rgba(255, 255, 255, 0.6); font-size: 0.88rem; }
.celda-fecha   { color: rgba(255, 255, 255, 0.5); font-size: 0.85rem; }
.celda-total   { color: #ffc850; font-weight: 700; }

/* ─── Badge status ─── */
.badge-status {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  padding: 3px 10px;
  border-radius: 20px;
}

.badge-pending {
  background: rgba(255, 200, 80, 0.15);
  color: #ffc850;
  border: 1px solid rgba(255, 200, 80, 0.4);
}

.badge-paid {
  background: rgba(80, 220, 120, 0.15);
  color: #50dc78;
  border: 1px solid rgba(80, 220, 120, 0.4);
}

.badge-cancelled {
  background: rgba(255, 80, 80, 0.15);
  color: #ff7b7b;
  border: 1px solid rgba(255, 80, 80, 0.4);
}

.badge-count {
  background: rgba(123, 47, 247, 0.3);
  border: 1px solid rgba(123, 47, 247, 0.5);
  border-radius: 20px;
  padding: 3px 10px;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.75);
}

.celda-accion { text-align: center; }

.chevron {
  display: inline-block;
  color: rgba(255, 200, 80, 0.5);
  font-size: 0.75rem;
  transition: transform 0.25s ease;
}

.chevron.abierto { transform: rotate(180deg); color: #ffc850; }

/* ─── Fila de detalle expandible ─── */
.fila-detalle td {
  padding: 0;
  background: rgba(0, 0, 0, 0.2);
}

.detalle-container {
  padding: 1rem 1.5rem 1.2rem 2rem;
  border-bottom: 1px solid rgba(255, 200, 80, 0.1);
}

.detalle-titulo {
  font-size: 0.8rem;
  color: rgba(255, 200, 80, 0.7);
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-bottom: 0.6rem;
}

.detalle-items {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 0.8rem;
}

.detalle-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 10px;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 7px;
  font-size: 0.88rem;
  max-width: 500px;
  gap: 0.5rem;
}

.detalle-nombre { color: rgba(255, 255, 255, 0.75); flex: 1; }
.detalle-qty    { color: rgba(255, 255, 255, 0.4); font-size: 0.82rem; }
.detalle-precio { color: #ffc850; font-weight: 600; }

.detalle-total {
  display: flex;
  justify-content: space-between;
  max-width: 500px;
  padding: 6px 10px;
  border-top: 1px solid rgba(255, 200, 80, 0.12);
  margin-top: 0.3rem;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
}

.detalle-total-valor {
  font-weight: 800;
  color: #ffc850;
}
</style>
