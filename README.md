# API REST- Flask (VideoApp)
API REST - Flask. Esta es una API básica que proporciona varios endpoints, para autenticar y registrar usuarios ,ademas de la posibilidad de carga de videos que deseen sus usuarios Esta aplicación está desarrollada para el curso de Desarrollo de Soluciones Cloud. 

# VM de despliegue 

Para ejecutar la aplicación siga las siguientes instrucciones: 

## Instalar dependecias de proyecto
> * ```$ python3 -m venv nuevo_ambiente```
> * ```$ source nuevo_ambiente/bin/activate```
> * ```$ cd flaskr```
> * ```$ pip install -r requirements.txt```
> * ```$ mkdir videos```

## Ejecutar
> * ```$ flask run -h 0.0.0.0```

## Consumir los servicios
* Utilice Postman (o una herramienta equivalente) para realizar solicitudes post a los endpoints disponibles. 
> * Ruta Endpoint 1 [POST]: ```http://ip_servidor:5000/api/auth/singup```
> * Ruta Endpoint 2 [POST]: ```http://ip_servidor:5000/api/auth/login```
> * Ruta Endpoint 3 [POST]: ```http://ip_servidor:5000/api/tasks```
> * Ruta Endpoint 4 [GET]: ```http://ip_servidor:5000/api/tasks```
> * Ruta Endpoint 5 [POST]: ```http://ip_servidor:5000/api/task/id```
> * Ruta Endpoint 6 [DEL]:```http://ip_servidor:5000/api/task/id```
