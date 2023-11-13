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
