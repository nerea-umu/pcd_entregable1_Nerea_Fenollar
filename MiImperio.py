from enum import Enum
from abc import ABC, abstractmethod

class ErrorImperio(Exception):
    """Clase base para excepciones del sistema."""
    pass

class PiezaNoEncontradaError(ErrorImperio):
    """Se lanza cuando una pieza no existe en el catálogo."""
    pass

class StockInsuficienteError(ErrorImperio):
    """Se lanza cuando no hay suficientes unidades de un repuesto."""
    pass

class ClaveIncorrectaError(ErrorImperio):
    """Se lanza cuando la clave cifrada de la nave no coincide."""
    pass




class Clase(Enum):
    EJECUTOR = 1
    ECLIPSE = 2
    SOBERANO = 3


class Ubicacion(Enum):
    ENDOR = 1
    CUMULO_RAIMOS = 2
    NEBULOSA_KALIIDA = 3


class Propiedades(ABC):
    def __init__(self, tripulacion : int, pasaje : int):
        self.tripulacion = tripulacion
        self.pasaje = pasaje
     

class Unidad_Combate(ABC):
    def __init__(self, id_combate : str, clave_cif : int):
        self.id_combate = id_combate
        self.clave_cif = clave_cif

    def validar_clave(self, clave_cif):
        if self.clave_cif != clave_cif:
            raise ClaveIncorrectaError('La clave cifrada proporcionada no coincide con la clave de la nave.')


class Nave(Unidad_Combate):
    def __init__(self, nombre : str, piezas : list, id_combate : str, clave_cif : int):
        super().__init__(id_combate, clave_cif)
        self.nombre = nombre
        self.piezas = piezas

    def __str__(self):
        return f'Nave: {self.nombre} \nPiezas: {len(self.piezas)} \nID Combate: {self.id_combate} \nClave CIF: {self.clave_cif}'
    
    def solicitar_repuesto(self, almacen, nombre_repuesto, clave_cif):
        self.validar_clave(clave_cif)
        repuesto = almacen.eliminar_repuesto(nombre_repuesto, 1)
        self.piezas.append(repuesto)
    
    def ver_piezas(self):
        print(f'Piezas de la nave {self.nombre}:')
        for pieza in self.piezas:
            print(pieza)


class Estacion_espacial(Propiedades, Nave):
    def __init__(self, nombre : str, piezas : list, id_combate : str, clave_cif : int, tripulacion : int, pasaje : int, ubicacion : Ubicacion):
        Propiedades.__init__(self, tripulacion, pasaje)
        Nave.__init__(self, nombre, piezas, id_combate, clave_cif)
        self.ubicacion = ubicacion

    def __str__(self):
        return f'Estacion Espacial: {self.nombre} \nPiezas: {len(self.piezas)} \nTripulación: {self.tripulacion} \nPasaje: {self.pasaje} \nUbicación: {self.ubicacion.name}'
    
    def get_ubicacion(self):
        return self.ubicacion
    
    def set_ubicacion(self, ubicacion : Ubicacion):
        self.ubicacion = ubicacion
    
    def get_capacidad(self):
        return self.tripulacion + self.pasaje


class Nave_estelar(Propiedades, Nave):
    def __init__(self, nombre : str, piezas : list, id_combate : str, clave_cif : int, tripulacion : int, pasaje : int, clase : Clase):
        Propiedades.__init__(self, tripulacion, pasaje)
        Nave.__init__(self, nombre, piezas, id_combate, clave_cif)
        self.clase = clase
    
    def __str__(self):
        return f'Nave Estelar: {self.nombre} \nPiezas: {len(self.piezas)} \nTripulación: {self.tripulacion} \nPasaje: {self.pasaje} \nClase: {self.clase.name}'
    
    def get_clase(self):
        return self.clase
    
    def set_clase(self, clase : Clase):
        self.clase = clase

    def get_capacidad(self):
        return self.tripulacion + self.pasaje


class Caza(Nave):
    def __init__(self, nombre : str, piezas : list, id_combate : str, clave_cif : int, dotacion : int):
        Nave.__init__(self, nombre, piezas, id_combate, clave_cif)
        self.dotacion = dotacion
    
    def __str__(self):
        return f'Caza: {self.nombre} \nPiezas: {len(self.piezas)} \nDotación: {self.dotacion}'
    
    def get_dotacion(self):
        return self.dotacion
    
    def set_dotacion(self, dotacion : int):
        self.dotacion = dotacion


class Repuesto():
    def __init__(self, nombre : str, cantidad : int, proveedor : str, precio : float):
        self.nombre = nombre
        self.__cantidad = cantidad
        self.proveedor = proveedor
        self.precio = precio

    def __str__(self):
        return f'Repuesto: {self.nombre} \nCantidad: {self.__cantidad} \nProveedor: {self.proveedor} \nPrecio: ${self.precio:.2f}'
    
    def actualiza_stock(self, unidades : int):
        if self.__cantidad + unidades < 0:
            raise StockInsuficienteError(f'No se puede reducir el stock del repuesto "{self.nombre}". Stock actual: {self.__cantidad}')
        self.__cantidad += unidades
    
    def get_cantidad(self):
        return self.__cantidad
    
    def get_proveedor(self):
        return self.proveedor
    
    def set_proveedor(self, proveedor : str):
        self.proveedor = proveedor

    def get_precio(self):
        return self.precio
    
    def set_precio(self, precio : float):
        self.precio = precio


class Almacen():
    def __init__(self, nombre : str, ubicacion : str):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.catalogo = {}
    
    def __str__(self):
        return f'Almacén: {self.nombre} \nUbicación: {self.ubicacion} \nCatálogo: {len(self.catalogo)} repuestos'
    
    def agregar_repuesto(self, repuesto : Repuesto):
        if repuesto in self.catalogo.keys():
            self.catalogo[repuesto] += repuesto.get_cantidad()
        self.catalogo[repuesto] = repuesto.get_cantidad()
    
    def eliminar_repuesto(self, nombre_pieza : str, cantidad : int):
        repuesto = self.buscar_repuesto(nombre_pieza)
        if not repuesto:
            raise PiezaNoEncontradaError(f'El repuesto "{nombre_pieza}" no se encuentra en el catálogo.')
        if repuesto.get_cantidad() < cantidad:
            raise StockInsuficienteError(f'No hay suficiente stock del repuesto "{nombre_pieza}". Cantidad disponible: {repuesto.get_cantidad()}')
        repuesto.set_cantidad(repuesto.get_cantidad() - cantidad)
        if repuesto.get_cantidad() == 0:
            del self.catalogo[repuesto]

        repuesto.actualiza_stock(-cantidad)
        return repuesto
    
    def listar_repuestos(self):
        print(f'Catálogo de repuestos de {self.nombre}:')
        for r in self.catalogo:
            print(r)
    
    def buscar_repuesto(self, nombre : str):
        for repuesto in self.catalogo:
            if repuesto.nombre == nombre:
                return repuesto
        return None
    

class MiImperio():
    def __init__(self, nombre : str):
        self.nombre = nombre
        self.naves = []
        self.almacenes = []
        self.repuestos = []
    
    def __str__(self):
        return f'Mi Imperio: {self.nombre} \nNaves: {len(self.naves)} \nAlmacenes: {len(self.almacenes)} \nRepuestos: {len(self.repuestos)}'
    
    def agregar_nave(self, nave : Nave):
        self.naves.append(nave)
    
    def eliminar_nave(self, nave : Nave):
        self.naves.remove(nave)
    
    def get_nave(self, nombre : str):
        for nave in self.naves:
            if nave.nombre == nombre:
                return nave
        return None
    
    def listar_naves(self):
        print(f'Naves del Imperio {self.nombre}:')
        for nave in self.naves:
            print(nave)
    
    def agregar_almacen(self, almacen : Almacen):
        self.almacenes.append(almacen)
    
    def eliminar_almacen(self, almacen : Almacen):
        self.almacenes.remove(almacen)
    
    def get_almacen(self, nombre : str):
        for almacen in self.almacenes:
            if almacen.nombre == nombre:
                return almacen
        return None
    
    def listar_almacenes(self):
        print(f'Almacenes del Imperio {self.nombre}:')
        for almacen in self.almacenes:
            print(almacen)
    
    def comprar_repuesto(self, repuesto : Repuesto):
        self.repuestos.append(repuesto)
    
    def vender_repuesto(self, repuesto : Repuesto):
        self.repuestos.remove(repuesto)
    
    def listar_repuestos(self):
        print(f'Repuestos del Imperio {self.nombre}:')
        for repuesto in self.repuestos:
            print(repuesto)
    
    def buscar_repuesto(self, nombre : str):
        for repuesto in self.repuestos:
            if repuesto.nombre == nombre:
                return repuesto
        return None




if __name__ == "__main__":
    try:
        # 1. Creamos un almacén con algo de stock
        almacen1 = Almacen("Depósito Imperial", "Cerca de la Estrella de la Muerte")
        motor = Repuesto("Motor T-14", 2, "Chatarrerías Watto", 1500.0)
        almacen1.agregar_repuesto(motor)

        # 2. Creamos un Caza (Recuerda ajustar el constructor según tu Nave)
        caza1 = Caza("CAZA Advanced", [], 'C-001', 5578, 1)
        # Nota: asegúrate de que Caza pase el ID y Clave a Nave
                
        # 3. Intentamos pedir un repuesto con CLAVE INCORRECTA
        print(almacen1)
        almacen1.listar_repuestos()
        # Suponiendo que la clave es 1234
        caza1.solicitar_repuesto(almacen1, "Motor T-14", 5578)

        # 4. Intentamos pedir un repuesto con CLAVE CORRECTA
        # Suponiendo que la clave es 1500
        caza1.solicitar_repuesto(almacen1, "Motor T-14", 5578)
        print(caza1)
        almacen1.listar_repuestos()
        

    except ErrorImperio as e:
        print(f"Error en la operación: {e}")