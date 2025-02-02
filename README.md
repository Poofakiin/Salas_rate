# 2023-2-Grupo-8
![alt text](ReseñasSalasBeauchef/static/images/Logo.png)

Integrantes:
- Antonio Vitalic
- Benjamín Aguilar
- Ignacio Mella
- José Pereira
- Raúl Aliste


# Reseñas Salas Beauchef
Es una aplicación web que permite a los estudiantes de la Facultad de Ciencias Físicas y Matemáticas de la Universidad de Chile, realizar reseñas de las salas de estudio de la facultad, con el fin de ayudar a los estudiantes a elegir la sala que más se acomode a sus necesidades.

## Instalación
Para instalar el proyecto se debe clonar el repositorio y luego instalar las dependencias necesarias para el funcionamiento del proyecto. Para esto se debe ejecutar el siguiente comando en la carpeta raíz del proyecto:
```bash
pip install -r requirements.txt
```
## Ejecución
Para ejecutar el proyecto se debe ejecutar el siguiente comando en la carpeta raíz del proyecto:
```bash
python manage.py runserver
```
Luego se debe ingresar a la dirección http://127.0.0.1:8000/

# Descripción

Apenas el usuario ingresa a la página, se encuentra con la portada, en la cual encontrará una barra de navegación superior: 

Inicio | Todas las Salas | Salas por Edificio | Sobre Nosotros | Novedades | Hacer Reseña | Iniciar Sesión | Registrarse

# Inicio
En esta sección se encuentra la portada, la que presenta información general de la página

## Todas las Salas
En esta sección se encuentran todas las salas de la facultad, con los siguientes atributos: 

Nombre Sala	| Edificio	| Capacidad Normal	| Capacidad Examen	| Aforo	| Híbrido |	Calificación Promedio Global | 	Calificación Promedio Atributo |	Link

Nombre Sala: Nombre de la sala de estudio (string)

Edificio: Edificio en el que se encuentra la sala (string)

Capacidad Normal: Capacidad de la sala en condiciones normales (int)

Capacidad Examen: Capacidad de la sala en condiciones de examen (int)

Aforo: Aforo de la sala, dato relevante para los tiempos de pandemia de COVID-19 (int)

Híbrido: Indica si la sala es híbrida o no (bool)

Calificación Promedio Global: Calificación promedio de la sala (float)

Calificación Promedio Atributo: Calificación promedio de los atributos de la sala (float)

Link: Link a la página de U-Campus de la sala (string)

## Salas por Edificio
En esta sección se encuentran todas las salas de la facultad, agrupadas por edificio.

## Sobre Nosotros
En esta sección se encuentra información sobre el grupo de trabajo.

## Novedades
En esta sección se encuentran las últimas novedades de la página.

## Hacer Reseña
En esta sección se encuentra el formulario para realizar una reseña de una sala de estudio.

## Iniciar Sesión
En esta sección se encuentra el formulario para iniciar sesión en la página.

## Registrarse
En esta sección se encuentra el formulario para registrarse en la página.

© 2023 Reseñas Salas Beauchef. Todos los derechos reservados.
