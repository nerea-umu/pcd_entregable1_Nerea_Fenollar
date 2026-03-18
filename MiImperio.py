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
        return f'Unidad de combate: {self.id_combate} \nClave CIF: {self.clave_cif}\n'





class Nave(Unidad_Combate):
    def __init__(self, id_combate : str, clave_cif : int, nombre : str, piezas : list = None):
        super().__init__(id_combate, clave_cif)
        self.nombre = nombre
        self.piezas = piezas if piezas else []


    def __str__(self):
        return super().__str__() + f'Nave: {self.nombre} \nPiezas: {len(self.piezas)}\n'
    


    def solicitar_repuesto(self, almacen, repuesto):
        if not isinstance(repuesto, Repuesto):
            raise ObjetoErroneo('El objeto proporcionado no es un repuesto válido. Debe ser una instancia de la clase Repuesto.')

        if repuesto in self.piezas:
            raise PiezaYaIncluida(f'La nave ya tiene el repuesto "{repuesto.nombre}".')
        
        almacen.eliminar_repuesto(repuesto, 1)
        self.piezas.append(repuesto)
    

    def ver_piezas(self):
        print(f'Piezas de la nave {self.nombre}:')
        for pieza in self.piezas:
            print(pieza)
        print()




class Estacion_espacial(Propiedades, Nave):
    def __init__(self, nombre : str, piezas : list, id_combate : str, clave_cif : int, tripulacion : int, pasaje : int, ubicacion : Ubicacion):
        Propiedades.__init__(self, tripulacion, pasaje)
        Nave.__init__(self, id_combate, clave_cif, nombre, piezas)
        self.ubicacion = ubicacion

    def __str__(self):
        return f'Tipo de unidad: Estación Espacial\n' + super().__str__() + f'\nTripulación: {self.tripulacion} \nPasaje: {self.pasaje} \nUbicación: {self.ubicacion.name}\n'
    
    def get_ubicacion(self):
        return self.ubicacion
    
    def set_ubicacion(self, ubicacion : Ubicacion):
        self.ubicacion = ubicacion
    
    def get_capacidad(self):
        return self.tripulacion + self.pasaje


class Nave_estelar(Propiedades, Nave):
    def __init__(self, nombre : str, piezas : list, id_combate : str, clave_cif : int, tripulacion : int, pasaje : int, clase : Clase):
        Propiedades.__init__(self, tripulacion, pasaje)
        Nave.__init__(self, id_combate, clave_cif, nombre, piezas)
        self.clase = clase
    
    def __str__(self):
        return f'Tipo de unidad: Nave Estelar\n' + super().__str__() + f'\nTripulación: {self.tripulacion} \nPasaje: {self.pasaje} \nClase: {self.clase.name}\n'
    
    def get_clase(self):
        return self.clase
    
    def set_clase(self, clase : Clase):
        self.clase = clase

    def get_capacidad(self):
        return self.tripulacion + self.pasaje


class Caza(Nave):
    def __init__(self, nombre : str, piezas : list, id_combate : str, clave_cif : int, dotacion : int):
        Nave.__init__(self, id_combate, clave_cif, nombre, piezas)
        self.dotacion = dotacion
    
    def __str__(self):
        return f'Tipo de unidad: Caza\n' + super().__str__() + f'Dotación: {self.dotacion}\n'
    
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
        return f'Repuesto: {self.nombre} \nCantidad: {self.__cantidad} \nProveedor: {self.proveedor} \nPrecio: ${self.precio:.2f}\n'
    
    def actualiza_stock(self, unidades : int):
        if self.__cantidad + unidades < 0:
            raise StockInsuficienteError(f'No se puede reducir el stock del repuesto "{self.nombre}". Stock actual: {self.__cantidad}')
        self.__cantidad += unidades

    def get_nombre(self):
        return self.nombre
    
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
    def __init__(self, nombre : str, ubicacion : str, catalogo : list = None):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.catalogo = catalogo if catalogo else []
    
    def __str__(self):
        return f'Almacén: {self.nombre} \nUbicación: {self.ubicacion} \nCatálogo: {len(self.catalogo)} repuestos\n'
    
    def buscar_repuesto(self, nombre_pieza : str):
        for repuesto in self.catalogo:
            if repuesto.get_nombre() == nombre_pieza:
                return repuesto
        raise PiezaNoEncontradaError(f'El repuesto "{nombre_pieza}" no se encuentra en el catálogo.')
    

    def ver_catalogo(self):
        print(f'Catálogo del almacén {self.nombre}:')
        for repuesto in self.catalogo:
            print(f'-{repuesto}')
        print('\n')
    


    def agregar_repuesto(self, repuesto : Repuesto):
        if not isinstance(repuesto, Repuesto):
            raise ObjetoErroneo('El objeto proporcionado no es un repuesto válido. Debe ser una instancia de la clase Repuesto.')
        if repuesto in self.catalogo:
            raise PiezaYaIncluida(f'El repuesto "{repuesto.nombre}" ya existe en el catálogo.')
        else:
            self.catalogo.append(repuesto)
    
    def eliminar_repuesto(self, repuesto : Repuesto, cantidad : int):
        if repuesto not in self.catalogo: 
            raise PiezaNoEncontradaError(f'El repuesto "{repuesto.nombre}" no se encuentra en el catálogo.')
        
        repuesto.actualiza_stock(-cantidad)

        if repuesto.get_cantidad() == 0:
            self.catalogo.remove(repuesto)

        return repuesto
    
    def eliminar_almacen(self):
        self.catalogo.clear()
        print(f'El almacén "{self.nombre}" ha sido eliminado.')
    

    

class MiImperio():
    def __init__(self, nombre : str):
        self.nombre = nombre
        self.naves = []
        self.almacenes = []
        self.repuestos = []
    
    def __str__(self):
        return f'Mi Imperio: {self.nombre} \nNaves: {len(self.naves)} \nAlmacenes: {len(self.almacenes)} \nRepuestos: {len(self.repuestos)}\n'
    
    def agregar_nave(self, nave : Nave):
        if not isinstance(nave, Nave):
            raise ObjetoErroneo('El objeto proporcionado no es una nave válida. Debe ser una instancia de la clase Nave.')
        if nave in self.naves:
            raise PiezaYaIncluida(f'La nave "{nave.nombre}" ya existe en el imperio.')
        else:
            self.naves.append(nave)
    
    def eliminar_nave(self, nave : Nave):
        if not isinstance(nave, Nave):
            raise ObjetoErroneo('El objeto proporcionado no es una nave válida. Debe ser una instancia de la clase Nave.')
        if nave not in self.naves:
            raise PiezaNoEncontradaError(f'La nave "{nave.nombre}" no se encuentra en el imperio.')
        else:
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
        if almacen in self.almacenes:
            raise PiezaYaIncluida(f'El almacén "{almacen.nombre}" ya existe en el imperio.')
        else:
            self.almacenes.append(almacen)
    
    def eliminar_almacen(self, almacen : Almacen):
        if not isinstance(almacen, Almacen):
            raise ObjetoErroneo('El objeto proporcionado no es un almacén válido. Debe ser una instancia de la clase Almacen.')
        if almacen not in self.almacenes:
            raise PiezaNoEncontradaError(f'El almacén "{almacen.nombre}" no se encuentra en el imperio.')
        else:
            for almacen in self.almacenes:
                if almacen.nombre == almacen.nombre:
                    almacen.eliminar_almacen()
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
































if __name__ == "__main__":
    try:
        print("=== PROTOCOLO DE PRUEBAS DEL SISTEMA IMPERIAL ===\n")
    
        # 1. PRUEBA DE LA CLASE: Repuesto
        print("-------------Probando repuestos:-------------")
        r_motor = Repuesto("Motor Iónico S-1", 5, "Sienar Fleet Systems", 2500.0)
        r_laser = Repuesto("Cañón Láser pesado", 2, "Kuat Drive Yards", 1200.0)
        print(r_motor)
        print(r_laser.get_proveedor())
        r_lanzallamas = Repuesto("Lanzallamas FireBlast-9", 3, "Sienar Fleet Systems", 10000.0)
        r_rueda = Repuesto("Rueda de repuesto", 7, "Kuat Drive Yards", 700.0)
        r_motor2 = Repuesto("Motor Sónico S-8", 4, "Sienar Fleet Systems", 4500.0)
        r_pantalla = Repuesto("Pantalla táctil P-12", 2, "Kuat Drive Yards", 1200.0)

        # 2. PRUEBA DE LA CLASE: Almacen
        print("\n-------------Probando almacenes:-------------")
        almacen_central = Almacen("Almacén de Coruscant", "Sector 4")
        almacen_central.agregar_repuesto(r_motor)
        almacen_central.agregar_repuesto(r_laser)
        print(almacen_central)
        almacen_central.ver_catalogo()
        almacen_jhonson = Almacen("Almacén de Jhonson", "Sector 7")
        almacen_jhonson.agregar_repuesto(r_lanzallamas)
        almacen_jhonson.agregar_repuesto(r_rueda)
        almacen_jhonson.agregar_repuesto(r_motor2)
        almacen_jhonson.agregar_repuesto(r_pantalla)
        print(almacen_jhonson)
        almacen_jhonson.ver_catalogo()


        # 3. PRUEBA DE LA CLASE: Caza (Herencia de Nave)
        print("\n-------------Probando cazas:-------------")
        tie_vader = Caza("TIE Advanced x1", [], "VADER-01", 1138, 1)
        print(tie_vader)
        tie_vader.solicitar_repuesto(almacen_central, r_motor)
        almacen_central.ver_catalogo()
        tie_vader.solicitar_repuesto(almacen_jhonson, r_rueda)
        print(tie_vader)
        tie_vader.ver_piezas()


        # 4. PRUEBA DE LA CLASE: Nave_estelar (Herencia Múltiple y Enum Clase)
        print("\n-------------Probando Nave Estelar:-------------")
        ejecutor1 = Nave_estelar("Ejecutor-001", [], "EXEC-001", 9003, 50000, 38000, Clase.EJECUTOR)
        print(ejecutor1)
        print(ejecutor1.get_clase().name)
        ejecutor1.solicitar_repuesto(almacen_jhonson, r_pantalla)
        ejecutor1.ver_piezas()


        # 5. PRUEBA DE LA CLASE: Estacion_espacial (Herencia Múltiple y Enum Ubicación)
        print("\n-------------Probando Estación Espacial:-------------")
        estrella_muerte = Estacion_espacial("Estrella de la Muerte", [], "DS-01", 4439, 250000, 1000000, Ubicacion.ENDOR)
        estrella_muerte.solicitar_repuesto(almacen_central, r_laser)
        estrella_muerte.solicitar_repuesto(almacen_jhonson, r_lanzallamas)
        print(estrella_muerte)
        print(estrella_muerte.get_ubicacion().name)
        print(f'Capacidad total de la estación: {estrella_muerte.get_capacidad()} mandalorianos')


        # 6. PRUEBA DE LA CLASE: MiImperio (Gestión de colecciones)
        print("\n-------------Probando Imperio:-------------")
        imperio = MiImperio("Imperio Galáctico")
        imperio.agregar_nave(tie_vader)
        imperio.agregar_nave(ejecutor1)
        imperio.agregar_nave(estrella_muerte)
        imperio.agregar_almacen(almacen_central)
        imperio.agregar_almacen(almacen_jhonson)
        imperio.listar_naves()
        imperio.get_nave("TIE Advanced x1").ver_piezas()
        imperio.listar_almacenes()


        # 8. PRUEBA DE EXCEPCIONES:
        print("\n-------------Probando Excepciones:-------------")
        
        # Error 1: Pieza ya incluida
        try:
            tie_vader.solicitar_repuesto(almacen_central, r_motor)
        except PiezaYaIncluida as e:
            print(f"   [CAPTURA] Error esperado: {e}")

        # Error 2: Stock insuficiente
        try:
            almacen_central.eliminar_repuesto(r_laser, 10) # Pedimos 10 pero solo hay 2
        except StockInsuficienteError as e:
            print(f"   [CAPTURA] Error esperado: {e}")

        # Error 3: Objeto Erróneo
        try:
            almacen_central.agregar_repuesto("Esto no es una pieza")
        except ObjetoErroneo as e:
            print(f"   [CAPTURA] Error esperado: {e}")

        print("\n=== PRUEBAS FINALIZADAS CON ÉXITO ===")

    except Exception as e:
        print(f"\n[ERROR CRÍTICO] Se ha detenido la prueba por: {e}")
        import traceback
        traceback.print_exc()