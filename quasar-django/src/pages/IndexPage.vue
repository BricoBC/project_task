<template>
  <!-- Forms -->
  <q-form action="" @submit="onSubmit" @reset="onReset">
    <div class="q-pt-sm row no-wrap justify-around">
      <q-select
        style="min-width: 20%; max-width: 20%"
        readonly
        filled
        v-model="input_option"
        :options="options"
      />
      <q-input
        style="min-width: 70%; max-width: 70%"
        label="Agrega el titulo"
        standout
        :rules="[(val) => (val && val.length > 0) || 'Please type something']"
        v-model="input_title"
      />
    </div>
    <div class="q-pa-sm row no-wrap justify-around">
      <q-input
        v-model="input_description"
        filled
        autogrow
        :rules="[(val) => (val && val.length > 0) || 'Please type something']"
        style="width: 85%"
      />
      <q-btn
        style="min-width: 5%; max-width: 5%"
        color="primary"
        icon="mdi-plus"
        type="submit"
        />
        <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
    </div>
  </q-form>
  <div class="q-mt-md full-width row justify-end">
    Titulo: {{ JSON.stringify(input_title) }}, Descripción:
    {{ JSON.stringify(input_description) }}
  </div>
  <!-- Table -->
  <h4 class="q-py-xs q-ma-none">Django Api</h4>
  <q-page class="q-pa-md">
    <q-table
      class="my-sticky-header-table"
      label="Agrega una descripción"
      flat
      bordered
      :rows="rows"
      :columns="columns"
      row-key="name"
      :selected-rows-label="getSelectedString"
      selection="single"
      v-model:selected="selected"
    />
    <div class="q-mt-md full-width row justify-end">
      Selected: {{ JSON.stringify(selected) }}
      <q-btn class="q-mx-sm" color="primary" label="Editar" />
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, watch } from "vue";
import { api } from "boot/axios";
import { useQuasar } from "quasar";

export default defineComponent({
  name: "IndexPage",
  data() {
    return {
      $q: useQuasar(),
      options: ["Crear", "Actualizar"],
      input_option: ref("Crear"),
      input_description: ref(null),
      input_title: ref(null),
      selected: ref([]),
      action: "Crear",
      set_values: {},
      columns: [
        {
          name: "titulo", //La vinculación a ese campo
          label: "Titulo", // Lo que se ve en la tabla
          align: "left", //La forma de cómo se alinea
          field: "title", //El campo del backend
          sortable: true,
          action: "acciones",
        },
        {
          name: "description",
          label: "Descripción",
          align: "left",
          field: "description",
          sortable: true,
          action: "acciones",
        },
        {
          name: "done",
          label: "Hecho",
          align: "left",
          field: "done",
          sortable: true,
          action: "acciones",
        },
      ],
      rows: [],
    };
  },
  mounted() {
    this.getRows();
  },
  methods: {
    verification() {
      if (this.input_description != null && this.input_title != null)
        return true;
      else return false;
    },
    onReset () {
        this.input_description = null
        this.input_title = null
      },
    onSubmit() {
      if (this.input_description != null && this.input_title != null) {
        this.$q.notify({
          color: "primary",
          textColor: "white",
          icon: "mdi-check-all",
          message: "Submitted",
        });
        this.set_values = {
          title: this.input_title,
          description: this.input_description,
          done: false,
        };
        this.setValues(this.set_values);
      } else {
        this.$q.notify({
          color: "red-5",
          textColor: "white",
          icon: "mdi-alert",
          message: "Ingresa la información del forms",
        });
        this.onReset();
      }
    },
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
    setValues(forms) {
      api
        .post("/task/", forms)
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    getSelectedString() {
      return selected.value.length === 0
        ? ""
        : `${selected.value.length} record${
            selected.value.length > 1 ? "s" : ""
          } selected of ${rows.length}`;
    },
  },
});
</script>
<style lang="sass">
.my-sticky-header-table
  height: 400px

  .q-table__top,
  thead tr:first-child th
    background-color: $secondary-dark
    color: white

  thead tr th
    position: sticky
    z-index: 1
  thead tr:first-child th
    top: 0

  &.q-table--loading thead tr:last-child th

    top: 48px


  tbody
    scroll-margin-top: 48px
</style>
