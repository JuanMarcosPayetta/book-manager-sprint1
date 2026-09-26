"""Consola interactiva de Book Manager.

Cada opción del menú llama a un servicio, nunca a un repositorio
directamente. Los submenús se ajustan a lo que permite cada repositorio.
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


def _leer_entero(mensaje: str) -> int:
    """Pide un entero por consola hasta que el usuario ingrese uno válido.

    Args:
        mensaje (str): Texto a mostrar.

    Returns:
        int: El entero ingresado.
    """
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Ingresá un número entero válido.")


def _leer_flotante(mensaje: str) -> float:
    """Pide un flotante por consola hasta que el usuario ingrese uno válido.

    Args:
        mensaje (str): Texto a mostrar.

    Returns:
        float: El flotante ingresado.
    """
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Ingresá un número válido.")


def _leer_fecha(mensaje: str) -> date:
    """Pide una fecha (AAAA-MM-DD) por consola hasta que sea válida.

    Args:
        mensaje (str): Texto a mostrar.

    Returns:
        date: La fecha ingresada.
    """
    while True:
        try:
            return date.fromisoformat(input(mensaje))
        except ValueError:
            print("Ingresá una fecha con formato AAAA-MM-DD.")


def _menu_genero(servicio) -> None:
    """Submenú de Genero.

    Args:
        servicio: Servicio de géneros.
    """
    while True:
        print("\n--- Géneros ---")
        print("1) Listar  2) Crear  3) Leer por id  4) Actualizar  5) Eliminar  0) Volver")
        opcion = input("Opción: ")
        try:
            if opcion == "1":
                for genero in servicio.leer_todos():
                    print(genero)
            elif opcion == "2":
                servicio.crear(Genero(id=_leer_entero("ID: "), nombre=input("Nombre: ")))
                print("Creado.")
            elif opcion == "3":
                print(servicio.leer_por_id(_leer_entero("ID: ")) or "No encontrado.")
            elif opcion == "4":
                id_actualizar = _leer_entero("ID a actualizar: ")
                servicio.actualizar(Genero(id=id_actualizar, nombre=input("Nuevo nombre: ")))
                print("Actualizado.")
            elif opcion == "5":
                encontrado = servicio.eliminar(_leer_entero("ID a eliminar: "))
                print("Eliminado." if encontrado else "No encontrado.")
            elif opcion == "0":
                return
            else:
                print("Opción inválida.")
        except ValueError as error:
            print(f"Error: {error}")


def _menu_editorial(servicio) -> None:
    """Submenú de Editorial.

    Args:
        servicio: Servicio de editoriales.
    """
    while True:
        print("\n--- Editoriales ---")
        print("1) Listar  2) Crear  0) Volver")
        opcion = input("Opción: ")
        try:
            if opcion == "1":
                for editorial in servicio.leer_todos():
                    print(editorial)
            elif opcion == "2":
                servicio.crear(Editorial(id=_leer_entero("ID: "), nombre=input("Nombre: ")))
                print("Creado.")
            elif opcion == "0":
                return
            else:
                print("Opción inválida.")
        except ValueError as error:
            print(f"Error: {error}")


def _menu_moneda(servicio) -> None:
    """Submenú de Moneda.

    Args:
        servicio: Servicio de monedas.
    """
    while True:
        print("\n--- Monedas ---")
        print("1) Listar  2) Crear  0) Volver")
        opcion = input("Opción: ")
        try:
            if opcion == "1":
                for moneda in servicio.leer_todos():
                    print(moneda)
            elif opcion == "2":
                servicio.crear(Moneda(id=_leer_entero("ID: "), codigo=input("Código (3 letras): ")))
                print("Creado.")
            elif opcion == "0":
                return
            else:
                print("Opción inválida.")
        except ValueError as error:
            print(f"Error: {error}")


def _menu_tipo_cotizacion(servicio) -> None:
    """Submenú de TipoCotizacion.

    Args:
        servicio: Servicio de tipos de cotización.
    """
    while True:
        print("\n--- Tipos de cotización ---")
        print("1) Listar  2) Crear  0) Volver")
        opcion = input("Opción: ")
        try:
            if opcion == "1":
                for tipo in servicio.leer_todos():
                    print(tipo)
            elif opcion == "2":
                servicio.crear(TipoCotizacion(id=_leer_entero("ID: "), nombre=input("Nombre: ")))
                print("Creado.")
            elif opcion == "0":
                return
            else:
                print("Opción inválida.")
        except ValueError as error:
            print(f"Error: {error}")


def _menu_libro(servicio) -> None:
    """Submenú de Libro.

    Args:
        servicio: Servicio de libros.
    """
    while True:
        print("\n--- Libros ---")
        print("1) Listar  2) Crear  3) Leer por id  4) Actualizar  5) Eliminar  0) Volver")
        opcion = input("Opción: ")
        try:
            if opcion == "1":
                for libro in servicio.leer_todos():
                    print(libro)
            elif opcion == "2":
                servicio.crear(Libro(
                    id=_leer_entero("ID: "),
                    isbn=input("ISBN: "),
                    titulo=input("Título: "),
                    autor=input("Autor: "),
                    genero_id=_leer_entero("ID de género: "),
                    editorial_id=_leer_entero("ID de editorial: "),
                ))
                print("Creado.")
            elif opcion == "3":
                print(servicio.leer_por_id(_leer_entero("ID: ")) or "No encontrado.")
            elif opcion == "4":
                servicio.actualizar(Libro(
                    id=_leer_entero("ID a actualizar: "),
                    isbn=input("ISBN: "),
                    titulo=input("Título: "),
                    autor=input("Autor: "),
                    genero_id=_leer_entero("ID de género: "),
                    editorial_id=_leer_entero("ID de editorial: "),
                ))
                print("Actualizado.")
            elif opcion == "5":
                encontrado = servicio.eliminar(_leer_entero("ID a eliminar: "))
                print("Eliminado." if encontrado else "No encontrado.")
            elif opcion == "0":
                return
            else:
                print("Opción inválida.")
        except ValueError as error:
            print(f"Error: {error}")


def _menu_precio(servicio) -> None:
    """Submenú de Precio.

    Args:
        servicio: Servicio de precios.
    """
    while True:
        print("\n--- Precios ---")
        print("1) Listar  2) Crear  0) Volver")
        opcion = input("Opción: ")
        try:
            if opcion == "1":
                for precio in servicio.leer_todos():
                    print(precio)
            elif opcion == "2":
                servicio.crear(Precio(
                    id=_leer_entero("ID: "),
                    libro_id=_leer_entero("ID de libro: "),
                    moneda_id=_leer_entero("ID de moneda: "),
                    monto=_leer_flotante("Monto: "),
                ))
                print("Creado.")
            elif opcion == "0":
                return
            else:
                print("Opción inválida.")
        except ValueError as error:
            print(f"Error: {error}")


def _menu_stock(servicio) -> None:
    """Submenú de Stock (clave: libro_id).

    Args:
        servicio: Servicio de stock.
    """
    while True:
        print("\n--- Stock ---")
        print("1) Crear  2) Leer por libro_id  3) Actualizar  4) Eliminar  0) Volver")
        opcion = input("Opción: ")
        try:
            if opcion == "1":
                servicio.crear(Stock(
                    id=_leer_entero("ID: "),
                    libro_id=_leer_entero("ID de libro: "),
                    cantidad=_leer_entero("Cantidad: "),
                ))
                print("Creado.")
            elif opcion == "2":
                print(servicio.leer_por_libro(_leer_entero("ID de libro: ")) or "No encontrado.")
            elif opcion == "3":
                servicio.actualizar(Stock(
                    id=_leer_entero("ID: "),
                    libro_id=_leer_entero("ID de libro: "),
                    cantidad=_leer_entero("Cantidad: "),
                ))
                print("Actualizado.")
            elif opcion == "4":
                encontrado = servicio.eliminar(_leer_entero("ID de libro: "))
                print("Eliminado." if encontrado else "No encontrado.")
            elif opcion == "0":
                return
            else:
                print("Opción inválida.")
        except ValueError as error:
            print(f"Error: {error}")


def _menu_cotizacion(servicio) -> None:
    """Submenú de CotizacionDolar (clave: tipo_cotizacion_id + fecha).

    Args:
        servicio: Servicio de cotizaciones.
    """
    while True:
        print("\n--- Cotizaciones del dólar ---")
        print("1) Histórico por tipo  2) Crear  3) Leer por tipo y fecha  "
              "4) Actualizar  5) Eliminar  0) Volver")
        opcion = input("Opción: ")
        try:
            if opcion == "1":
                for cotizacion in servicio.leer_historico_por_tipo(_leer_entero("ID de tipo de cotización: ")):
                    print(cotizacion)
            elif opcion == "2":
                servicio.crear(CotizacionDolar(
                    id=_leer_entero("ID: "),
                    tipo_cotizacion_id=_leer_entero("ID de tipo de cotización: "),
                    fecha=_leer_fecha("Fecha (AAAA-MM-DD): "),
                    valor=_leer_flotante("Valor: "),
                ))
                print("Creada.")
            elif opcion == "3":
                tipo_id = _leer_entero("ID de tipo de cotización: ")
                fecha = _leer_fecha("Fecha (AAAA-MM-DD): ")
                print(servicio.leer_por_tipo_y_fecha(tipo_id, fecha) or "No encontrada.")
            elif opcion == "4":
                servicio.actualizar(CotizacionDolar(
                    id=_leer_entero("ID: "),
                    tipo_cotizacion_id=_leer_entero("ID de tipo de cotización: "),
                    fecha=_leer_fecha("Fecha (AAAA-MM-DD): "),
                    valor=_leer_flotante("Nuevo valor: "),
                ))
                print("Actualizada.")
            elif opcion == "5":
                tipo_id = _leer_entero("ID de tipo de cotización: ")
                fecha = _leer_fecha("Fecha (AAAA-MM-DD): ")
                print("Eliminada." if servicio.eliminar(tipo_id, fecha) else "No encontrada.")
            elif opcion == "0":
                return
            else:
                print("Opción inválida.")
        except ValueError as error:
            print(f"Error: {error}")


def iniciar_consola(
    servicio_genero,
    servicio_editorial,
    servicio_moneda,
    servicio_tipo_cotizacion,
    servicio_libro,
    servicio_precio,
    servicio_stock,
    servicio_cotizacion,
) -> None:
    """Muestra el menú principal y despacha al submenú de cada entidad.

    Args:
        servicio_genero: Servicio de géneros.
        servicio_editorial: Servicio de editoriales.
        servicio_moneda: Servicio de monedas.
        servicio_tipo_cotizacion: Servicio de tipos de cotización.
        servicio_libro: Servicio de libros.
        servicio_precio: Servicio de precios.
        servicio_stock: Servicio de stock.
        servicio_cotizacion: Servicio de cotizaciones del dólar.
    """
    while True:
        print("\n=== Book Manager ===")
        print("1) Géneros")
        print("2) Editoriales")
        print("3) Monedas")
        print("4) Tipos de cotización")
        print("5) Libros")
        print("6) Precios")
        print("7) Stock")
        print("8) Cotizaciones del dólar")
        print("0) Salir")
        opcion = input("Opción: ")

        if opcion == "1":
            _menu_genero(servicio_genero)
        elif opcion == "2":
            _menu_editorial(servicio_editorial)
        elif opcion == "3":
            _menu_moneda(servicio_moneda)
        elif opcion == "4":
            _menu_tipo_cotizacion(servicio_tipo_cotizacion)
        elif opcion == "5":
            _menu_libro(servicio_libro)
        elif opcion == "6":
            _menu_precio(servicio_precio)
        elif opcion == "7":
            _menu_stock(servicio_stock)
        elif opcion == "8":
            _menu_cotizacion(servicio_cotizacion)
        elif opcion == "0":
            print("¡Hasta luego!")
            return
        else:
            print("Opción inválida.")