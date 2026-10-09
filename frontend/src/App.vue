<template>
  <header class="topbar">
    <div class="brand"><span class="brand-mark">V</span><div><strong>Ventas</strong><small>Panel administrativo</small></div></div>
    <nav>
      <RouterLink to="/dashboard">Inicio</RouterLink>
      <RouterLink to="/clientes">Clientes</RouterLink>
      <RouterLink to="/productos">Productos</RouterLink>
      <RouterLink to="/pedidos">Pedidos</RouterLink>
    </nav>
  </header>
  <main class="container"><RouterView /></main>
  <footer>Aplicación CRUD · Vue 3 + Axios + Flask</footer>
</template>
