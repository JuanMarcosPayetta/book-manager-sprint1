"""Carga de datos iniciales para Book Manager.

Crea 10 registros por entidad usando los repositorios, que son los que
escriben en los CSV. Si un id ya existe, la creación falla silenciosamente,
así que ejecutarlo dos veces no duplica datos.
"""

from datetime import date

from book_manager.entities.entities import (
    CotizacionDolar,
    Editorial,
    Genero,
    Libro,
    Moneda,
    Precio,
    Stock,
    TipoCotizacion,
)
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


def _crear_si_no_existe(repositorio, entidad) -> None:
    """Crea una entidad si su id no existe todavía.

    Args:
        repositorio: Repositorio con método crear.
        entidad: Entidad a crear.
    """
    try:
        repositorio.crear(entidad)
    except ValueError:
        pass


def precargar_datos(
    repo_generos: RepositorioGenero,
    repo_editoriales: RepositorioEditorial,
    repo_monedas: RepositorioMoneda,
    repo_tipos_cotizacion: RepositorioTipoCotizacion,
    repo_libros: RepositorioLibro,
    repo_precios: RepositorioPrecio,
    repo_stocks: RepositorioStock,
    repo_cotizaciones: RepositorioCotizacionDolar,
) -> None:
    """Crea 10 registros de cada entidad, coherentes entre sí.

    Args:
        repo_generos (RepositorioGenero): Repositorio de géneros.
        repo_editoriales (RepositorioEditorial): Repositorio de editoriales.
        repo_monedas (RepositorioMoneda): Repositorio de monedas.
        repo_tipos_cotizacion (RepositorioTipoCotizacion): Repositorio de tipos de cotización.
        repo_libros (RepositorioLibro): Repositorio de libros.
        repo_precios (RepositorioPrecio): Repositorio de precios.
        repo_stocks (RepositorioStock): Repositorio de stock.
        repo_cotizaciones (RepositorioCotizacionDolar): Repositorio de cotizaciones del dólar.
    """
    generos = [
        Genero(id=1, nombre="Novela"),
        Genero(id=2, nombre="Ensayo"),
        Genero(id=3, nombre="Infantil"),
        Genero(id=4, nombre="Técnico"),
        Genero(id=5, nombre="Poesía"),
        Genero(id=6, nombre="Historia"),
        Genero(id=7, nombre="Biografía"),
        Genero(id=8, nombre="Ciencia Ficción"),
        Genero(id=9, nombre="Policial"),
        Genero(id=10, nombre="Terror"),
    ]
    for genero in generos:
        _crear_si_no_existe(repo_generos, genero)

    editoriales = [
        Editorial(id=1, nombre="Planeta"),
        Editorial(id=2, nombre="Sudamericana"),
        Editorial(id=3, nombre="Alfaguara"),
        Editorial(id=4, nombre="Anagrama"),
        Editorial(id=5, nombre="Siglo XXI"),
        Editorial(id=6, nombre="Emecé"),
        Editorial(id=7, nombre="Paidós"),
        Editorial(id=8, nombre="Tusquets"),
        Editorial(id=9, nombre="Edhasa"),
        Editorial(id=10, nombre="Fondo de Cultura Económica"),
    ]
    for editorial in editoriales:
        _crear_si_no_existe(repo_editoriales, editorial)

    monedas = [
        Moneda(id=1, codigo="ARS"),
        Moneda(id=2, codigo="USD"),
        Moneda(id=3, codigo="EUR"),
        Moneda(id=4, codigo="BRL"),
        Moneda(id=5, codigo="CLP"),
        Moneda(id=6, codigo="UYU"),
        Moneda(id=7, codigo="PYG"),
        Moneda(id=8, codigo="BOB"),
        Moneda(id=9, codigo="GBP"),
        Moneda(id=10, codigo="JPY"),
    ]
    for moneda in monedas:
        _crear_si_no_existe(repo_monedas, moneda)

    tipos_cotizacion = [
        TipoCotizacion(id=1, nombre="Oficial"),
        TipoCotizacion(id=2, nombre="Blue"),
        TipoCotizacion(id=3, nombre="MEP"),
        TipoCotizacion(id=4, nombre="CCL"),
        TipoCotizacion(id=5, nombre="Turista"),
        TipoCotizacion(id=6, nombre="Mayorista"),
        TipoCotizacion(id=7, nombre="Cripto"),
        TipoCotizacion(id=8, nombre="Ahorro"),
        TipoCotizacion(id=9, nombre="Tarjeta"),
        TipoCotizacion(id=10, nombre="Solidario"),
    ]
    for tipo_cotizacion in tipos_cotizacion:
        _crear_si_no_existe(repo_tipos_cotizacion, tipo_cotizacion)

    libros = [
        Libro(id=1, isbn="9789500728956", titulo="Rayuela", autor="Julio Cortázar", genero_id=1, editorial_id=2),
        Libro(id=2, isbn="9788420471839", titulo="Cien años de soledad", autor="Gabriel García Márquez", genero_id=1, editorial_id=3),
        Libro(id=3, isbn="9789507319025", titulo="El Aleph", autor="Jorge Luis Borges", genero_id=1, editorial_id=6),
        Libro(id=4, isbn="9788433925906", titulo="2666", autor="Roberto Bolaño", genero_id=9, editorial_id=4),
        Libro(id=5, isbn="9789504911360", titulo="Ficciones", autor="Jorge Luis Borges", genero_id=1, editorial_id=6),
        Libro(id=6, isbn="9788437604947", titulo="Pedro Páramo", autor="Juan Rulfo", genero_id=1, editorial_id=3),
        Libro(id=7, isbn="9789872070597", titulo="Sapiens", autor="Yuval Noah Harari", genero_id=6, editorial_id=5),
        Libro(id=8, isbn="9788439732852", titulo="El Principito", autor="Antoine de Saint-Exupéry", genero_id=3, editorial_id=1),
        Libro(id=9, isbn="9788498387418", titulo="1984", autor="George Orwell", genero_id=8, editorial_id=9),
        Libro(id=10, isbn="9789505477239", titulo="Martín Fierro", autor="José Hernández", genero_id=5, editorial_id=10),
    ]
    for libro in libros:
        _crear_si_no_existe(repo_libros, libro)

    precios = [
        Precio(id=1, libro_id=1, moneda_id=1, monto=15000.0),
        Precio(id=2, libro_id=2, moneda_id=1, monto=18000.0),
        Precio(id=3, libro_id=3, moneda_id=1, monto=12000.0),
        Precio(id=4, libro_id=4, moneda_id=1, monto=22000.0),
        Precio(id=5, libro_id=5, moneda_id=1, monto=13000.0),
        Precio(id=6, libro_id=6, moneda_id=1, monto=14000.0),
        Precio(id=7, libro_id=7, moneda_id=1, monto=25000.0),
        Precio(id=8, libro_id=8, moneda_id=1, monto=9000.0),
        Precio(id=9, libro_id=9, moneda_id=1, monto=17000.0),
        Precio(id=10, libro_id=10, moneda_id=1, monto=16000.0),
    ]
    for precio in precios:
        _crear_si_no_existe(repo_precios, precio)

    stocks = [
        Stock(id=1, libro_id=1, cantidad=10),
        Stock(id=2, libro_id=2, cantidad=8),
        Stock(id=3, libro_id=3, cantidad=15),
        Stock(id=4, libro_id=4, cantidad=5),
        Stock(id=5, libro_id=5, cantidad=12),
        Stock(id=6, libro_id=6, cantidad=7),
        Stock(id=7, libro_id=7, cantidad=20),
        Stock(id=8, libro_id=8, cantidad=30),
        Stock(id=9, libro_id=9, cantidad=9),
        Stock(id=10, libro_id=10, cantidad=6),
    ]
    for stock in stocks:
        _crear_si_no_existe(repo_stocks, stock)

    cotizaciones = [
        CotizacionDolar(id=1, tipo_cotizacion_id=1, fecha=date(2026, 1, 2), valor=850.0),
        CotizacionDolar(id=2, tipo_cotizacion_id=2, fecha=date(2026, 1, 2), valor=1250.0),
        CotizacionDolar(id=3, tipo_cotizacion_id=3, fecha=date(2026, 1, 2), valor=1100.0),
        CotizacionDolar(id=4, tipo_cotizacion_id=1, fecha=date(2026, 1, 3), valor=855.0),
        CotizacionDolar(id=5, tipo_cotizacion_id=2, fecha=date(2026, 1, 3), valor=1260.0),
        CotizacionDolar(id=6, tipo_cotizacion_id=3, fecha=date(2026, 1, 3), valor=1105.0),
        CotizacionDolar(id=7, tipo_cotizacion_id=1, fecha=date(2026, 1, 4), valor=858.0),
        CotizacionDolar(id=8, tipo_cotizacion_id=2, fecha=date(2026, 1, 4), valor=1270.0),
        CotizacionDolar(id=9, tipo_cotizacion_id=3, fecha=date(2026, 1, 4), valor=1110.0),
        CotizacionDolar(id=10, tipo_cotizacion_id=1, fecha=date(2026, 1, 5), valor=860.0),
    ]
    for cotizacion in cotizaciones:
        _crear_si_no_existe(repo_cotizaciones, cotizacion)