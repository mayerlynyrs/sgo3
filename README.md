# SGO
# Fiirmatec

Sistema de Gestión de Operaciones.
Plataforma de Firma Electrónica simple de contratos.

## Getting started

Dentro de esta sección se tratarán los temas necesarios para poder descargar,
instalar y ejecutar la aplicación SGO.

### Requisitos

A continuación se listan los elementos de *software* básicos para poder ejecutar
la aplicación de manera local:

*   Python: Tener instalado y funcionando python.
        (Durante la instalación, marque Agregar Python 3 a la RUTA `Add Python 3 to PATH`, luego haga clic en Personalizar instalación `Customize Installation` y asegúrese de que `pip` esté marcado.)

    Visual Studio Code
    Git
    Postgres 12 Git (clave root)


### Instalación
En esta sección se explicará el cómo descargar y ejecutar el proyecto.

Dentro del repositorio donde esta alojado el proyecto en GitHub.com, se encuentra un botón
verde en donde se puede clonar el repositorio (Code/Código), se selecciona el botón 'code/Código'
y se copia la URL para clonar el proyecto. 
La url de este botón le entregará el siguiente enlace:

`https://github.com/empresasintegra/sgo3.git`

No se recomienda crear una carpeta para el proyecto, se debe descargar (clonar)
el proyecto con el siguiente comando, ejecutado desde la terminal de Visual Studio Code

`git clone https://github.com/empresasintegra/sgo3.git`

Una vez descargado proyecto debes correr los siguientes comandos desde la terminal de Visual Studio Code.

Debes ejecutar el powershell como administrador y ejecutar el comando `Set-ExecutionPolicy Unrestricted`, para habilitar ejecución de scripts visual studio code

Una vez clonado el repositorio se debe ingresar a la carpeta
y ejecutar los siguientes comandos, para crear y activar el entorno virtual.

```
cd sgo3
python -m venv .envs
.envs\Scripts\activate
pip install -r requirements.txt
```

Una vez ejecutado los siguientes comandos.

#### Creación de la base de datos

- Se debe abrir pgAdmin 4 y crear la base de datos (nombre de la base de datos `sgo`)

- Dentro de la carpeta del proyecto ejecutar el siguiente 
comando para crear la base de datos del proyecto a partir de los modelos.
 ```
python manage.py makemigrations
python manage.py migrate
``` 
- Para correr el proyecto
```
python manage.py runserver
```

### Ejecución

Una vez ejecutado este código la aplicación puede encontrarse en:

`http://127.0.0.1:8000`

Los usuarios de prueba son:
```
Usuario           RUT         Clave
Administrador    12345678     1234
Trabajador       87654321     1234*
```

### Actualizar Proyecto
```
git origin master
```

## Tecnologías utilizadas

Acá se dan a conocer los lenguajes usados en el desarrollo de la plataforma, junto con sus respectivas versiones.

* Python 3.6
* Javascript ECMA 5+
* HTML
* CSS

## Nuevo en esta versión

Las siguientes características se han añadido a esta versión de la aplicación:

### Version 0.1 alpha

*   Se crearon los modulos base: cliente, planta, para el funcionamiento del sistema. El modulo de usuarios,
    la recuperación de contraseña via correo electrónico y el modulo de ficheros digitales.

## Autor

*   **EmpresasIntegra** - [TDC]()
