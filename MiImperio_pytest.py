import pytest
from enum import Enum
from abc import ABCMeta, abstractmethod

class Clase(Enum):
    EJECUTOR = 1
    ECLIPSE = 2
    SOBERANO = 3


class Ubicacion(Enum):
    ENDOR = 1
    CUMULO_RAIMOS = 2
    NEBULOSA_KALIIDA = 3


class Propiedades(ABCMeta):
    def __init__(self, tripulacion : int, pasaje : int):
        self.tripulacion = tripulacion
        self.pasaje = pasaje
    
    @abstractmethod
    def calcular_coste_mantenimiento(self) -> float:
        pass


class Unidad_Combate(ABCMeta):
    def __init__(self, id_combate : str, clave_cif : int):
        self.id_combate = id_combate
        self.clave_cif = clave_cif
    
    @abstractmethod
    def calcular_coste_mantenimiento(self) -> float:
        pass
   
    """
    Posibles métodos:
    - get_id_combate()
    - get_clave_cif()
    - set_id_combate()
    - set_clave_cif()
    - __str__()
    """


class Nave(Unidad_Combate):
    def __init__(self, nombre : str, piezas : list, id_combate : str, clave_cif : int):
        super().__init__(id_combate, clave_cif)
        self.nombre = nombre
        self.piezas = piezas

    """
    Posibles métodos:
    - agregar_pieza()
    - eliminar_pieza()
    - mostrar_catalogo()
    - __str__()
    """


class Estacion_espacial(Propiedades, Nave):
    def __init__(self, nombre : str, piezas : list, tripulacion : int, pasaje : int, ubicacion : Ubicacion):
        Propiedades.__init__(self, tripulacion, pasaje)
        Nave.__init__(self, nombre, piezas)
        self.ubicacion = ubicacion
    
    """
    Posibles métodos:
    - get_ubicacion()
    - set_ubicacion()
    - capacidad_total() -- suma tripulacion + pasaje
    - __str__()
    """


class Nave_estelar(Propiedades, Nave):
    def __init__(self, nombre : str, piezas : list, tripulacion : int, pasaje : int, clase : Clase):
        Propiedades.__init__(self, tripulacion, pasaje)
        Nave.__init__(self, nombre, piezas)
        self.clase = clase
    
    """
    Posibles métodos:
    - get_clase()
    - set_clase()
    - capacidad_total() -- suma tripulacion + pasaje
    - __str__()
    """


class Caza(Nave):
    def __init__(self, nombre : str, piezas : list, dotacion : int):
        Nave.__init__(self, nombre, piezas)
        self.dotacion = dotacion
    
    """
    Posibles métodos:
    - get_dotacion()
    - set_dotacion()
    - __str__()
    """


class Repuesto():
    def __init__(self, nombre : str, cantidad : int, proveedor : str, precio : float):
        self.nombre = nombre
        self._cantidad = cantidad
        self.proveedor = proveedor
        self.precio = precio

    """
    Posibles métodos:
    - get_cantidad()
    - aumentar_stock(cantidad : int)
    - reducir_stock(cantidad : int)
    - get_proveedor()
    - set_proveedor()
    - get_precio()
    - set_precio()
    - __str__()
    """

class Almacen():
    def __init__(self, nombre : str, ubicacion : str, catalogo : list):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.catalogo = catalogo

    """
    Posibles métodos:
    - agregar_repuesto(repuesto : Repuesto)
    - eliminar_repuesto(nombre : str)
    - mostrar_catalogo()
    - buscar_repuesto(nombre : str)
    - actualizar_stock(nombre : str, cantidad : int)
    - __str__()
    """


class MiImperio():
    def __init__(self, nombre : str):
        self.nombre = nombre
        self.naves = []
        self.almacenes = []
        self.repuestos = []

    """
    Posibles métodos:
    - agregar_nave()
    - eliminar_nave()
    - listar_naves()
    
    - agregar_almacen()
    - eliminar_almacen()
    - listar_almacenes()
    
    - comprar_repuesto()
    - vender_repuesto()
    - listar_repuestos()
    - __str__()
    """
