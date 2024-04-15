# API REST- Flask (VideoApp)
API REST - Flask. Esta es una API básica que proporciona varios endpoints, para autenticar y registrar usuarios ,ademas de la posibilidad de carga de videos que deseen sus usuarios Esta aplicación está desarrollada para el curso de Desarrollo de Soluciones Cloud. 

# VM de despliegue 

Para ejecutar la aplicación siga las siguientes instrucciones: 

## Instalación

1. Clona el repositorio de Flaskr:

```
git clone https://github.com/Erikolierq/MISW4204_BackEndRest_24
```

2. Instala las dependencias:

```
pip install -r requirements.txt
```

3. Inicia Redis Server:

```
sudo service redis-server start
```

## Ejecución

Para ejecutar la aplicación Flask, sigue estos pasos:

1. Abre una terminal y navega hasta la carpeta `flaskr`.

2. Ejecuta el siguiente comando para iniciar la aplicación:

```
flask run
```

Para ejecutar Celery y procesar tareas en segundo plano, utiliza el siguiente comando:

```
celery -A flaskr.modelos.tareas worker --pool=solo -l info
```

## APIs Disponibles

- **Registro de Usuario**: 
  - Método: `POST`
  - URL: `/api/auth/singup`

- **Inicio de Sesión**: 
  - Método: `POST`
  - URL: `/api/auth/login`

- **Obtener Lista de Tareas**: 
  - Método: `GET`
  - URL: `/api/tasks`

- **Obtener Detalles de una Tarea Específica**: 
  - Método: `GET`
  - URL: `/api/task/<int:id>`
