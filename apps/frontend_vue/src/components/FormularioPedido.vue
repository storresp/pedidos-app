<script setup>
import { ref } from 'vue'

const props = defineProps({
  enviando: {
    type: Boolean,
    default: false
  },
  enviado: {
    type: Boolean,
    default: false
  },
  errorMsg: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['enviar'])

const nombre = ref('')
const correo = ref('')
const errorFront = ref('')

function handleSubmit() {
  errorFront.value = ''

  // Validación básica del lado del frontend
  if (!nombre.value.trim() || !correo.value.trim()) {
    errorFront.value = 'Por favor completa todos los campos.'
    return
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo.value)) {
    errorFront.value = 'El correo no es válido.'
    return
  }

  // Notificamos al componente padre (PaginaCheckout) que intente guardar en BD
  emit('enviar', { 
    nombre: nombre.value.trim(), 
    correo: correo.value.trim() 
  })
}
</script>

<template>
  <div class="formulario-container">
    <div class="form-header">
      <span class="form-icon">📋</span>
      <h2 class="form-titulo">Datos del Cliente</h2>
    </div>

    <!-- Confirmación de éxito (controlado por el prop `enviado` del padre) -->
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
          :disabled="enviando"
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
          :disabled="enviando"
        />
      </div>

      <!-- Errores locales del formulario -->
      <p v-if="errorFront" class="error-msg">⚠️ {{ errorFront }}</p>
      <!-- Errores que vienen del backend o del padre -->
      <p v-else-if="errorMsg" class="error-msg dev-error">❌ {{ errorMsg }}</p>

      <button type="submit" class="btn-enviar" :disabled="enviando">
        <span v-if="enviando">Guardando en BD... ⏳</span>
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

input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-msg {
  font-size: 0.88rem;
  color: #ff7b7b;
  margin-top: -0.4rem;
}

.dev-error {
  color: #ff5757;
  font-weight: 600;
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
