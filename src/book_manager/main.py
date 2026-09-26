"""Inicio del Book Manager."""

import os

from book_manager.preload_data.preload_data import precargar_datos
from book_manager.repositories.repositories import (
    RepositorioCotizacionDolar,
    RepositorioEditorial,
    RepositorioGenero,
    RepositorioLibro,
    RepositorioMoneda,
    RepositorioPrecio,
    RepositorioStock,
    RepositorioTipoCotizacion,
)
from book_manager.services.services import (
    ServicioCotizacionDolar,
    ServicioEditorial,
    ServicioGenero,
    ServicioLibro,
    ServicioMoneda,
    ServicioPrecio,
    ServicioStock,
    ServicioTipoCotizacion,
)
from book_manager.ui.console import iniciar_consola

# Rutas relativas a este archivo, asi funciona sin importar desde donde se ejecute
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_MIGRATIONS_CSV = os.path.join(RUTA_BASE, "migrations", "csv")

RUTA_CSV_GENEROS = os.path.join(RUTA_MIGRATIONS_CSV, "generos.csv")
RUTA_CSV_EDITORIALES = os.path.join(RUTA_MIGRATIONS_CSV, "editoriales.csv")
RUTA_CSV_MONEDAS = os.path.join(RUTA_MIGRATIONS_CSV, "monedas.csv")
RUTA_CSV_TIPOS_COTIZACION = os.path.join(RUTA_MIGRATIONS_CSV, "tipos_cotizacion.csv")
RUTA_CSV_LIBROS = os.path.join(RUTA_MIGRATIONS_CSV, "libros.csv")
RUTA_CSV_PRECIOS = os.path.join(RUTA_MIGRATIONS_CSV, "precios.csv")
RUTA_CSV_STOCKS = os.path.join(RUTA_MIGRATIONS_CSV, "stocks.csv")
RUTA_CSV_COTIZACIONES = os.path.join(RUTA_MIGRATIONS_CSV, "cotizaciones_dolar.csv")


def main(import_default_data: bool = False) -> None:
    """Punto de entrada del sistema.

    Args:
        import_default_data (bool): Si es True, precarga los datos semilla
        antes de iniciar la consola. Si es False, no precarga nada
    """
    repo_generos = RepositorioGenero(RUTA_CSV_GENEROS)
    repo_editoriales = RepositorioEditorial(RUTA_CSV_EDITORIALES)
    repo_monedas = RepositorioMoneda(RUTA_CSV_MONEDAS)
    repo_tipos_cotizacion = RepositorioTipoCotizacion(RUTA_CSV_TIPOS_COTIZACION)
    repo_libros = RepositorioLibro(RUTA_CSV_LIBROS)
    repo_precios = RepositorioPrecio(RUTA_CSV_PRECIOS)
    repo_stocks = RepositorioStock(RUTA_CSV_STOCKS)
    repo_cotizaciones = RepositorioCotizacionDolar(RUTA_CSV_COTIZACIONES)

    if import_default_data:
        precargar_datos(
            repo_generos,
            repo_editoriales,
            repo_monedas,
            repo_tipos_cotizacion,
            repo_libros,
            repo_precios,
            repo_stocks,
            repo_cotizaciones,
        )

    iniciar_consola(
        ServicioGenero(repo_generos),
        ServicioEditorial(repo_editoriales),
        ServicioMoneda(repo_monedas),
        ServicioTipoCotizacion(repo_tipos_cotizacion),
        ServicioLibro(repo_libros),
        ServicioPrecio(repo_precios),
        ServicioStock(repo_stocks),
        ServicioCotizacionDolar(repo_cotizaciones),
    )