<template>
  <section class="page-head"><div><span class="eyebrow">VENTAS</span><h1>Pedidos</h1><p>Registra pedidos y controla su estado.</p></div><span class="count-badge">{{ pedidos.length }} registros</span></section>
  <AlertMessage :message="error" /><AlertMessage :message="exito" type="success" />
  <section class="panel"><div class="panel-head"><div><h2>Crear pedido</h2><p>El sistema descontará las existencias al registrar el pedido.</p></div><span class="panel-step">NUEVO PEDIDO</span></div>
    <form class="form-grid" @submit.prevent="guardar">
      <label class="field"><span>Cliente *</span><select v-model.number="form.cliente_id" required><option disabled value="">Seleccione un cliente</option><option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.nombre }}</option></select></label>
      <label class="field"><span>Producto *</span><select v-model.number="form.producto_id" required><option disabled value="">Seleccione un producto</option><option v-for="p in disponibles" :key="p.id" :value="p.id">{{ p.nombre }} — Q{{ Number(p.precio).toFixed(2) }} ({{ p.stock }} disponibles)</option></select></label>
      <BaseInput v-model="form.cantidad" label="Cantidad *" type="number" min="1" step="1" required :error="cantidadError" />
      <div class="form-actions"><BaseButton type="submit" :disabled="guardando">{{ guardando ? 'Registrando…' : '+ Registrar pedido' }}</BaseButton></div>
    </form>
  </section>
  <section class="list-section"><div class="section-heading"><div><span class="eyebrow">BASE DE DATOS</span><h2>Historial de pedidos</h2></div><input v-model="busqueda" class="search" placeholder="⌕  Buscar pedido…" /></div>
    <DataTable :rows="filtrados" :columns="columns"><template #actions="{ row }"><select class="status-select" :value="row.estado" @change="cambiarEstado(row,$event.target.value)"><option v-for="s in estados" :key="s" :value="s">{{ s }}</option></select><BaseButton variant="danger" @click="eliminar(row)">Eliminar</BaseButton></template></DataTable>
  </section>
</template>
<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { clientesApi } from '../api/clientes'
import { productosApi } from '../api/productos'
import { pedidosApi } from '../api/pedidos'
import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import DataTable from '../components/DataTable.vue'
const pedidos=ref([]),clientes=ref([]),productos=ref([]),error=ref(''),exito=ref(''),guardando=ref(false),busqueda=ref('')
const estados=['pendiente','pagado','enviado','cancelado']
const columns=[{key:'id',label:'Pedido'},{key:'cliente',label:'Cliente'},{key:'producto',label:'Producto'},{key:'cantidad',label:'Cantidad'},{key:'total',label:'Total'},{key:'estado',label:'Estado'}]
const form=reactive({cliente_id:'',producto_id:'',cantidad:'1'})
const disponibles=computed(()=>productos.value.filter(p=>p.activo && p.stock>0))
const cantidadError=computed(()=>form.cantidad!==''&&(!Number.isInteger(Number(form.cantidad))||Number(form.cantidad)<1)?'La cantidad debe ser un entero mayor que cero.':'')
const filtrados=computed(()=>pedidos.value.filter(p=>`${p.id} ${p.cliente} ${p.producto} ${p.estado}`.toLowerCase().includes(busqueda.value.toLowerCase())))
watch(()=>form.producto_id,()=>{})
async function cargar(){try{const [a,b,c]=await Promise.all([pedidosApi.listar(),clientesApi.listar(),productosApi.listar()]);pedidos.value=a.data;clientes.value=b.data;productos.value=c.data;error.value=''}catch(e){error.value=e.message}}
async function guardar(){error.value='';exito.value='';if(!form.cliente_id||!form.producto_id||cantidadError.value){error.value='Completa los campos y verifica la cantidad.';return}guardando.value=true;try{await pedidosApi.crear({cliente_id:Number(form.cliente_id),producto_id:Number(form.producto_id),cantidad:Number(form.cantidad)});Object.assign(form,{cliente_id:'',producto_id:'',cantidad:'1'});await cargar();exito.value='Pedido registrado y stock actualizado.'}catch(e){error.value=e.message}finally{guardando.value=false}}
async function cambiarEstado(p,estado){error.value='';try{await pedidosApi.actualizar(p.id,{estado});await cargar();exito.value='Estado del pedido actualizado.'}catch(e){error.value=e.message;await cargar()}}
async function eliminar(p){if(!window.confirm(`¿Eliminar pedido #${p.id}? Solo se pueden eliminar pedidos cancelados.`))return;error.value='';try{await pedidosApi.eliminar(p.id);await cargar();exito.value='Pedido eliminado.'}catch(e){error.value=e.message}}
onMounted(cargar)
</script>
