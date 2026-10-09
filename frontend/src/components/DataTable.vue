<template>
  <div class="table-wrapper"><table>
    <thead><tr><th v-for="column in columns" :key="column.key">{{ column.label }}</th><th>Acciones</th></tr></thead>
    <tbody>
      <tr v-if="!rows.length"><td :colspan="columns.length + 1" class="empty">No hay registros todavía.</td></tr>
      <tr v-for="row in rows" :key="row.id">
        <td v-for="column in columns" :key="column.key">
          <span v-if="column.key === 'activo'" :class="['pill', row[column.key] ? 'pill--green' : 'pill--gray']">{{ row[column.key] ? 'Activo' : 'Inactivo' }}</span>
          <span v-else-if="column.key === 'total'">Q{{ Number(row[column.key]).toFixed(2) }}</span>
          <span v-else>{{ row[column.key] ?? '—' }}</span>
        </td>
        <td class="actions"><slot name="actions" :row="row" /></td>
      </tr>
    </tbody>
  </table></div>
</template>
<script setup>
defineProps({ rows: { type: Array, default: () => [] }, columns: { type: Array, required: true } })
</script>
