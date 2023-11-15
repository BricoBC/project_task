<template>
  
  <!-- Table -->
  <q-page class="">
    <div class="q-pa-md">
      <q-table
        label="Agrega una descripción"
        flat
        bordered
        title="Django-API"
        :rows="rows"
        :columns="columns"
        row-key="name"
      />
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";
import { api } from "boot/axios";

export default defineComponent({
  name: "IndexPage",
  data() {
    return {
      options: ["Crear", "Actualizar"],
      input_option: ref("Crear"),
      input_txtarea: ref(null),
      input_text: ref(null),
      action: "Crear",
      columns: [
        {
          name: "titulo", //La vinculación a ese campo
          label: "Titulo", // Lo que se ve en la tabla
          align: "left", //La forma de cómo se alinea
          field: "title", //El campo del backend
          sortable: true,
        },
        {
          name: "description",
          label: "Descripción",
          align: "left",
          field: "description",
          sortable: true,
        },
        {
          name: "done",
          label: "Hecho",
          align: "left",
          field: "done",
          sortable: true,
        },
      ],
      rows: [],
    };
  },
  mounted() {
    this.getRows();
  },
  methods: {
    getRows() {
      //api ya tiene el resto del url
      api
        .get("/task/")
        .then((res) => {
          this.rows = res.data;
          console.log(this.rows);
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
});
</script>
