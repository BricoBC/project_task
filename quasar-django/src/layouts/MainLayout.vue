<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar :class="{ bexBackground: primary }">
        <q-btn flat dense round icon="mdi-file-document" aria-label="Agregar" />

        <q-toolbar-title> Task App </q-toolbar-title>

        <div class="q-pl-xs">v{{ version }}</div>
        <q-toggle
          :label="isActiveModeDark"
          unchecked-icon="mdi-brightness-1"
          color="white"
          v-model="isActiveModeDark"
          @update:model-value="$q.dark.toggle()"
        />
        <q-icon
          v-show="isActiveModeDark"
          name="mdi-moon-waxing-crescent"
          size="250%"
        ></q-icon>
        <q-icon
          v-show="!isActiveModeDark"
          name="mdi-weather-sunny"
          size="250%"
        ></q-icon>
        <q-icon></q-icon>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref, computed } from "vue";
import { useQuasar } from "quasar";

export default defineComponent({
  name: "MainLayout",

  setup() {
    const leftDrawerOpen = ref(true);
    const $q = useQuasar();

    return {
      version: "0.0.1",
      colorPrincipal: "primary",
      isActiveModeDark: ref($q.dark.isActive),
      selection: ref(true),
      leftDrawerOpen,
      methods: {
        darkMode(val) {
          this.$q.dark.set(val);
          console.log(this.$q.dark.mode); // "auto", true, false
        },
      },
    };
  },
  computed: {
    primaryColor() {
      // Accede a las variables SCSS utilizando $primary-color
      return this.$q.dark ? this.$q.theme.primary : this.$q.theme.secondary;
    },
  },
});
</script>
