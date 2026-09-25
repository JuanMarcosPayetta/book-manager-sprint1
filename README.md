# Book Manager

## Sprint 1

### Integrantes

- Vicente Franco Damián
- Da Silva César Augusto
- Simonetta Sebastian
- Juan Marcos Payetta 

### Objetivo

El objetivo principal de este proyecto es aplicar los conocimientos adquiridos en programación orientada a objetos, almacenamiento de datos en archivos para su persistencia.

### Introducción y contexto del problema

Una librería con venta al público necesita modernizar su sistema de gestión de inventario de libros. Debido a la fluctuación en los costos de importación de material bibliográfico, el sistema debe gestionar precios en diferentes monedas y seguir de cerca la cotización del dólar para actualizar sus valores en tiempo real.

El objetivo es desarrollar una aplicación de consola (CLI) robusta en Python que permita gestionar el inventario de una librería, cotizar los libros en tiempo real según el valor del dólar y comparar precios automáticamente con la competencia web.

### Entidades del dominio

- **Libro**: cada título del catálogo (isbn, título, autor, género, editorial).
- **Genero**: categoría literaria (novela, ensayo, infantil, técnico, etc.).
- **Editorial**: proveedor/distribuidora que provee los libros.
- **Moneda**: monedas en las que se puede expresar un precio (ARS, USD, etc.).
- **TipoCotizacion**: tipos de cotización del dólar (Oficial, Blue, MEP, etc.).
- **Precio**: valor monetario asociado a un libro en una moneda determinada.
- **Stock**: cantidad disponible de cada libro.
- **CotizacionDolar**: registro histórico de cotizaciones por tipo y fecha.

### Repositorio

https://github.com/JuanMarcosPayetta/book-manager-sprint1

### Persistencia y reproducibilidad

Todos los archivos del proyecto (codigo y CSV de datos) se encuentran en este repositorio y son versionados con Git. En Colab se clona el repositorio, se ejecuta `main()` y se muestra el resultado.




