<template>
  <q-page class="flex flex-center">
    <div class="q-pa-md">
    <q-table
      flat bordered
      title="Django-API"
      :rows="rows"
      :columns="columns"
      row-key="name"
      :separator="separator"
    />
  </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'IndexPage',
  data(){
    return {
      columns:[
        {
          name: 'titulo', //La vinculación a ese campo
          label: 'Titulo', // Lo que se ve en la tabla
          align: 'left', //La forma de cómo se alinea
          field: 'title', //El campo del backend
          sortable: true
        },
        {
          name: 'description',
          label: 'Descripción',
          align: 'left',
          field: 'description',
          sortable: true
        },
        {
          name: 'done',
          label: 'Hecho',
          align: 'left',
          field: 'done',
          sortable: true
        }, 
      ],
      rows: [],  
    }
  },
  mounted(){
    this.getRows()
  },
  methods:{
    getRows(){
        this.$axios
        .get('http://127.0.0.1:8000/tasks/api/v1/task/')
        .then(res =>{ this.rows = res.data })
        .catch( e=>{ console.log(e)})
    }
  },
})
</script>
