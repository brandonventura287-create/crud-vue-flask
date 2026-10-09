<template>
  <section class="page-head"><div><span class="eyebrow">DIRECTORIO</span><h1>Clientes</h1><p>Administra los datos de tus clientes.</p></div><span class="count-badge">{{ clientes.length }} registros</span></section>
  <AlertMessage :message="error" /><AlertMessage :message="exito" type="success" />
  <section class="panel"><div class="panel-head"><div><h2>{{ editando ? 'Editar cliente' : 'Nuevo cliente' }}</h2><p>Completa los campos requeridos.</p></div><span class="panel-step">{{ editando ? 'EDITAR' : 'NUEVO REGISTRO' }}</span></div>
    <form class="form-grid" @submit.prevent="guardar" novalidate>
      <BaseInput v-model="form.nombre" label="Nombre completo *" placeholder="Ej. Ana López" :error="errores.nombre" required />
      <BaseInput v-model="form.correo" label="Correo electrónico *" type="email" placeholder="ana@correo.com" :error="errores.correo" required />
      <BaseInput v-model="form.telefono" label="Teléfono" placeholder="5555-5555" />
      <div class="form-actions"><BaseButton type="submit" :disabled="guardando">{{ guardando ? 'Guardando…' : editando ? 'Guardar cambios' : '+ Crear cliente' }}</BaseButton><BaseButton v-if="editando" variant="secondary" @click="limpiar">Cancelar</BaseButton></div>
    </form>
  </section>
  <section class="list-section"><div class="section-heading"><div><span class="eyebrow">BASE DE DATOS</span><h2>Listado de clientes</h2></div><input v-model="busqueda" class="search" placeholder="⌕  Buscar cliente…" /></div>
    <DataTable :rows="filtrados" :columns="columns"><template #actions="{ row }"><BaseButton variant="secondary" @click="editar(row)">Editar</BaseButton><BaseButton variant="danger" @click="eliminar(row)">Eliminar</BaseButton></template></DataTable>
  </section>
</template>
<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { clientesApi } from '../api/clientes'
import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import DataTable from '../components/DataTable.vue'
const clientes = ref([]), error = ref(''), exito = ref(''), guardando = ref(false), editando = ref(false), idEditando = ref(null), busqueda = ref('')
const errores = reactive({ nombre: '', correo: '' })
const columns = [{key:'id',label:'ID'},{key:'nombre',label:'Nombre'},{key:'correo',label:'Correo'},{key:'telefono',label:'Teléfono'}]
const form = reactive({ nombre:'', correo:'', telefono:'' })
const filtrados = computed(() => clientes.value.filter(c => `${c.nombre} ${c.correo} ${c.telefono}`.toLowerCase().includes(busqueda.value.toLowerCase())))
function limpiar(){ Object.assign(form,{nombre:'',correo:'',telefono:''}); editando.value=false; idEditando.value=null; errores.nombre=''; errores.correo='' }
async function cargar(){ try { clientes.value=(await clientesApi.listar()).data; error.value='' } catch(e){error.value=e.message} }
async function guardar(){
  error.value=''; exito.value=''; errores.nombre=''; errores.correo=''
  if(!form.nombre.trim()) errores.nombre='El nombre es obligatorio.'
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.correo.trim())) errores.correo='Ingresa un correo válido.'
  if(errores.nombre||errores.correo) return
  guardando.value=true
  try { if(editando.value) await clientesApi.actualizar(idEditando.value,{...form}); else await clientesApi.crear({...form}); limpiar(); await cargar(); exito.value='Cliente guardado correctamente.' }
  catch(e){error.value=e.message} finally{guardando.value=false}
}
function editar(c){Object.assign(form,c);editando.value=true;idEditando.value=c.id;errores.nombre='';errores.correo='';exito.value=''}
async function eliminar(c){if(!window.confirm(`¿Eliminar a ${c.nombre}?`))return;error.value='';exito.value='';try{await clientesApi.eliminar(c.id);await cargar();exito.value='Cliente eliminado.'}catch(e){error.value=e.message}}
onMounted(cargar)
</script>
