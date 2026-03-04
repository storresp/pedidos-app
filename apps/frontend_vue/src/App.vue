<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<template>
  <div class="app-container">

    <!-- Header global -->
    <header class="header">
      <div class="header-contenido">
        <div>
          <h1 class="titulo">🛍️ Gestor de Pedidos</h1>
          <p class="subtitulo">Selecciona tus productos y gestiona tu pedido</p>
        </div>

        <!-- Enlace Admin (discreto, esquina superior derecha) -->
        <RouterLink
          to="/admin"
          class="link-admin"
          :class="{ activo: route.name === 'admin' }"
        >
          ⚙️ Admin
        </RouterLink>
      </div>
    </header>

    <!-- Las vistas se renderizan aquí -->
    <RouterView />

  </div>
</template>

<!-- Estilos globales: elimina bordes blancos en html/body -->
<style>
*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  min-height: 100vh;
  background: #1a0040;
}
</style>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a0040 0%, #3b0080 45%, #6a0dad 75%, #1a0040 100%);
  font-family: 'Segoe UI', Tahoma, sans-serif;
}

.header {
  background: rgba(0, 0, 0, 0.3);
  border-bottom: 1px solid rgba(255, 200, 80, 0.25);
  backdrop-filter: blur(8px);
  padding: 1.5rem 2rem;
}

.header-contenido {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1400px;
  margin: 0 auto;
}

.titulo {
  font-size: 2.2rem;
  font-weight: 800;
  color: #ffc850;
  text-shadow: 0 0 24px rgba(255, 200, 80, 0.55);
  letter-spacing: 1px;
}

.subtitulo {
  margin-top: 4px;
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: 0.4px;
}

/* Link de admin: discreto pero accesible */
.link-admin {
  text-decoration: none;
  color: rgba(255, 255, 255, 0.45);
  font-size: 0.88rem;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.2s ease;
  letter-spacing: 0.3px;
  white-space: nowrap;
}

.link-admin:hover,
.link-admin.activo {
  color: #ffc850;
  border-color: rgba(255, 200, 80, 0.4);
  background: rgba(255, 200, 80, 0.07);
}
</style>
