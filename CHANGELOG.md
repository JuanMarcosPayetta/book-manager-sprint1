# Changelog

## [Ejercicio 4]
- Servicios de CRUD para las 8 entidades, que delegan en los repositorios.
- ServicioStock con consultar_stock y descontar_stock, más StockInsuficienteError.
- ServicioCotizacionDolar con conversión entre monedas usando la cotización del dólar como puente, más CotizacionNoEncontradaError y ConversionNoSoportadaError.

## [Ejercicio 3]
- Definición de repositories.py con las interfaces IRepositorio, IRepositorioStock e IRepositorioCotizacionDolar.
- Un repositorio por entidad y persistencia en archivo CSV.
- Funciones auxiliares para evitar repetir el código de lectura y escritura.

## [Ejercicio 2]
- Definicion de EntidadBase (abstracta) con id validado y metodos to_dict/from_dict.
- Definicion de las clases Genero, Editorial, Moneda, TipoCotizacion, Libro, Precio, Stock y CotizacionDolar.
- Encapsulamiento con atributos privados y @property, con validaciones en los setter.

## [Ejercicio 1]
- Inicialización del repositorio en GitHub y creacion de la rama Sprint_1.
- Estructura inicial de directorios y archivos del proyecto.
- Creacion de README.md, CHANGELOG.md, requirements.txt, .gitignore.
- Configuracion de Git para realizar los commits.