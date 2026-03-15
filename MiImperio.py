from enum import Enum
from abc import ABC, abstractmethod

class ErrorImperio(Exception):
    """Clase base para excepciones del sistema."""
    pass

class PiezaNoEncontradaError(ErrorImperio):
    """Se lanza cuando una pieza no existe en el catálogo."""
    pass

class PiezaYaIncluida(ErrorImperio):
    """Se lanza cuando una pieza ya existe en el catálogo."""
    pass

class StockInsuficienteError(ErrorImperio):
    """Se lanza cuando no hay suficientes unidades de un repuesto."""
    pass

class ClaveIncorrectaError(ErrorImperio):
    """Se lanza cuando la clave cifrada de la nave no coincide."""
    pass

class ObjetoErroneo(ErrorImperio):
    """Se lanza cuando un objeto proporcionado no es válido para el método."""
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

    def __str__(self):
        return f'UNIDAD DE COMBARE: \nID Combate: {self.id_combate} \nClave CIF: {self.clave_cif}'

    def validar_clave(self, clave_cif):
        if self.clave_cif != clave_cif:
            raise ClaveIncorrectaError('La clave cifrada proporcionada no coincide con la clave de la nave.')


class Nave(Unidad_Combate):
    def __init__(self, nombre : str, piezas : list, id_combate : str, clave_cif : int):
        super().__init__(id_combate, clave_cif)
        self.nombre = nombre
        self.piezas = piezas if piezas else []

    def __str__(self):
        return super().__str__() + f'Nave: {self.nombre} \nPiezas: {len(self.piezas)} \nID Combate: {self.id_combate} \nClave CIF: {self.clave_cif}'
    
    def solicitar_repuesto(self, almacen, repuesto, clave_cif):
        if repuesto in self.piezas:
            raise PiezaYaIncluida(f'La nave ya tiene el repuesto "{repuesto.nombre}".')
        if not isinstance(repuesto, Repuesto):
            raise ObjetoErroneo('El objeto proporcionado no es un repuesto válido. Debe ser una instancia de la clase Repuesto.')
        self.validar_clave(clave_cif)
        almacen.eliminar_repuesto(repuesto.nombre, 1)
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


class Repuesto:
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


class Almacen:
    def __init__(self, nombre : str, ubicacion : str):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.catalogo = {}
    
    def __str__(self):
        return f'Almacén: {self.nombre} \nUbicación: {self.ubicacion} \nCatálogo: {len(self.catalogo)} repuestos'
    
    def ver_catalogo(self):
        print(f'Catálogo del almacén {self.nombre}:')
        for repuesto, cantidad in self.catalogo.items():
            print(f'-{repuesto} | Cantidad: {cantidad}')
    
    def agregar_repuesto(self, repuesto : Repuesto):
        if not isinstance(repuesto, Repuesto):
            raise ObjetoErroneo('El objeto proporcionado no es un repuesto válido. Debe ser una instancia de la clase Repuesto.')
        if repuesto in self.catalogo.keys():
            self.catalogo[repuesto] += repuesto.get_cantidad()
        else:
            self.catalogo[repuesto] = repuesto.get_cantidad()
    
    def eliminar_repuesto(self, nombre_pieza : str, cantidad : int):
        repuesto = self.buscar_repuesto(nombre_pieza)
        if repuesto not in self.catalogo.keys(): 
            raise PiezaNoEncontradaError(f'El repuesto "{nombre_pieza}" no se encuentra en el catálogo.')
        repuesto.actualiza_stock(-cantidad)
        if repuesto.get_cantidad() == 0:
            del self.catalogo[repuesto]
        else:
            self.catalogo[repuesto] = repuesto.get_cantidad()
        return repuesto
    
    def listar_repuestos(self):
        print(f'Catálogo de repuestos de {self.nombre}:')
        for r in self.catalogo:
            print(r)
    
    def buscar_repuesto(self, nombre : str):
        for repuesto in self.catalogo.keys():
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
        if not isinstance(nave, Nave):
            raise ObjetoErroneo('El objeto proporcionado no es una nave válida. Debe ser una instancia de la clase Nave.')
        self.naves.append(nave)
    
    def eliminar_nave(self, nave : Nave):
        if not isinstance(nave, Nave):
            raise ObjetoErroneo('El objeto proporcionado no es una nave válida. Debe ser una instancia de la clase Nave.')
        self.naves.remove(nave)
    
    def get_nave(self, nombre : str):
        for nave in self.naves:
            if nave.nombre == nombre:
                return nave
        return None
    
    def listar_naves(self):
        print(f'Naves del Imperio {self.nombre}:')
        for nave in self.naves:
            print(f'-{nave}')
        print()
    
    def agregar_almacen(self, almacen : Almacen):
        if not isinstance(almacen, Almacen):
            raise ObjetoErroneo('El objeto proporcionado no es un almacén válido. Debe ser una instancia de la clase Almacen.')
        self.almacenes.append(almacen)
    
    def eliminar_almacen(self, almacen : Almacen):
        if not isinstance(almacen, Almacen):
            raise ObjetoErroneo('El objeto proporcionado no es un almacén válido. Debe ser una instancia de la clase Almacen.')
        self.almacenes.remove(almacen)
    
    def get_almacen(self, nombre : str):
        for almacen in self.almacenes:
            if almacen.nombre == nombre:
                return almacen
        return None
    
    def listar_almacenes(self):
        print(f'Almacenes del Imperio {self.nombre}:')
        for almacen in self.almacenes:
            print(f'-{almacen}')
        print()
    
    def comprar_repuesto(self, repuesto : Repuesto):
        if not isinstance(repuesto, Repuesto):
            raise ObjetoErroneo('El objeto proporcionado no es un repuesto válido. Debe ser una instancia de la clase Repuesto.')
        self.repuestos.append(repuesto)
    
    def vender_repuesto(self, repuesto : Repuesto):
        if not isinstance(repuesto, Repuesto):
            raise ObjetoErroneo('El objeto proporcionado no es un repuesto válido. Debe ser una instancia de la clase Repuesto.')
        self.repuestos.remove(repuesto)
    
    def listar_repuestos(self):
        print(f'Repuestos del Imperio {self.nombre}:')
        for repuesto in self.repuestos:
            print(f'-{repuesto}')
        print()
    
    def buscar_repuesto(self, nombre : str):
        for repuesto in self.repuestos:
            if repuesto.nombre == nombre:
                return repuesto
        return None




if __name__ == "__main__":
    try:
        # 1. Creamos un almacén con algo de stock
        almacen1 = Almacen("Depósito Imperial", "Cerca de la Estrella de la Muerte")
        motor1 = Repuesto("Motor T-14", 2, "Chatarrerías Watto", 1500.0)
        almacen1.agregar_repuesto(motor1)

        # 2. Creamos un Caza (Recuerda ajustar el constructor según tu Nave)
        caza1 = Caza("CAZA Advanced", [], 'C-001', 5578, 1)
        # Nota: asegúrate de que Caza pase el ID y Clave a Nave
                
        # 3. Intentamos pedir un repuesto con CLAVE INCORRECTA
        print(almacen1)
        try:
            caza1.solicitar_repuesto(almacen1, motor1, 1500)
            print(caza1)
            almacen1.listar_repuestos()
        except ErrorImperio as e:
            print(f"Error: {e}")



        try:
        # 4. Intentamos pedir un repuesto con CLAVE CORRECTA
        # Suponiendo que la clave es 1500
            caza1.solicitar_repuesto(almacen1, motor1, 5578)
            print(caza1)
            almacen1.listar_repuestos()
        except ErrorImperio as e:
            print(f"Error: {e}")
            


           
        print("--- INICIANDO PROTOCOLO DE PRUEBAS IMPERIALES ---\n")
        
        # 1. Configuración Inicial
        almacen_vader = Almacen("Depósito Estrella de la Muerte", "Sector 0")
        motor = Repuesto("Motor Iónico T-IE", 1, "Sienar Fleet", 5000.0)
        almacen_vader.agregar_repuesto(motor)
        
        mi_caza = Caza("TIE Advanced x1", [], "VADER-001", 1138, 1)

        # --- TRANSACCIÓN 1: Éxito ---
        print("TRANSACCIÓN 1: Solicitud correcta")
        try:
            mi_caza.solicitar_repuesto(almacen_vader, motor, 1138)
        except ErrorImperio as e:
            print(f"Error: {e}")
        print("-" * 30)

        # --- TRANSACCIÓN 2: Error de Clave ---
        print("TRANSACCIÓN 2: Clave de seguridad incorrecta")
        try:
            mi_caza.solicitar_repuesto(almacen_vader, motor, 9999)
        except ErrorImperio as e:
            print(f"CAPTURA EXITOSA: {e}")
        print("-" * 30)

        # --- TRANSACCIÓN 3: Error de Pieza Repetida ---
        print("TRANSACCIÓN 3: Pieza ya instalada")
        try:
            # Volvemos a pedir el motor que ya instalamos en la T1
            mi_caza.solicitar_repuesto(almacen_vader, motor, 1138)
        except ErrorImperio as e:
            print(f"CAPTURA EXITOSA: {e}")
        print("-" * 30)

        # --- TRANSACCIÓN 4: Error de Stock ---
        print("TRANSACCIÓN 4: Stock insuficiente")
        try:
            # Añadimos una pieza nueva pero solo 1 unidad
            laser = Repuesto("Cañón Láser L-s9", 1, "Sienar", 1200.0)
            almacen_vader.agregar_repuesto(laser)
            
            caza_aux = Caza("TIE Fighter", [], "AUX-99", 0000, 1)
            caza_aux.solicitar_repuesto(almacen_vader, laser, 0000) # Se lleva el único que hay
            
            # Intentamos pedir otro
            mi_caza.solicitar_repuesto(almacen_vader, laser, 1138)
        except ErrorImperio as e:
            print(f"CAPTURA EXITOSA: {e}")
        print("-" * 30)

        # --- RESULTADO FINAL ---
        print("\n--- RESUMEN DE ESTADO ---")
        print(mi_caza)
        mi_caza.ver_piezas()
        almacen_vader.ver_catalogo()

    except ErrorImperio as e:
        print(f"Error en la operación: {e}")