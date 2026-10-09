<template>
  <section class="hero">
    <div><span class="eyebrow">PANEL DE CONTROL</span><h1>Gestiona tus ventas<br><em>en un solo lugar.</em></h1>
      <p>Administra clientes, productos e inventario de pedidos desde una interfaz sencilla.</p>
      <div class="hero-actions"><RouterLink class="button button--primary" to="/pedidos">Crear pedido <span>→</span></RouterLink><RouterLink class="button button--secondary" to="/productos">Ver productos</RouterLink></div>
    </div>
    <div class="hero-art"><div class="art-card"><span class="art-icon">↗</span><small>Gestión organizada</small><strong>Ventas & pedidos</strong><div class="art-bars"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><span class="art-caption">Controla cada registro</span></div><div class="art-dot dot-one"></div><div class="art-dot dot-two"></div></div>
  </section>
  <section class="section-heading"><div><span class="eyebrow">MÓDULOS</span><h2>Todo lo que necesitas</h2></div><p>Selecciona un módulo para comenzar.</p></section>
  <div class="module-grid">
    <RouterLink to="/clientes" class="module-card"><span class="module-icon lavender">♙</span><span class="module-count">01 / REGISTROS</span><h3>Clientes</h3><p>Registra y actualiza la información de tus clientes.</p><span class="module-link">Administrar <b>↗</b></span></RouterLink>
    <RouterLink to="/productos" class="module-card"><span class="module-icon mint">▦</span><span class="module-count">02 / INVENTARIO</span><h3>Productos</h3><p>Controla precios, existencias y disponibilidad.</p><span class="module-link">Administrar <b>↗</b></span></RouterLink>
    <RouterLink to="/pedidos" class="module-card"><span class="module-icon peach">▤</span><span class="module-count">03 / VENTAS</span><h3>Pedidos</h3><p>Crea pedidos, consulta totales y actualiza estados.</p><span class="module-link">Administrar <b>↗</b></span></RouterLink>
  </div>
  <p class="dashboard-note"><span>✦</span> Los cambios se guardan en la base de datos a través de la API Flask.</p>
</template>
