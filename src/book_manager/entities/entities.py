"""Entidades del dominio de Book Manager.

Clases: Genero, Editorial, Moneda, TipoCotizacion, Libro, Precio, Stock y
CotizacionDolar. Todas heredan de EntidadBase y usan atributos privados
con @property.

Las relaciones entre entidades se guardan por ID (genero_id, editorial_id,
libro_id, moneda_id, tipo_cotizacion_id) y se resuelven en repositorios y
servicios. Libro guarda genero_id y editorial_id, Precio
guarda libro_id y moneda_id, Stock guarda libro_id,
CotizacionDolar guarda tipo_cotizacion_id.
"""

import abc
from datetime import date


def _validar_entero_no_negativo(valor: int, nombre_campo: str) -> int:
    """Valida que un valor sea un entero no negativo.

    Args:
        valor (int): Valor a validar.
        nombre_campo (str): Nombre del campo, usado en el mensaje de error.

    Returns:
        int: El valor validado.

    Raises:
        TypeError: Si valor no es un int (o es bool).
        ValueError: Si valor es negativo.
    """
    if not isinstance(valor, int) or isinstance(valor, bool):
        raise TypeError(f"{nombre_campo} debe ser int, recibido {type(valor).__name__}")
    if valor < 0:
        raise ValueError(f"{nombre_campo} debe ser no negativo, recibido {valor}")
    return valor


def _validar_texto_no_vacio(valor: str, nombre_campo: str) -> str:
    """Valida que un valor sea un string no vacío.

    Args:
        valor (str): Valor a validar.
        nombre_campo (str): Nombre del campo, usado en el mensaje de error.

    Returns:
        str: El valor validado, sin espacios al principio ni al final.

    Raises:
        TypeError: Si valor no es un str.
        ValueError: Si valor queda vacío.
    """
    if not isinstance(valor, str):
        raise TypeError(f"{nombre_campo} debe ser str, recibido {type(valor).__name__}")
    valor = valor.strip()
    if not valor:
        raise ValueError(f"{nombre_campo} no puede estar vacío")
    return valor


def _validar_numero_positivo(valor: float, nombre_campo: str) -> float:
    """Valida que un valor sea numérico y mayor a 0.

    Args:
        valor (float): Valor a validar.
        nombre_campo (str): Nombre del campo, usado en el mensaje de error.

    Returns:
        float: El valor validado, convertido a float.

    Raises:
        TypeError: Si valor no es int ni float (o es bool).
        ValueError: Si valor es menor o igual a 0.
    """
    if not isinstance(valor, (int, float)) or isinstance(valor, bool):
        raise TypeError(f"{nombre_campo} debe ser numérico, recibido {type(valor).__name__}")
    if valor <= 0:
        raise ValueError(f"{nombre_campo} debe ser mayor a 0, recibido {valor}")
    return float(valor)


class EntidadBase(abc.ABC):
    """Clase base abstracta para las entidades del sistema.

    Define un id validado y los métodos to_dict/from_dict que usan los
    repositorios para guardar y leer.
    """

    def __init__(self, id: int) -> None:
        """Inicializa la entidad.

        Args:
            id (int): ID de la entidad.
        """
        self.id = id

    @property
    def id(self) -> int:
        """int: ID de la entidad."""
        return self.__id

    @id.setter
    def id(self, valor: int) -> None:
        self.__id = _validar_entero_no_negativo(valor, "id")

    @abc.abstractmethod
    def to_dict(self) -> dict:
        """Devuelve la entidad como diccionario.

        Returns:
            dict: Diccionario con los campos de la entidad.
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, datos: dict) -> "EntidadBase":
        """Crea una entidad a partir de un diccionario.

        Args:
            datos (dict): Diccionario con los campos de la entidad.

        Returns:
            EntidadBase: Una nueva instancia.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"


class Genero(EntidadBase):
    """Categoría literaria a la que pertenece un libro."""

    def __init__(self, id: int, nombre: str) -> None:
        """Inicializa el género.

        Args:
            id (int): ID del género.
            nombre (str): Nombre del género.
        """
        super().__init__(id)
        self.nombre = nombre

    @property
    def nombre(self) -> str:
        """str: Nombre del género."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = _validar_texto_no_vacio(valor, "nombre")

    def to_dict(self) -> dict:
        return {"id": self.id, "nombre": self.nombre}

    @classmethod
    def from_dict(cls, datos: dict) -> "Genero":
        return cls(id=int(datos["id"]), nombre=str(datos["nombre"]))


class Editorial(EntidadBase):
    """Proveedor o distribuidora que provee libros a la librería."""

    def __init__(self, id: int, nombre: str) -> None:
        """Inicializa la editorial.

        Args:
            id (int): ID de la editorial.
            nombre (str): Nombre de la editorial.
        """
        super().__init__(id)
        self.nombre = nombre

    @property
    def nombre(self) -> str:
        """str: Nombre de la editorial."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = _validar_texto_no_vacio(valor, "nombre")

    def to_dict(self) -> dict:
        return {"id": self.id, "nombre": self.nombre}

    @classmethod
    def from_dict(cls, datos: dict) -> "Editorial":
        return cls(id=int(datos["id"]), nombre=str(datos["nombre"]))


class Moneda(EntidadBase):
    """Moneda en la que puede expresarse un precio (ARS, USD, etc.)."""

    def __init__(self, id: int, codigo: str) -> None:
        """Inicializa la moneda.

        Args:
            id (int): ID de la moneda.
            codigo (str): Código de 3 letras (por ejemplo, "ARS").
        """
        super().__init__(id)
        self.codigo = codigo

    @property
    def codigo(self) -> str:
        """str: Código de 3 letras en mayúsculas."""
        return self.__codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        valor = _validar_texto_no_vacio(valor, "codigo").upper()
        if len(valor) != 3 or not valor.isalpha():
            raise ValueError(f"codigo debe tener 3 letras, recibido {valor!r}")
        self.__codigo = valor

    def to_dict(self) -> dict:
        return {"id": self.id, "codigo": self.codigo}

    @classmethod
    def from_dict(cls, datos: dict) -> "Moneda":
        return cls(id=int(datos["id"]), codigo=str(datos["codigo"]))


class TipoCotizacion(EntidadBase):
    """Tipo de cotización del dólar (Oficial, Blue, MEP, etc.)."""

    def __init__(self, id: int, nombre: str) -> None:
        """Inicializa el tipo de cotización.

        Args:
            id (int): ID del tipo de cotización.
            nombre (str): Nombre del tipo (por ejemplo, "Oficial").
        """
        super().__init__(id)
        self.nombre = nombre

    @property
    def nombre(self) -> str:
        """str: Nombre del tipo de cotización."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = _validar_texto_no_vacio(valor, "nombre")

    def to_dict(self) -> dict:
        return {"id": self.id, "nombre": self.nombre}

    @classmethod
    def from_dict(cls, datos: dict) -> "TipoCotizacion":
        return cls(id=int(datos["id"]), nombre=str(datos["nombre"]))


class Libro(EntidadBase):
    """Título del catálogo de la librería.

    Se relaciona con Genero y Editorial por ID.
    """

    def __init__(
        self,
        id: int,
        isbn: str,
        titulo: str,
        autor: str,
        genero_id: int,
        editorial_id: int,
    ) -> None:
        """Inicializa el libro.

        Args:
            id (int): ID del libro.
            isbn (str): ISBN de 10 o 13 dígitos.
            titulo (str): Título del libro.
            autor (str): Autor del libro.
            genero_id (int): ID del género.
            editorial_id (int): ID de la editorial.
        """
        super().__init__(id)
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.genero_id = genero_id
        self.editorial_id = editorial_id

    @property
    def isbn(self) -> str:
        """str: ISBN del libro."""
        return self.__isbn

    @isbn.setter
    def isbn(self, valor: str) -> None:
        valor = _validar_texto_no_vacio(valor, "isbn")
        solo_digitos = valor.replace("-", "").replace(" ", "")
        if len(solo_digitos) not in (10, 13) or not solo_digitos.isdigit():
            raise ValueError(f"isbn debe tener 10 o 13 dígitos, recibido {valor!r}")
        self.__isbn = valor

    @property
    def titulo(self) -> str:
        """str: Título del libro."""
        return self.__titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        self.__titulo = _validar_texto_no_vacio(valor, "titulo")

    @property
    def autor(self) -> str:
        """str: Autor del libro."""
        return self.__autor

    @autor.setter
    def autor(self, valor: str) -> None:
        self.__autor = _validar_texto_no_vacio(valor, "autor")

    @property
    def genero_id(self) -> int:
        """int: ID del género."""
        return self.__genero_id

    @genero_id.setter
    def genero_id(self, valor: int) -> None:
        self.__genero_id = _validar_entero_no_negativo(valor, "genero_id")

    @property
    def editorial_id(self) -> int:
        """int: ID de la editorial."""
        return self.__editorial_id

    @editorial_id.setter
    def editorial_id(self, valor: int) -> None:
        self.__editorial_id = _validar_entero_no_negativo(valor, "editorial_id")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "isbn": self.isbn,
            "titulo": self.titulo,
            "autor": self.autor,
            "genero_id": self.genero_id,
            "editorial_id": self.editorial_id,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Libro":
        return cls(
            id=int(datos["id"]),
            isbn=str(datos["isbn"]),
            titulo=str(datos["titulo"]),
            autor=str(datos["autor"]),
            genero_id=int(datos["genero_id"]),
            editorial_id=int(datos["editorial_id"]),
        )


class Precio(EntidadBase):
    """Valor monetario asociado a un libro en una moneda determinada."""

    def __init__(self, id: int, libro_id: int, moneda_id: int, monto: float) -> None:
        """Inicializa el precio.

        Args:
            id (int): ID del precio.
            libro_id (int): ID del libro.
            moneda_id (int): ID de la moneda.
            monto (float): Valor del precio.
        """
        super().__init__(id)
        self.libro_id = libro_id
        self.moneda_id = moneda_id
        self.monto = monto

    @property
    def libro_id(self) -> int:
        """int: ID del libro."""
        return self.__libro_id

    @libro_id.setter
    def libro_id(self, valor: int) -> None:
        self.__libro_id = _validar_entero_no_negativo(valor, "libro_id")

    @property
    def moneda_id(self) -> int:
        """int: ID de la moneda."""
        return self.__moneda_id

    @moneda_id.setter
    def moneda_id(self, valor: int) -> None:
        self.__moneda_id = _validar_entero_no_negativo(valor, "moneda_id")

    @property
    def monto(self) -> float:
        """float: Valor del precio."""
        return self.__monto

    @monto.setter
    def monto(self, valor: float) -> None:
        self.__monto = _validar_numero_positivo(valor, "monto")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "libro_id": self.libro_id,
            "moneda_id": self.moneda_id,
            "monto": self.monto,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Precio":
        return cls(
            id=int(datos["id"]),
            libro_id=int(datos["libro_id"]),
            moneda_id=int(datos["moneda_id"]),
            monto=float(datos["monto"]),
        )


class Stock(EntidadBase):
    """Cantidad disponible de un libro determinado."""

    def __init__(self, id: int, libro_id: int, cantidad: int) -> None:
        """Inicializa el registro de stock.

        Args:
            id (int): ID del registro.
            libro_id (int): ID del libro.
            cantidad (int): Cantidad de ejemplares.
        """
        super().__init__(id)
        self.libro_id = libro_id
        self.cantidad = cantidad

    @property
    def libro_id(self) -> int:
        """int: ID del libro."""
        return self.__libro_id

    @libro_id.setter
    def libro_id(self, valor: int) -> None:
        self.__libro_id = _validar_entero_no_negativo(valor, "libro_id")

    @property
    def cantidad(self) -> int:
        """int: Cantidad de ejemplares disponibles."""
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        self.__cantidad = _validar_entero_no_negativo(valor, "cantidad")

    def to_dict(self) -> dict:
        return {"id": self.id, "libro_id": self.libro_id, "cantidad": self.cantidad}

    @classmethod
    def from_dict(cls, datos: dict) -> "Stock":
        return cls(
            id=int(datos["id"]),
            libro_id=int(datos["libro_id"]),
            cantidad=int(datos["cantidad"]),
        )


class CotizacionDolar(EntidadBase):
    """Registro histórico de la cotización del dólar por tipo y fecha."""

    def __init__(self, id: int, tipo_cotizacion_id: int, fecha: date, valor: float) -> None:
        """Inicializa la cotización.

        Args:
            id (int): ID del registro.
            tipo_cotizacion_id (int): ID del tipo de cotización.
            fecha (date): Fecha de la cotización.
            valor (float): Valor de la cotización.
        """
        super().__init__(id)
        self.tipo_cotizacion_id = tipo_cotizacion_id
        self.fecha = fecha
        self.valor = valor

    @property
    def tipo_cotizacion_id(self) -> int:
        """int: ID del tipo de cotización."""
        return self.__tipo_cotizacion_id

    @tipo_cotizacion_id.setter
    def tipo_cotizacion_id(self, valor: int) -> None:
        self.__tipo_cotizacion_id = _validar_entero_no_negativo(valor, "tipo_cotizacion_id")

    @property
    def fecha(self) -> date:
        """date: Fecha de la cotización."""
        return self.__fecha

    @fecha.setter
    def fecha(self, valor: date) -> None:
        if not isinstance(valor, date):
            raise TypeError(f"fecha debe ser date, recibido {type(valor).__name__}")
        if valor > date.today():
            raise ValueError(f"fecha no puede ser futura, recibido {valor}")
        self.__fecha = valor

    @property
    def valor(self) -> float:
        """float: Valor de la cotización."""
        return self.__valor

    @valor.setter
    def valor(self, valor: float) -> None:
        self.__valor = _validar_numero_positivo(valor, "valor")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "tipo_cotizacion_id": self.tipo_cotizacion_id,
            "fecha": self.fecha.isoformat(),
            "valor": self.valor,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "CotizacionDolar":
        return cls(
            id=int(datos["id"]),
            tipo_cotizacion_id=int(datos["tipo_cotizacion_id"]),
            fecha=date.fromisoformat(str(datos["fecha"])),
            valor=float(datos["valor"]),
        )