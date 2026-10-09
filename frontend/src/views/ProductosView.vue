<template>
  <section class="page-head"><div><span class="eyebrow">CATÁLOGO</span><h1>Productos</h1><p>Administra productos, precios y existencias.</p></div><span class="count-badge">{{ productos.length }} registros</span></section>
  <AlertMessage :message="error" /><AlertMessage :message="exito" type="success" />
  <section class="panel"><div class="panel-head"><div><h2>{{ editando ? 'Editar producto' : 'Nuevo producto' }}</h2><p>Los campos con * son obligatorios.</p></div><span class="panel-step">{{ editando ? 'EDITAR' : 'INVENTARIO' }}</span></div>
    <form class="form-grid" @submit.prevent="guardar" novalidate>
      <BaseInput v-model="form.nombre" label="Nombre *" placeholder="Ej. Teclado inalámbrico" :error="errores.nombre" required />
      <BaseInput v-model="form.descripcion" label="Descripción" placeholder="Descripción breve" />
      <BaseInput v-model="form.precio" label="Precio (Q) *" type="number" min="0" step="0.01" :error="errores.precio" required />
      <BaseInput v-model="form.stock" label="Existencias *" type="number" min="0" step="1" :error="errores.stock" required />
      <label class="check-field"><input v-model="form.activo" type="checkbox" /> Producto activo y disponible</label>
      <div class="form-actions"><BaseButton type="submit" :disabled="guardando">{{ guardando ? 'Guardando…' : editando ? 'Guardar cambios' : '+ Crear producto' }}</BaseButton><BaseButton v-if="editando" variant="secondary" @click="limpiar">Cancelar</BaseButton></div>
    </form>
  </section>
  <section class="list-section"><div class="section-heading"><div><span class="eyebrow">BASE DE DATOS</span><h2>Listado de productos</h2></div><input v-model="busqueda" class="search" placeholder="⌕  Buscar producto…" /></div>
    <DataTable :rows="filtrados" :columns="columns"><template #actions="{ row }"><BaseButton variant="secondary" @click="editar(row)">Editar</BaseButton><BaseButton variant="danger" @click="eliminar(row)">Eliminar</BaseButton></template></DataTable>
  </section>
</template>
<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { productosApi } from '../api/productos'
import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import DataTable from '../components/DataTable.vue'
const productos=ref([]),error=ref(''),exito=ref(''),guardando=ref(false),editando=ref(false),idEditando=ref(null),busqueda=ref('')
const errores=reactive({nombre:'',precio:'',stock:''})
const columns=[{key:'id',label:'ID'},{key:'nombre',label:'Producto'},{key:'precio',label:'Precio Q'},{key:'stock',label:'Stock'},{key:'activo',label:'Estado'}]
const form=reactive({nombre:'',descripcion:'',precio:'',stock:'0',activo:true})
const filtrados=computed(()=>productos.value.filter(p=>`${p.nombre} ${p.descripcion}`.toLowerCase().includes(busqueda.value.toLowerCase())))
function limpiar(){Object.assign(form,{nombre:'',descripcion:'',precio:'',stock:'0',activo:true});editando.value=false;idEditando.value=null;Object.keys(errores).forEach(k=>errores[k]='')}
async function cargar(){try{productos.value=(await productosApi.listar()).data;error.value=''}catch(e){error.value=e.message}}
async function guardar(){
 error.value='';exito.value='';Object.keys(errores).forEach(k=>errores[k]='')
 if(!form.nombre.trim())errores.nombre='El nombre es obligatorio.'
 if(form.precio===''||!Number.isFinite(Number(form.precio))||Number(form.precio)<0)errores.precio='Precio no válido.'
 if(form.stock===''||!Number.isInteger(Number(form.stock))||Number(form.stock)<0)errores.stock='El stock debe ser entero y no negativo.'
 if(Object.values(errores).some(Boolean))return
 guardando.value=true
 try{const payload={...form,precio:Number(form.precio),stock:Number(form.stock)};if(editando.value)await productosApi.actualizar(idEditando.value,payload);else await productosApi.crear(payload);limpiar();await cargar();exito.value='Producto guardado correctamente.'}catch(e){error.value=e.message}finally{guardando.value=false}
}
function editar(p){Object.assign(form,{...p,precio:String(p.precio),stock:String(p.stock)});editando.value=true;idEditando.value=p.id;exito.value=''}
async function eliminar(p){if(!window.confirm(`¿Eliminar ${p.nombre}?`))return;error.value='';try{await productosApi.eliminar(p.id);await cargar();exito.value='Producto eliminado.'}catch(e){error.value=e.message}}
onMounted(cargar)
</script>
