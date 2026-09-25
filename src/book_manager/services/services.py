"""Logica de negocio de Book Manager.

Los servicios reciben sus repositorios por constructor.

La mayoria delega el CRUD en su repositorio. Stock y CotizacionDolar
tienen reglas de negocio propias, con excepciones especificas.
"""

from datetime import date
from typing import List, Optional

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
    IRepositorio,
    IRepositorioCotizacionDolar,
    IRepositorioStock
)


class StockInsuficienteError(Exception):
    """Se lanza cuando no hay stock suficiente para descontar una cantidad."""

    def __init__(self, libro_id: int, cantidad_solicitada: int, cantidad_disponible: int) -> None:
        """Inicializa la excepción.

        Args:
            libro_id (int): ID del libro sin stock suficiente.
            cantidad_solicitada (int): Cantidad que se intentó descontar.
            cantidad_disponible (int): Cantidad realmente disponible.
        """
        self.libro_id = libro_id
        self.cantidad_solicitada = cantidad_solicitada
        self.cantidad_disponible = cantidad_disponible
        super().__init__(
            f"Stock insuficiente para libro_id={libro_id}: "
            f"se pidieron {cantidad_solicitada}, hay {cantidad_disponible}"
        )


class CotizacionNoEncontradaError(Exception):
    """Se lanza cuando no hay cotización registrada para un tipo y fecha."""

    def __init__(self, tipo_cotizacion_id: int, fecha: date) -> None:
        """Inicializa la excepción.

        Args:
            tipo_cotizacion_id (int): ID del tipo de cotizacion buscado.
            fecha (date): Fecha para la que se busco la cotización.
        """
        self.tipo_cotizacion_id = tipo_cotizacion_id
        self.fecha = fecha
        super().__init__(
            f"No hay cotización para tipo_cotizacion_id={tipo_cotizacion_id} y fecha={fecha}"
        )


class ConversionNoSoportadaError(Exception):
    """Se lanza cuando no hay informacion suficiente para convertir entre dos monedas."""

    def __init__(self, moneda_origen: str, moneda_destino: str) -> None:
        """Inicializa la excepción.

        Args:
            moneda_origen (str): Código de la moneda de origen.
            moneda_destino (str): Código de la moneda de destino.
        """
        self.moneda_origen = moneda_origen
        self.moneda_destino = moneda_destino
        super().__init__(
            f"No se puede convertir de {moneda_origen} a {moneda_destino} "
            "con la información disponible (solo se admite ARS <-> USD)"
        )


class ServicioGenero:
    """CRUD de Genero, delegado en su repositorio."""

    def __init__(self, repositorio: IRepositorio[Genero]) -> None:
        """Inicializa el servicio.

        Args:
            repositorio (IRepositorio[Genero]): Repositorio de géneros.
        """
        self.__repositorio = repositorio

    def crear(self, genero: Genero) -> Genero:
        return self.__repositorio.crear(genero)

    def leer_por_id(self, id: int) -> Optional[Genero]:
        return self.__repositorio.leer_por_id(id)

    def leer_todos(self) -> List[Genero]:
        return self.__repositorio.leer_todos()

    def actualizar(self, genero: Genero) -> Genero:
        return self.__repositorio.actualizar(genero)

    def eliminar(self, id: int) -> bool:
        return self.__repositorio.eliminar(id)


class ServicioEditorial:
    """CRUD de Editorial, delegado en su repositorio."""

    def __init__(self, repositorio: IRepositorio[Editorial]) -> None:
        """Inicializa el servicio.

        Args:
            repositorio (IRepositorio[Editorial]): Repositorio de editoriales.
        """
        self.__repositorio = repositorio

    def crear(self, editorial: Editorial) -> Editorial:
        return self.__repositorio.crear(editorial)

    def leer_por_id(self, id: int) -> Optional[Editorial]:
        return self.__repositorio.leer_por_id(id)

    def leer_todos(self) -> List[Editorial]:
        return self.__repositorio.leer_todos()

    def actualizar(self, editorial: Editorial) -> Editorial:
        return self.__repositorio.actualizar(editorial)

    def eliminar(self, id: int) -> bool:
        return self.__repositorio.eliminar(id)


class ServicioMoneda:
    """CRUD de Moneda, delegado en su repositorio."""

    def __init__(self, repositorio: IRepositorio[Moneda]) -> None:
        """Inicializa el servicio.

        Args:
            repositorio (IRepositorio[Moneda]): Repositorio de monedas.
        """
        self.__repositorio = repositorio

    def crear(self, moneda: Moneda) -> Moneda:
        return self.__repositorio.crear(moneda)

    def leer_por_id(self, id: int) -> Optional[Moneda]:
        return self.__repositorio.leer_por_id(id)

    def leer_todos(self) -> List[Moneda]:
        return self.__repositorio.leer_todos()

    def actualizar(self, moneda: Moneda) -> Moneda:
        return self.__repositorio.actualizar(moneda)

    def eliminar(self, id: int) -> bool:
        return self.__repositorio.eliminar(id)


class ServicioTipoCotizacion:
    """CRUD de TipoCotizacion, delegado en su repositorio."""

    def __init__(self, repositorio: IRepositorio[TipoCotizacion]) -> None:
        """Inicializa el servicio.

        Args:
            repositorio (IRepositorio[TipoCotizacion]): Repositorio de tipos de cotización.
        """
        self.__repositorio = repositorio

    def crear(self, tipo_cotizacion: TipoCotizacion) -> TipoCotizacion:
        return self.__repositorio.crear(tipo_cotizacion)

    def leer_por_id(self, id: int) -> Optional[TipoCotizacion]:
        return self.__repositorio.leer_por_id(id)

    def leer_todos(self) -> List[TipoCotizacion]:
        return self.__repositorio.leer_todos()

    def actualizar(self, tipo_cotizacion: TipoCotizacion) -> TipoCotizacion:
        return self.__repositorio.actualizar(tipo_cotizacion)

    def eliminar(self, id: int) -> bool:
        return self.__repositorio.eliminar(id)


class ServicioLibro:
    """CRUD de Libro, delegado en su repositorio."""

    def __init__(self, repositorio: IRepositorio[Libro]) -> None:
        """Inicializa el servicio.

        Args:
            repositorio (IRepositorio[Libro]): Repositorio de libros.
        """
        self.__repositorio = repositorio

    def crear(self, libro: Libro) -> Libro:
        return self.__repositorio.crear(libro)

    def leer_por_id(self, id: int) -> Optional[Libro]:
        return self.__repositorio.leer_por_id(id)

    def leer_todos(self) -> List[Libro]:
        return self.__repositorio.leer_todos()

    def actualizar(self, libro: Libro) -> Libro:
        return self.__repositorio.actualizar(libro)

    def eliminar(self, id: int) -> bool:
        return self.__repositorio.eliminar(id)


class ServicioPrecio:
    """CRUD de Precio, delegado en su repositorio."""

    def __init__(self, repositorio: IRepositorio[Precio]) -> None:
        """Inicializa el servicio.

        Args:
            repositorio (IRepositorio[Precio]): Repositorio de precios.
        """
        self.__repositorio = repositorio

    def crear(self, precio: Precio) -> Precio:
        return self.__repositorio.crear(precio)

    def leer_por_id(self, id: int) -> Optional[Precio]:
        return self.__repositorio.leer_por_id(id)

    def leer_todos(self) -> List[Precio]:
        return self.__repositorio.leer_todos()

    def actualizar(self, precio: Precio) -> Precio:
        return self.__repositorio.actualizar(precio)

    def eliminar(self, id: int) -> bool:
        return self.__repositorio.eliminar(id)


class ServicioStock:
    """CRUD de Stock (por libro_id) más las reglas de negocio sobre existencias."""

    def __init__(self, repositorio: IRepositorioStock) -> None:
        """Inicializa el servicio.

        Args:
            repositorio (IRepositorioStock): Repositorio de stock.
        """
        self.__repositorio = repositorio

    def crear(self, stock: Stock) -> Stock:
        return self.__repositorio.crear(stock)

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        return self.__repositorio.leer_por_libro(libro_id)

    def actualizar(self, stock: Stock) -> Stock:
        return self.__repositorio.actualizar(stock)

    def eliminar(self, libro_id: int) -> bool:
        return self.__repositorio.eliminar(libro_id)

    def consultar_stock(self, libro_id: int) -> int:
        """Consulta la cantidad disponible de un libro.

        Args:
            libro_id (int): ID del libro a consultar.

        Returns:
            int: Cantidad disponible (0 si no hay registro de stock).
        """
        stock = self.__repositorio.leer_por_libro(libro_id)
        return stock.cantidad if stock else 0

    def descontar_stock(self, libro_id: int, cantidad: int) -> Stock:
        """Descuenta unidades del stock de un libro (por ejemplo, al venderlo).

        Args:
            libro_id (int): ID del libro.
            cantidad (int): Cantidad a descontar.

        Returns:
            Stock: El registro de stock actualizado.

        Raises:
            StockInsuficienteError: Si no hay unidades suficientes.
        """
        stock = self.__repositorio.leer_por_libro(libro_id)
        disponible = stock.cantidad if stock else 0
        if disponible < cantidad:
            raise StockInsuficienteError(libro_id, cantidad, disponible)
        stock.cantidad = disponible - cantidad
        return self.__repositorio.actualizar(stock)


class ServicioCotizacionDolar:
    """CRUD de CotizacionDolar más la conversión de montos entre monedas."""

    def __init__(self, repositorio: IRepositorioCotizacionDolar) -> None:
        """Inicializa el servicio.

        Args:
            repositorio (IRepositorioCotizacionDolar): Repositorio de cotizaciones.
        """
        self.__repositorio = repositorio

    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        return self.__repositorio.crear(cotizacion)

    def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: date) -> Optional[CotizacionDolar]:
        return self.__repositorio.leer_por_tipo_y_fecha(tipo_id, fecha)

    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        return self.__repositorio.leer_historico_por_tipo(tipo_id)

    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        return self.__repositorio.actualizar(cotizacion)

    def eliminar(self, tipo_id: int, fecha: date) -> bool:
        return self.__repositorio.eliminar(tipo_id, fecha)

    def convertir(
        self,
        monto: float,
        moneda_origen: str,
        moneda_destino: str,
        tipo_cotizacion_id: int,
        fecha: date,
    ) -> float:
        """Convierte un monto de una moneda a otra usando el dólar como puente.

        Si ambas monedas son la misma, devuelve el monto sin cambios.
        Con la información disponible, solo se puede convertir entre ARS y USD.

        Args:
            monto (float): Monto a convertir.
            moneda_origen (str): Código de la moneda de origen.
            moneda_destino (str): Código de la moneda de destino.
            tipo_cotizacion_id (int): Tipo de cotización a usar como puente.
            fecha (date): Fecha de la cotización.

        Returns:
            float: El monto convertido.

        Raises:
            CotizacionNoEncontradaError: Si no hay cotización para ese tipo y fecha.
            ConversionNoSoportadaError: Si la conversión pedida no es ARS<->USD.
        """
        origen = moneda_origen.upper()
        destino = moneda_destino.upper()

        if origen == destino:
            return monto

        cotizacion = self.__repositorio.leer_por_tipo_y_fecha(tipo_cotizacion_id, fecha)
        if cotizacion is None:
            raise CotizacionNoEncontradaError(tipo_cotizacion_id, fecha)

        if origen == "USD" and destino == "ARS":
            return monto * cotizacion.valor
        if origen == "ARS" and destino == "USD":
            return monto / cotizacion.valor

        raise ConversionNoSoportadaError(origen, destino)