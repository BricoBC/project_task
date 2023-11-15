<template>
  <!-- Forms -->
  <q-container class="q-pt-sm row no-wrap justify-around">
    <q-select
      style="min-width: 20%; max-width: 20%"
      rounded
      filled
      v-model="input_option"
      :options="options"
      label="Elige una opción"
    />
    <q-input
      style="min-width: 70%; max-width: 70%"
      label="Agrega el titulo"
      standout
      v-model="input_text"
    />
  </q-container>
  <q-container class="q-pt-sm row no-wrap justify-around">
    <q-input
      v-model="input_txtarea"
      filled
      autogrow
      style="min-width: 85%; max-width: 85%"
      />
      <q-btn
      style="min-width: 5%; max-width: 5%"
      color="primary"
      icon="mdi-plus"
    />
  </q-container>
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
