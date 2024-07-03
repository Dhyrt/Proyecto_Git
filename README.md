# Sistema de Gestión de Órdenes de HealQuest Labs 📦💼💊

## Descripción
HealQuest Labs es un laboratorio farmacéutico dedicado a la producción y distribución de medicamentos. El objetivo de este proyecto es desarrollar un sistema de gestión de órdenes de compra, facturación y envío de productos a los clientes. El sistema permite a la empresa gestionar eficientemente las órdenes de compra, emitir facturas y despachar los productos a los destinatarios finales.

## Objetivo del Proyecto 🎯
El objetivo principal del proyecto es desarrollar un sistema que facilite la gestión de órdenes de compra, facturación y envío de productos en HealQuest Labs. Este sistema busca mejorar la eficiencia operativa y asegurar que los productos sean entregados de manera precisa y oportuna a los clientes.

## Alcance del Proyecto 🎯
El sistema desarrollado abarca las siguientes funcionalidades:
- Ingreso de Órdenes de Compra.
- Sistema de autenticación (login y logout).
- Visualización de órdenes de compra almacenadas.
- Emisión de facturas.
- Envío de productos a clientes.

## Requerimientos Funcionales ✔️
- **RF 1:** El sistema debe permitir ingresar las órdenes de compra con los datos mínimos necesarios (Dirección, teléfono, comuna, Región, productos, y precio).
- **RF 2:** El sistema debe tener un login de acceso con autenticación mediante contraseña almacenada en una base de datos.
- **RF 3:** El sistema debe tener un menú principal con opciones para mostrar las órdenes de compra, un botón para la página principal (home) y un botón para cerrar sesión.
- **RF 4:** El sistema debe emitir facturas cambiando el estado de la orden de compra a facturada, calculando el IVA (19%) y mostrando el monto total a pagar.
- **RF 5:** El sistema debe permitir el envío de productos agregando un texto indicativo de que los productos fueron despachados.

## Requerimientos No Funcionales 🚫
- **RNF 1:** El sistema debe ser fácil de usar y tener una interfaz intuitiva.
- **RNF 2:** El sistema debe ser seguro, protegiendo los datos de los usuarios y las transacciones.
- **RNF 3:** El sistema debe ser rápido y eficiente en la gestión de las órdenes y facturas.
- **RNF 4:** El sistema debe ser mantenible y escalable para futuras mejoras.

## Tecnologías Utilizadas 🛠️
- Python (Django): Utilizado para el desarrollo del backend y la lógica del servidor.
- HTML: Para la estructura del frontend.
- CSS: Para el estilo y diseño del frontend.
- Bootstrap: Para la creación de un frontend responsivo y atractivo.

### ¿Por qué Django? 🐍
Django es un framework de desarrollo web robusto y escalable que permite una rápida creación de aplicaciones seguras y mantenibles. Su arquitectura facilita el desarrollo al proporcionar componentes listos para usar, como el sistema de autenticación, la administración y ORM para bases de datos.

## Ejecución del Proyecto ▶️

### Requisitos Previos
- Python 3.x
- Django 3.x o superior
- Base de datos SQLite (por defecto en Django)
- Navegador web moderno

### Instrucciones de Instalación

1. Clonar el repositorio:
   ```
   git clone https://github.com/Dhyrt/Proyecto_Git.git
   ```
2. **Navegar al directorio del proyecto:**
   ```
   cd Proyecto_Git
   ```
3. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Realizar migraciones de la base de datos:
   ```
   python manage.py migrate
   ```
5. Ejecutar el servidor de desarrollo:
   ```
   python manage.py runserver
   ```
6. Abrir un navegador web y navegar a http://127.0.0.1:8000 para ver la aplicación en funcionamiento.
