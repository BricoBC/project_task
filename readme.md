## INTRODUCCIÓN
Este proyecto está basado con conocimientos básicos que se exponen en el repositorio de _**project-django**_ , **crud-auth** y **drt-crud**.
Se va a mencionar conceptos que fueron mencionados en ese repositorio y se va a ir complementando con respecto para hacer un REST API y su comunicación que tenga con el frontend.

## 1. Buenas prácticas
Recordar que las buenas prácticas consiste en:
1. Crear carpeta del proyecto.
```bash
  mkdir carpeta
```
2. Inicializar git.
```bash
  git init
```

3. Crear entorno virtual.
```python
python3 -m venv venv
```

4. Activar entorno virtual.
```bash
source ./venv/bin/activate
```
5. Hacer un documento txt en donde esten las dependencias que utilicemos.
```python
pip freeze > requirements.txt
```

6. Instalar dependencias:
```python
pip install -r requirements.txt
```
Es importante recordar que a lo largo de la vida del proyecto hay que estar guardando las dependencias si se instala algo más.

7. Instalar django, djangorestframework y django-cors-headers
```python
pip install django
```

```python
pip install djangorestframework
```

```python
pip install django-cors-headers
```

NOTA: Si usas vscode puedes hacer clic a la barra buscadora de hasta arriba y escribir ">python: Select interpret ", la das enter. Después seleccionas el entorno virtual que creaste.
Esto te ayuda para que cuando abras una nueva terminal no tengas que activar el entorno a cada rato.

# BACKEND (DJANGO)
## 2 Configuración del proyecto.
### 2.1) Crear el proyecto
```python
django-admin startproject crud_api .
```
### 2.2) Arrancar el servidor de django
```python
py manage.py runserver
```

### 2.3) Crear app
```python
py manage.py startapp pass_secure
```
### 2.4) Conectar la app con el proyecto
Se tiene que abrir el archivo de **settings.py** del proyecto y agregar lo siguiente:
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
    'rest_framework',
    'pass_secure',
]
...


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders',
    ...

...
CORS_ALLOWED_ORIGINS = [
    ## Aqui va el servidor del frontend
]
```

## 3) Modelos
### 3.1) Crear la migraciones
```python
py manage.py makemigrations
```
### 3.2) Migrar los modelos
```python
py manage.py migrate
```

### 3.3) Crear las tablas
Hay que recordar que en la aplicación que se hizo hay un archivo **models.py** en donde se ingresa el código para crear las tablas, en mi caso fue el siguiente:
```python
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    done = models.BooleanField(default=False)

```
Después se usa el comando para crear las migraciones y después se migran los modelos.

## 4. Panel de administrador
Existe una ruta exclusiva para el panel de administrador, para ello hay que crear un usario administrador y eso se hace con el siguiente comando:
```python
py manage.py createsuperuser
```
Después te solicita unos datos, hay que ingresarlos.

Ahora sincronicemos la tabla creada con el panel de administración.
En el archivo **admin.py** de la app de ingresa lo siguiente:
```python
from django.contrib import admin
#Modelo Task
from .models import Task

admin.site.register(Task)
```

Después se ejecuta el servidor de django y se pone al final de la ruta /admin/, se ingresa los datos de login y accedes al panel de administrador.

Nota: Si no te gusta como se ve cuando ya se tiene registrado un dato en la tabla se puede modificar de la siguiente forma:
En el archivo models.py del modelo agregar lo siguiente:
```python
    ...
    done = models.BooleanField(default=False)

    def __str__(self) -> str:        
        return self.title
```

## 5. API
Para crear las vistas del CRUD es necesario hacer lo siguiente:
En la app crear el archivo **serializer.p**y que contenga lo siguiente:
```python
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        #Se indica cuales campos se quiere mandar al front.
        ## fields = ('id', 'title', 'description', 'done')
        fields = '__all__'
```

En el archivo **views.py** agregar lo siguiente:
```python
from rest_framework import viewsets
from .serializer import TaskSerializer
from .models import Task

class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
```
Lo anterior es para que pueda hacer toda la operación del crud.

Para crear las rutas hay que crear el archivo **urls.py** en la app y poner lo siguiente:
```python
from django.urls import path, include
from rest_framework import routers
from tasks import views

router = routers.DefaultRouter()
router.register(r'task', views.TaskView, 'tasks')

#api versioning
urlpatterns = [
    path("api/v1", include(router.urls))
]
```
Después en el archivo de urls.py del proyeto se pone lo siguiente:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls') ),
]
```
## 6. Documentar
La parte más tediosa es el documentar el proyecto desde el backend y el frontend, para el desarrollo de la API hay un modulo que permite documentar la API el cual se instala de la siguiente forma:
```python
pip install coreapi
```

Después se va al archivo de **settings.py** del proyecto para agregar lo siguiente:
```python
...
INSTALLED_APPS = [
  ...
    "corsheaders",
    'coreapi',
    'rest_framework',
  ...
  
CORS_ALLOWED_ORIGINS = []
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}
```

Después en el archivo de urls.py de la app se agrega lo siguiente:
```python
...
from rest_framework.documentation import include_docs_urls
...
urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("docs/", include_docs_urls(title="Task-API")),
]
```

Nota: En caso que no te funcione el servidore puedes hacer lo siguiente:
Ejecutar lo siguiente:
```python
py -m pip install --upgrade pip
pip install -r requirements.txt
pip install --upgrade setuptools
pip uninstall coreapi
pip install coreapi
```

# FRONTEND (QUASAR)

Descargar e instalar [node.JS](https://nodejs.org/en) 
Se comprueba que ya se tiene instalado con el siguiente comando para que salga la versión:
```bash
node -v
```

Para instalar quasar es con el siguiente comando:
```python
npm install -g @quasar/cli
```
NOTA: EL SIGUIENTE COMANDO LO EJECUTE EN LA MISMA CARPETA EN DONDE HICE EL PROYECTO DEL BACKEND.

Para empezar un nuevo proyecto es con el comando de 
```python
npm init quasar
```
Va a solicitar la siguiente información:

| Pregunta | Respuesta     |
| :-------- | :------- | 
| `√ Project folder:` | `quasar-django ` | 
| `√ Pick Quasar version:` | `Quasar v2 (Vue 3 - latest and greatest):` | 
| `√ Pick script type:` | `Javascript` | 
| `√ Pick Quasar App CLI variant:` | ` Quasar App CLI with Vite` | 
| `√ Package name:` | ` quasar-django` | 
| `√ Project product name:` | `Task App` | 
| `√ Project description:` | `Conexión backend django con frontend Quasar` | 
| `√ Author:` | `BricoBC <barajas.c.bruno.n@gmail.com>` | 
| `√ Pick your CSS preprocessor:` | `Sass with SCSS syntax` | 
| `√ Check the features needed for your project:` | `ESLint, Axios, Vuex` | 
| `√ Pick an ESLint preset:` | `Prettier` | 
| `√ Install project dependencies?` | `Yes, use npm` | 

Ya lo único que queda es acceder a la carpeta que se crea y ejecutar el servidor de Quasar con el siguiente comando:
```js
quasar dev
```

## 1. Agregar una tabla al inicio
Hay que acceder a la carpeta del proyecto de Quasar, después al de 'src' y después al de pages.
Hay que recordar que se trabaja en secciones con Quasar, por el momento el archivo de IndexPage.vue tiene el **template** y el **script**

En el de template hay que poner lo siguiente:
```js
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
```

En el de script hay que poner lo siguiente:
```js
<script>
import { defineComponent } from 'vue'
import { api } from "boot/axios";

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
})
</script>
```
Después en el archivo axios.js que se encuetra en la carpeta boot hay que poner lo  siguiente:

```js
const api = axios.create({ baseURL: 'http://127.0.0.1:8000/tasks/api/v1' })
```
Ahora tenemos que ver el puerto que se ejecuta el servidor de Quasar, en mi caso es el 9000 asi que lo voy a indicar en la configuración del proyecto de django.
```python
...
# Aquí van los servidores que se permite conectar
CORS_ALLOWED_ORIGINS = [
    'http://localhost:9000'
]

REST_FRAMEWORK = {
...
```

## 2. Agregar componentes
A continuación mostraré mi código de los componentes que agregue con su script y estilos, pero a continuación dejo la documentación para mayor amplitud en los componentes [Quasar Docs-Components]( https://quasar.dev/components ) 

### 2.1) IndexPage.vue
En el archivo IndexPage.vue queda de la siguiente forma
```js
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
```
En su script queda de la siguiente forma:
```js
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
```
Para los estilos
```css
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
```
### 2.2) MainLayout
En el template queda de la siguiente forma:
```js
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
```
En el script de la siguiente:
```js
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
```

Como se utiliza las notificaciones hay que configurarlas de la siguiente forma:
En el archivo quasar.config.js hay que poner lo siguiente:
```js
...
plugins: [
        'Notify'
      ]
...
```