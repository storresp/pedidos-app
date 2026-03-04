<template>
  <div class="card">
    <div class="card-icon">🖥️</div>
    <h3 class="nombre">{{ nombre }}</h3>
    <p class="precio">${{ precio.toLocaleString() }}</p>
    <button class="btn" @click="comprar">+ Agregar</button>
  </div>
</template>

<script setup>
const props = defineProps({
  nombre: String,
  precio: Number
})

const emit = defineEmits(['agregar'])

function comprar() {
  emit('agregar', {
    nombre: props.nombre,
    precio: props.precio
  })
}
</script>

<style scoped>
.card {
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 200, 80, 0.2);
  border-radius: 16px;
  padding: 1.4rem 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  backdrop-filter: blur(6px);
  cursor: default;
}

.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 30px rgba(106, 13, 173, 0.5);
  border-color: rgba(255, 200, 80, 0.6);
}

.card-icon {
  font-size: 2rem;
}

.nombre {
  font-size: 1.05rem;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: 0.3px;
}

.precio {
  font-size: 1.3rem;
  font-weight: 800;
  color: #ffc850;
  text-shadow: 0 0 10px rgba(255, 200, 80, 0.4);
}

.btn {
  width: 100%;
  background: linear-gradient(90deg, #7b2ff7, #e040fb);
  border: none;
  padding: 9px 0;
  border-radius: 10px;
  color: white;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  transition: opacity 0.2s ease, transform 0.1s ease;
  letter-spacing: 0.3px;
}

.btn:hover {
  opacity: 0.88;
  transform: scale(1.03);
}

.btn:active {
  transform: scale(0.97);
}
</style>