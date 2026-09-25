"""Persistencia de las entidades en archivos CSV.

Cada entidad se guarda en su propio archivo dentro de migrations/csv/.

Genero, Editorial, Moneda, TipoCotizacion, Libro y Precio usan
RepositorioCSV, que implementa IRepositorio[T]. Stock y CotizacionDolar
usan claves distintas (libro_id, y tipo_cotizacion_id + fecha) por eso
tienen sus propias clases.
"""

import csv
import os
from abc import ABC, abstractmethod
from datetime import date
from typing import Generic, List, Optional, TypeVar

from book_manager.entities.entities import (
    CotizacionDolar,
    Editorial,
    EntidadBase,
    Genero,
    Libro,
    Moneda,
    Precio,
    Stock,
    TipoCotizacion,
)

T = TypeVar("T", bound=EntidadBase)


class IRepositorio(ABC, Generic[T]):
    """Interfaz para repositorios que manejan entidades con operaciones CRUD basicas."""

    @abstractmethod
    def crear(self, entidad: T) -> T:
        """Crea una nueva entidad en el repositorio.

        Args:
            entidad (T): La entidad a crear.

        Returns:
            T: La entidad creada.

        Raises:
            ValueError: Si ya existe una entidad con el mismo ID.
        """
        pass

    @abstractmethod
    def leer_por_id(self, id: int) -> Optional[T]:
        """Lee una entidad del repositorio por su ID.

        Args:
            id (int): El ID de la entidad a leer.

        Returns:
            Optional[T]: La entidad si se encuentra, None en caso contrario.
        """
        pass

    @abstractmethod
    def leer_todos(self) -> List[T]:
        """Lee todas las entidades del repositorio.

        Returns:
            List[T]: Una lista de todas las entidades.
        """
        pass

    @abstractmethod
    def actualizar(self, entidad: T) -> T:
        """Actualiza una entidad existente en el repositorio.

        Args:
            entidad (T): La entidad a actualizar (debe tener un ID existente).

        Returns:
            T: La entidad actualizada.

        Raises:
            ValueError: Si no se encuentra la entidad para actualizar.
        """
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina una entidad del repositorio por su ID.

        Args:
            id (int): El ID de la entidad a eliminar.

        Returns:
            bool: True si la entidad fue eliminada, False si no se encontro.
        """
        pass


class IRepositorioStock(ABC):
    """Interfaz para repositorios del tipo Stock."""

    @abstractmethod
    def crear(self, stock: Stock) -> Stock:
        """Crea un nuevo registro de stock.

        Args:
            stock (Stock): El objeto Stock a crear.

        Returns:
            Stock: El objeto Stock creado.

        Raises:
            ValueError: Si ya existe un registro de stock para el mismo libro.
        """
        pass

    @abstractmethod
    def leer_por_libro(self, libro_id: int) -> Optional["Stock"]:
        """Lee un registro de stock por ID de libro.

        Args:
            libro_id (int): El ID del libro asociado al stock.

        Returns:
            Optional[Stock]: El objeto Stock si se encuentra, None en caso contrario.
        """
        pass

    @abstractmethod
    def actualizar(self, stock: "Stock") -> "Stock":
        """Actualiza un registro de stock existente.

        Args:
            stock (Stock): El objeto Stock a actualizar (debe tener un libro_id existente).

        Returns:
            Stock: El objeto Stock actualizado.

        Raises:
            ValueError: Si no se encuentra el stock para actualizar.
        """
        pass

    @abstractmethod
    def eliminar(self, libro_id: int) -> bool:
        """Elimina un registro de stock por ID de libro.

        Args:
            libro_id (int): El ID del libro asociado al stock a eliminar.

        Returns:
            bool: True si el stock fue eliminado, False si no se encontró.
        """
        pass


class IRepositorioCotizacionDolar(ABC):
    """Interfaz para repositorios del tipo RepositorioCotizacionDolar."""

    @abstractmethod
    def crear(self, cotizacion: "CotizacionDolar") -> "CotizacionDolar":
        """Crea una nueva cotización de dólar.

        Args:
            cotizacion (CotizacionDolar): El objeto CotizacionDolar a crear.

        Returns:
            CotizacionDolar: El objeto CotizacionDolar creado.

        Raises:
            ValueError: Si ya existe una cotización para el mismo tipo y fecha.
        """
        pass

    @abstractmethod
    def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: date) -> Optional["CotizacionDolar"]:
        """Lee una cotización de dólar por tipo y fecha.

        Args:
            tipo_id (int): El ID del tipo de cotización.
            fecha (date): La fecha de la cotización.

        Returns:
            Optional[CotizacionDolar]: La cotización si se encuentra, None en caso contrario.
        """
        pass

    @abstractmethod
    def leer_historico_por_tipo(self, tipo_id: int) -> List["CotizacionDolar"]:
        """Lee el histórico de cotizaciones para un tipo específico.

        Args:
            tipo_id (int): El ID del tipo de cotización.

        Returns:
            List[CotizacionDolar]: Una lista de cotizaciones históricas para el tipo dado.
        """
        pass

    @abstractmethod
    def actualizar(self, cotizacion: "CotizacionDolar") -> "CotizacionDolar":
        """Actualiza una cotización de dólar existente.

        Args:
            cotizacion (CotizacionDolar): El objeto CotizacionDolar a actualizar.

        Returns:
            CotizacionDolar: El objeto CotizacionDolar actualizado.

        Raises:
            ValueError: Si no se encuentra la cotización para actualizar.
        """
        pass

    @abstractmethod
    def eliminar(self, tipo_id: int, fecha: date) -> bool:
        """Elimina una cotización de dólar por tipo y fecha.

        Args:
            tipo_id (int): El ID del tipo de cotización.
            fecha (date): La fecha de la cotización a eliminar.

        Returns:
            bool: True si la cotización fue eliminada, False si no se encontró.
        """
        pass


def _leer_filas_csv(ruta: str) -> List[dict]:
    """Lee todas las filas de un CSV como diccionarios.

    Args:
        ruta (str): Ubicación del archivo CSV.

    Returns:
        List[dict]: Lista de diccionarios (vacía si el archivo no existe).
    """
    if not os.path.exists(ruta):
        return []
    with open(ruta, newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def _escribir_filas_csv(ruta: str, campos: List[str], filas: List[dict]) -> None:
    """Sobrescribe un CSV completo con las filas dadas.

    Args:
        ruta (str): Ubicación del archivo CSV.
        campos (List[str]): Nombres de las columnas.
        filas (List[dict]): Diccionarios a escribir, uno por fila.
    """
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas)


def _crear_en_csv(ruta: str, campos: List[str], entidad: EntidadBase) -> None:
    """Agrega una entidad a un CSV si su id no existe todavía.

    Args:
        ruta (str): Archivo CSV donde persiste la entidad.
        campos (List[str]): Nombres de las columnas.
        entidad (EntidadBase): Entidad a crear.

    Raises:
        ValueError: Si ya existe una entidad con el mismo id.
    """
    filas = _leer_filas_csv(ruta)
    if any(int(fila["id"]) == entidad.id for fila in filas):
        raise ValueError(f"Ya existe una entidad con id={entidad.id}")
    filas.append(entidad.to_dict())
    _escribir_filas_csv(ruta, campos, filas)


def _leer_por_id_en_csv(ruta: str, clase_entidad: type, id: int) -> Optional[EntidadBase]:
    """Busca una entidad por id en un CSV.

    Args:
        ruta (str): Archivo CSV donde persiste la entidad.
        clase_entidad (type): Clase para reconstruir la entidad.
        id (int): Id a buscar.

    Returns:
        Optional[EntidadBase]: La entidad si se encuentra, None si no.
    """
    for fila in _leer_filas_csv(ruta):
        if int(fila["id"]) == id:
            return clase_entidad.from_dict(fila)
    return None


def _leer_todos_en_csv(ruta: str, clase_entidad: type) -> List[EntidadBase]:
    """Lee todas las entidades de un CSV.

    Args:
        ruta (str): Archivo CSV donde persisten las entidades.
        clase_entidad (type): Clase para reconstruir cada entidad.

    Returns:
        List[EntidadBase]: Todas las entidades persistidas.
    """
    return [clase_entidad.from_dict(fila) for fila in _leer_filas_csv(ruta)]


def _actualizar_en_csv(ruta: str, campos: List[str], entidad: EntidadBase) -> bool:
    """Reemplaza en un CSV la fila con el mismo id que la entidad dada.

    Args:
        ruta (str): Archivo CSV donde persiste la entidad.
        campos (List[str]): Nombres de las columnas.
        entidad (EntidadBase): Entidad con los datos actualizados.

    Returns:
        bool: True si se encontró y actualizó, False si no existía.
    """
    filas = _leer_filas_csv(ruta)
    for indice, fila in enumerate(filas):
        if int(fila["id"]) == entidad.id:
            filas[indice] = entidad.to_dict()
            _escribir_filas_csv(ruta, campos, filas)
            return True
    return False


def _eliminar_de_csv(ruta: str, id: int) -> bool:
    """Elimina de un CSV la fila con el id dado.

    Args:
        ruta (str): Archivo CSV donde persiste la entidad.
        id (int): Id de la fila a eliminar.

    Returns:
        bool: True si se encontró y eliminó, False si no existía.
    """
    filas = _leer_filas_csv(ruta)
    if not filas:
        return False
    campos = list(filas[0].keys())
    restantes = [fila for fila in filas if int(fila["id"]) != id]
    if len(restantes) == len(filas):
        return False
    _escribir_filas_csv(ruta, campos, restantes)
    return True


class RepositorioGenero(IRepositorio[Genero]):
    """Repositorio de Genero, persistido en CSV."""

    CAMPOS: List[str] = ["id", "nombre"]

    def __init__(self, ruta_csv: str) -> None:
        """Inicializa el repositorio.

        Args:
            ruta_csv (str): Archivo CSV donde se persisten los registros.
        """
        self.__ruta_csv = ruta_csv

    def crear(self, entidad: Genero) -> Genero:
        _crear_en_csv(self.__ruta_csv, self.CAMPOS, entidad)
        return entidad

    def leer_por_id(self, id: int) -> Optional[Genero]:
        return _leer_por_id_en_csv(self.__ruta_csv, Genero, id)

    def leer_todos(self) -> List[Genero]:
        return _leer_todos_en_csv(self.__ruta_csv, Genero)

    def actualizar(self, entidad: Genero) -> Genero:
        if not _actualizar_en_csv(self.__ruta_csv, self.CAMPOS, entidad):
            raise ValueError(f"No se encontró una entidad con id={entidad.id} para actualizar")
        return entidad

    def eliminar(self, id: int) -> bool:
        return _eliminar_de_csv(self.__ruta_csv, id)


class RepositorioEditorial(IRepositorio[Editorial]):
    """Repositorio de Editorial, persistido en CSV."""

    CAMPOS: List[str] = ["id", "nombre"]

    def __init__(self, ruta_csv: str) -> None:
        """Inicializa el repositorio.

        Args:
            ruta_csv (str): Archivo CSV donde se persisten los registros.
        """
        self.__ruta_csv = ruta_csv

    def crear(self, entidad: Editorial) -> Editorial:
        _crear_en_csv(self.__ruta_csv, self.CAMPOS, entidad)
        return entidad

    def leer_por_id(self, id: int) -> Optional[Editorial]:
        return _leer_por_id_en_csv(self.__ruta_csv, Editorial, id)

    def leer_todos(self) -> List[Editorial]:
        return _leer_todos_en_csv(self.__ruta_csv, Editorial)

    def actualizar(self, entidad: Editorial) -> Editorial:
        if not _actualizar_en_csv(self.__ruta_csv, self.CAMPOS, entidad):
            raise ValueError(f"No se encontró una entidad con id={entidad.id} para actualizar")
        return entidad

    def eliminar(self, id: int) -> bool:
        return _eliminar_de_csv(self.__ruta_csv, id)


class RepositorioMoneda(IRepositorio[Moneda]):
    """Repositorio de Moneda, persistido en CSV."""

    CAMPOS: List[str] = ["id", "codigo"]

    def __init__(self, ruta_csv: str) -> None:
        """Inicializa el repositorio.

        Args:
            ruta_csv (str): Archivo CSV donde se persisten los registros.
        """
        self.__ruta_csv = ruta_csv

    def crear(self, entidad: Moneda) -> Moneda:
        _crear_en_csv(self.__ruta_csv, self.CAMPOS, entidad)
        return entidad

    def leer_por_id(self, id: int) -> Optional[Moneda]:
        return _leer_por_id_en_csv(self.__ruta_csv, Moneda, id)

    def leer_todos(self) -> List[Moneda]:
        return _leer_todos_en_csv(self.__ruta_csv, Moneda)

    def actualizar(self, entidad: Moneda) -> Moneda:
        if not _actualizar_en_csv(self.__ruta_csv, self.CAMPOS, entidad):
            raise ValueError(f"No se encontró una entidad con id={entidad.id} para actualizar")
        return entidad

    def eliminar(self, id: int) -> bool:
        return _eliminar_de_csv(self.__ruta_csv, id)


class RepositorioTipoCotizacion(IRepositorio[TipoCotizacion]):
    """Repositorio de TipoCotizacion, persistido en CSV."""

    CAMPOS: List[str] = ["id", "nombre"]

    def __init__(self, ruta_csv: str) -> None:
        """Inicializa el repositorio.

        Args:
            ruta_csv (str): Archivo CSV donde se persisten los registros.
        """
        self.__ruta_csv = ruta_csv

    def crear(self, entidad: TipoCotizacion) -> TipoCotizacion:
        _crear_en_csv(self.__ruta_csv, self.CAMPOS, entidad)
        return entidad

    def leer_por_id(self, id: int) -> Optional[TipoCotizacion]:
        return _leer_por_id_en_csv(self.__ruta_csv, TipoCotizacion, id)

    def leer_todos(self) -> List[TipoCotizacion]:
        return _leer_todos_en_csv(self.__ruta_csv, TipoCotizacion)

    def actualizar(self, entidad: TipoCotizacion) -> TipoCotizacion:
        if not _actualizar_en_csv(self.__ruta_csv, self.CAMPOS, entidad):
            raise ValueError(f"No se encontró una entidad con id={entidad.id} para actualizar")
        return entidad

    def eliminar(self, id: int) -> bool:
        return _eliminar_de_csv(self.__ruta_csv, id)


class RepositorioLibro(IRepositorio[Libro]):
    """Repositorio de Libro, persistido en CSV."""

    CAMPOS: List[str] = ["id", "isbn", "titulo", "autor", "genero_id", "editorial_id"]

    def __init__(self, ruta_csv: str) -> None:
        """Inicializa el repositorio.

        Args:
            ruta_csv (str): Archivo CSV donde se persisten los registros.
        """
        self.__ruta_csv = ruta_csv

    def crear(self, entidad: Libro) -> Libro:
        _crear_en_csv(self.__ruta_csv, self.CAMPOS, entidad)
        return entidad

    def leer_por_id(self, id: int) -> Optional[Libro]:
        return _leer_por_id_en_csv(self.__ruta_csv, Libro, id)

    def leer_todos(self) -> List[Libro]:
        return _leer_todos_en_csv(self.__ruta_csv, Libro)

    def actualizar(self, entidad: Libro) -> Libro:
        if not _actualizar_en_csv(self.__ruta_csv, self.CAMPOS, entidad):
            raise ValueError(f"No se encontró una entidad con id={entidad.id} para actualizar")
        return entidad

    def eliminar(self, id: int) -> bool:
        return _eliminar_de_csv(self.__ruta_csv, id)


class RepositorioPrecio(IRepositorio[Precio]):
    """Repositorio de Precio, persistido en CSV."""

    CAMPOS: List[str] = ["id", "libro_id", "moneda_id", "monto"]

    def __init__(self, ruta_csv: str) -> None:
        """Inicializa el repositorio.

        Args:
            ruta_csv (str): Archivo CSV donde se persisten los registros.
        """
        self.__ruta_csv = ruta_csv

    def crear(self, entidad: Precio) -> Precio:
        _crear_en_csv(self.__ruta_csv, self.CAMPOS, entidad)
        return entidad

    def leer_por_id(self, id: int) -> Optional[Precio]:
        return _leer_por_id_en_csv(self.__ruta_csv, Precio, id)

    def leer_todos(self) -> List[Precio]:
        return _leer_todos_en_csv(self.__ruta_csv, Precio)

    def actualizar(self, entidad: Precio) -> Precio:
        if not _actualizar_en_csv(self.__ruta_csv, self.CAMPOS, entidad):
            raise ValueError(f"No se encontró una entidad con id={entidad.id} para actualizar")
        return entidad

    def eliminar(self, id: int) -> bool:
        return _eliminar_de_csv(self.__ruta_csv, id)


class RepositorioStock(IRepositorioStock):
    """Repositorio de Stock, indexado por libro_id."""

    CAMPOS: List[str] = ["id", "libro_id", "cantidad"]

    def __init__(self, ruta_csv: str) -> None:
        """Inicializa el repositorio.

        Args:
            ruta_csv (str): Archivo CSV donde se persisten los registros.
        """
        self.__ruta_csv = ruta_csv

    def crear(self, stock: Stock) -> Stock:
        filas = _leer_filas_csv(self.__ruta_csv)
        if any(int(fila["libro_id"]) == stock.libro_id for fila in filas):
            raise ValueError(f"Ya existe stock para libro_id={stock.libro_id}")
        filas.append(stock.to_dict())
        _escribir_filas_csv(self.__ruta_csv, self.CAMPOS, filas)
        return stock

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        for fila in _leer_filas_csv(self.__ruta_csv):
            if int(fila["libro_id"]) == libro_id:
                return Stock.from_dict(fila)
        return None

    def actualizar(self, stock: Stock) -> Stock:
        filas = _leer_filas_csv(self.__ruta_csv)
        for indice, fila in enumerate(filas):
            if int(fila["libro_id"]) == stock.libro_id:
                filas[indice] = stock.to_dict()
                _escribir_filas_csv(self.__ruta_csv, self.CAMPOS, filas)
                return stock
        raise ValueError(f"No se encontro stock para libro_id={stock.libro_id} para actualizar")

    def eliminar(self, libro_id: int) -> bool:
        filas = _leer_filas_csv(self.__ruta_csv)
        restantes = [fila for fila in filas if int(fila["libro_id"]) != libro_id]
        if len(restantes) == len(filas):
            return False
        _escribir_filas_csv(self.__ruta_csv, self.CAMPOS, restantes)
        return True


class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
    """Repositorio de CotizacionDolar, indexado por (tipo_cotizacion_id, fecha)."""

    CAMPOS: List[str] = ["id", "tipo_cotizacion_id", "fecha", "valor"]

    def __init__(self, ruta_csv: str) -> None:
        """Inicializa el repositorio.

        Args:
            ruta_csv (str): Archivo CSV donde se persisten las cotizaciones.
        """
        self.__ruta_csv = ruta_csv

    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        filas = _leer_filas_csv(self.__ruta_csv)
        clave = (cotizacion.tipo_cotizacion_id, cotizacion.fecha.isoformat())
        if any((int(fila["tipo_cotizacion_id"]), fila["fecha"]) == clave for fila in filas):
            raise ValueError(
                f"Ya existe una cotización para tipo_cotizacion_id="
                f"{cotizacion.tipo_cotizacion_id} y fecha={cotizacion.fecha.isoformat()}"
            )
        filas.append(cotizacion.to_dict())
        _escribir_filas_csv(self.__ruta_csv, self.CAMPOS, filas)
        return cotizacion

    def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: date) -> Optional[CotizacionDolar]:
        clave = (tipo_id, fecha.isoformat())
        for fila in _leer_filas_csv(self.__ruta_csv):
            if (int(fila["tipo_cotizacion_id"]), fila["fecha"]) == clave:
                return CotizacionDolar.from_dict(fila)
        return None

    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        filas = [f for f in _leer_filas_csv(self.__ruta_csv) if int(f["tipo_cotizacion_id"]) == tipo_id]
        filas.sort(key=lambda fila: fila["fecha"])
        return [CotizacionDolar.from_dict(fila) for fila in filas]

    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        filas = _leer_filas_csv(self.__ruta_csv)
        clave = (cotizacion.tipo_cotizacion_id, cotizacion.fecha.isoformat())
        for indice, fila in enumerate(filas):
            if (int(fila["tipo_cotizacion_id"]), fila["fecha"]) == clave:
                filas[indice] = cotizacion.to_dict()
                _escribir_filas_csv(self.__ruta_csv, self.CAMPOS, filas)
                return cotizacion
        raise ValueError(
            f"No se encontró una cotización para tipo_cotizacion_id="
            f"{cotizacion.tipo_cotizacion_id} y fecha={cotizacion.fecha.isoformat()} para actualizar"
        )

    def eliminar(self, tipo_id: int, fecha: date) -> bool:
        clave = (tipo_id, fecha.isoformat())
        filas = _leer_filas_csv(self.__ruta_csv)
        restantes = [f for f in filas if (int(f["tipo_cotizacion_id"]), f["fecha"]) != clave]
        if len(restantes) == len(filas):
            return False
        _escribir_filas_csv(self.__ruta_csv, self.CAMPOS, restantes)
        return True