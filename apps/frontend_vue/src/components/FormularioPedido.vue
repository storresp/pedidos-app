<script setup>
import { ref } from 'vue'

// ── El componente emite el evento 'enviar' con { nombre, correo } ──
const emit = defineEmits(['enviar'])

const nombre = ref('')
const correo = ref('')
const enviando = ref(false)
const enviado = ref(false)
const error = ref('')

async function handleSubmit() {
  error.value = ''

  // Validación básica
  if (!nombre.value.trim() || !correo.value.trim()) {
    error.value = 'Por favor completa todos los campos.'
    return
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo.value)) {
    error.value = 'El correo no es válido.'
    return
  }

  enviando.value = true

  // ════════════════════════════════════════════════════════════════
  // TODO (cuando tengas la DB):
  //   Reemplaza este bloque con una llamada real a tu API.
  //   Ejemplo con fetch:
  //
  //   const res = await fetch('http://TU_BACKEND/api/pedidos/', {
  //     method: 'POST',
  //     headers: { 'Content-Type': 'application/json' },
  //     body: JSON.stringify({
  //       nombre: nombre.value,
  //       correo: correo.value,
  //       productos: props.productos   // <-- pasa los productos como prop desde PaginaCheckout
  //     })
  //   })
  //   if (!res.ok) throw new Error('Error al guardar el pedido')
  // ════════════════════════════════════════════════════════════════

  // Simulación de guardado (quitar cuando tengas la DB)
  await new Promise(r => setTimeout(r, 1000))

  enviando.value = false
  enviado.value = true

  emit('enviar', { nombre: nombre.value, correo: correo.value })
}
</script>

<template>
  <div class="formulario-container">
    <div class="form-header">
      <span class="form-icon">📋</span>
      <h2 class="form-titulo">Datos del Cliente</h2>
    </div>

    <!-- Confirmación de éxito -->
    <div v-if="enviado" class="exito">
      <span class="exito-icon">✅</span>
      <p>¡Pedido registrado con éxito!</p>
      <p class="exito-sub">Te contactaremos a <strong>{{ correo }}</strong></p>
    </div>

    <!-- Formulario -->
    <form v-else @submit.prevent="handleSubmit" class="form">

      <div class="campo">
        <label for="nombre">Nombre completo</label>
        <input
          id="nombre"
          v-model="nombre"
          type="text"
          placeholder="Ej. Juan Díaz"
          autocomplete="name"
        />
      </div>

      <div class="campo">
        <label for="correo">Correo electrónico</label>
        <input
          id="correo"
          v-model="correo"
          type="email"
          placeholder="Ej. juan@correo.com"
          autocomplete="email"
        />
      </div>

      <p v-if="error" class="error-msg">⚠️ {{ error }}</p>

      <button type="submit" class="btn-enviar" :disabled="enviando">
        <span v-if="enviando">Enviando...</span>
        <span v-else>Confirmar Pedido 🚀</span>
      </button>

    </form>
  </div>
</template>

<style scoped>
.formulario-container {
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 200, 80, 0.25);
  border-radius: 18px;
  backdrop-filter: blur(10px);
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Header */
.form-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1.3rem 1.5rem 1rem;
  border-bottom: 1px solid rgba(255, 200, 80, 0.15);
}

.form-icon { font-size: 1.4rem; }

.form-titulo {
  font-size: 1.15rem;
  font-weight: 700;
  color: #ffc850;
  letter-spacing: 0.5px;
}

/* Formulario */
.form {
  padding: 1.4rem 1.5rem 1.8rem;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.campo {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

label {
  font-size: 0.88rem;
  color: rgba(255, 255, 255, 0.65);
  font-weight: 500;
  letter-spacing: 0.3px;
}

input {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 200, 80, 0.2);
  border-radius: 10px;
  padding: 11px 14px;
  font-size: 0.95rem;
  color: #fff;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

input::placeholder { color: rgba(255, 255, 255, 0.3); }

input:focus {
  border-color: rgba(255, 200, 80, 0.6);
  box-shadow: 0 0 0 3px rgba(255, 200, 80, 0.1);
}

.error-msg {
  font-size: 0.88rem;
  color: #ff7b7b;
  margin-top: -0.4rem;
}

.btn-enviar {
  width: 100%;
  background: linear-gradient(90deg, #7b2ff7, #e040fb);
  border: none;
  padding: 13px 0;
  border-radius: 12px;
  color: white;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.15s;
  letter-spacing: 0.4px;
  margin-top: 0.4rem;
}

.btn-enviar:hover:not(:disabled) {
  opacity: 0.88;
  transform: scale(1.02);
}

.btn-enviar:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Éxito */
.exito {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
  padding: 2.5rem 1.5rem;
  text-align: center;
  color: rgba(255, 255, 255, 0.85);
}

.exito-icon { font-size: 3rem; }

.exito-sub {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.55);
  margin-top: 0.2rem;
}
</style>
