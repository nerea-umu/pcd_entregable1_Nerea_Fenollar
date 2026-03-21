from enum import Enum
from abc import ABC, abstractmethod

class ErrorImperio(Exception):
    """Clase base para excepciones del sistema."""
    pass

class PiezaNoEncontradaError(ErrorImperio):
    """clase para excepciones cuando una pieza no existe en el catálogo."""
    pass

class PiezaYaIncluida(ErrorImperio):
    """clase para excepciones cuando una pieza ya existe en el catálogo."""
    pass

class StockInsuficienteError(ErrorImperio):
    """clase para excepciones cuando no quedan suficientes unidades de un repuesto."""
    pass

class ObjetoErroneo(ErrorImperio):
    """clase para excepciones cuando un objeto proporcionado no es válido para el método."""
    pass




class Clase(Enum):  # enumeración para las clases de naves estelares
    EJECUTOR = 1
    ECLIPSE = 2
    SOBERANO = 3


class Ubicacion(Enum):  # enumeración para las ubicaciones de las estaciones espaciales
    ENDOR = 1
    CUMULO_RAIMOS = 2
    NEBULOSA_KALIIDA = 3


class Propiedades(ABC):  # clase abstracta para las propiedades que comparten tanto las naves estelares como las estaciones espaciales
    def __init__(self, tripulacion : int, pasaje : int):
        self.tripulacion = tripulacion
        self.pasaje = pasaje
     

class Unidad_Combate(ABC):  
    # clase abstracta que engloba todas las unidades de combate, tanto naves como otro tipo de vehículos que puedad
    # formar parte del imperio.

    def __init__(self, id_combate : str, clave_cif : int):
        self.id_combate = id_combate
        self.clave_cif = clave_cif

    def __str__(self):
        return f'Unidad de combate: {self.id_combate} \nClave CIF: {self.clave_cif}\n'





class Nave(Unidad_Combate):
    # Clase base que representa una nave genérica. Tanto las naves estelares como los cazas y las estaciones espaciales heredan de esta clase.
    # pero no contiene todo los tipos de vehículos del imperio, por eso hereda de Unidad_Combate.
    def __init__(self, id_combate : str, clave_cif : int, nombre : str, piezas : list = None):
        super().__init__(id_combate, clave_cif)
        self.nombre = nombre
        self.piezas = piezas if piezas else []


    def __str__(self):
        return super().__str__() + f'Nave: {self.nombre} \nPiezas: {len(self.piezas)}\n'
    

    def solicitar_repuesto(self, almacen, repuesto):  
        # Este método permite a una nave solicitar un repuesto a un almacén para su reparación, sin embargo, es el 
        # imperio el que debe gestionar la reparación, así que este método será utilizado en uno de los métodos de la clase
        # MiImperio (reparar_nave()).

        if not isinstance(repuesto, Repuesto):  # Nos aseguramos de que lo que se le pase sea un repuesto de la clase Repuesto
            raise ObjetoErroneo('El objeto proporcionado no es un repuesto válido. Debe ser una instancia de la clase Repuesto.')

        if repuesto in self.piezas:  # Nos aseguramos de que la nave no tenga ya el repuesto reparado
            raise PiezaYaIncluida(f'La nave ya tiene el repuesto "{repuesto.nombre}".')
        
        almacen.eliminar_repuesto(repuesto, 1)  # Eliminamos el repuesto del almacén
        self.piezas.append(repuesto)  # Agregamos el repuesto a la nave
    

    def ver_piezas(self):  # Método básico para mostrar las piezas que ha reparado la nave.
        print(f'Piezas de la nave {self.nombre}:')
        for pieza in self.piezas:
            print(pieza)
        print()




class Estacion_espacial(Propiedades, Nave):
    # Clase que representa una estación espacial, hereda tanto de Nave como de Propiedades, ya que es una nave y también comparte propiedades.
    # Esta clase es un ejemplo de herencia múltiple. Sólo tendrá métodos relacionados con la gestión de su ubicación y capacidad, ya que el resto
    # de métodos relacionados con la reparación y gestión de piezas los hereda de Nave.

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
    # Clase que representa a una nave estelar, es igual que la estación espacial, hereda tanto de Nave como de Propiedades y solo tiene métodos básicos
    # para la gestión de su clase.

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
    # Clase que representa a un caza galáctico, hereda de Nave, pero no de Propiedades, no comparte las mismas propiedades que las naves estelares y estaciones espaciales.
    # Esta clase solo tiene un atributo específico para gestionar la dotación de mandalorianos que tiene el caza, es un vehículo más pequeño y no cuenta con pasaje ni tripulación.
    # Además también contiene únicamente métodos para la gestión de su dotación.

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
    # Clase que representa a un repuesto, piezas que pueden ser utilizadas para reparar las naves del imperio, cada repuesto tiene un nombre, una cantidad en stock, 
    # un proveedor y un precio. Esta clase tiene métodos para gestionar el stock de cada repuesto, lo que nos permitirá aumentar o reducirlo conforme la gestión
    # del imperio lo necesite, así como métodos básicos para la gestión de sus atributos.

    def __init__(self, nombre : str, cantidad : int, proveedor : str, precio : float):
        self.nombre = nombre
        self.__cantidad = cantidad
        self.proveedor = proveedor
        self.precio = precio

    def __str__(self):
        return f'Repuesto: {self.nombre} \nCantidad: {self.__cantidad} \nProveedor: {self.proveedor} \nPrecio: ${self.precio:.2f}\n'
    
    def actualiza_stock(self, unidades : int):  # Este método a parte permite al imperio manipular el stock de cada repuesto, ya que es un atributo privado.
        if self.__cantidad + unidades < 0:
            raise StockInsuficienteError(f'No se puede reducir el stock del repuesto "{self.nombre}". Stock actual: {self.__cantidad}')
        self.__cantidad += unidades

    def get_nombre(self):
        return self.nombre
    
    def get_cantidad(self):  # Al igual que neceistamos un método a parte para poder ver el stock de cada repuesto.
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
# Clase que representa a un almacén del imperio, cada almacén tiene un nombre, una ubicación y un catálogo de repuestos disponibles. 
# Esta clase tiene métodos para gestionar su catálogo de repuestos y visualizarlo.

    def __init__(self, nombre : str, ubicacion : str, catalogo : list = None):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.catalogo = catalogo if catalogo else []
    
    def __str__(self):
        return f'Almacén: {self.nombre} \nUbicación: {self.ubicacion} \nCatálogo: {len(self.catalogo)} repuestos\n'
    
    def buscar_repuesto(self, nombre_pieza : str):  
        # Método para buscar un repuesto en el catálogo del almacén por su nombre. 
        for repuesto in self.catalogo:
            if repuesto.get_nombre() == nombre_pieza:  # devuelve el repuesto si lo encuentra
                return repuesto
        raise PiezaNoEncontradaError(f'El repuesto "{nombre_pieza}" no se encuentra en el catálogo.')  #  o lanza una excepción si no lo encuentra.
    

    def ver_catalogo(self):  # Método básico para listar todos los repuestos del catálogo del almacén. Funciona porque cada repuesto tiene su propio método __str__ para mostrar su información.
        print(f'Catálogo del almacén {self.nombre}:')
        for repuesto in self.catalogo:
            print(f'-{repuesto}')
        print('\n')
    

    def agregar_repuesto(self, repuesto : Repuesto):  
        # Método para agregar un repuesto al catálogo del almacén, esta gestión también se realiza a través del método comprar_repuesto() de la clase MiImperio, 
        # pero es necesario que el almacén tenga un método para agregar repuestos a su catálogo.
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
    

    def _eliminar_almacen(self):  
        # Si el imperio decide eliminar un almacén, también se eliminarán todos los repuestos de su catálogo. 
        # Este método es privado porque solo debe ser utilizado por la clase MiImperio a través del método eliminar_almacen().
        self.catalogo.clear()
        print(f'El almacén "{self.nombre}" ha sido eliminado.')
    

    

class MiImperio():
    # Clase que representa a nuestro imperio galáctico, esta clase es la encargada de gestionar todas las naves, almacenes y repuestos del imperio, 
    # así como de gestionar las reparaciones de las naves a través de los almacenes y repuestos disponibles. 
    # Esta clase tiene métodos para agregar, eliminar y listar naves, almacenes y repuestos, así como un método específico para gestionar la reparación de las naves.

    def __init__(self, nombre : str, balance : float):  # Se debe iniciar el imperio con un capital bastante alto.
        self.nombre = nombre
        self.balance = balance 
        self.naves = []
        self.almacenes = []
        self.repuestos = []
    
    def __str__(self):
        return f'Mi Imperio: {self.nombre} \nBalance: {self.balance}$ \nNaves: {len(self.naves)} \nAlmacenes: {len(self.almacenes)} \nRepuestos: {len(self.repuestos)}\n'
    
    def get_nombre(self):
        return self.nombre
    
    def get_balance(self):
        return self.balance
    
    
    def agregar_nave(self, nave : Nave):  # Agrega una nave o unidad de combate al imperio
        if not isinstance(nave, Nave):
            raise ObjetoErroneo('El objeto proporcionado no es una nave válida. Debe ser una instancia de la clase Nave.') 
        if nave in self.naves:
            raise PiezaYaIncluida(f'La nave "{nave.nombre}" ya existe en el imperio.')
        else:
            self.naves.append(nave)  # Añade la nave a la lista de naves del imperio
    

    def eliminar_nave(self, nave : Nave):  # De igual manera, elimina una nave o unidad de combate del imperio
        if not isinstance(nave, Nave):
            raise ObjetoErroneo('El objeto proporcionado no es una nave válida. Debe ser una instancia de la clase Nave.')
        if nave not in self.naves:
            raise PiezaNoEncontradaError(f'La nave "{nave.nombre}" no se encuentra en el imperio.')
        else:
            self.naves.remove(nave)
    

    def get_nave(self, nombre : str):  # Método para buscar una nave por su nombre, devuelve la nave si la encuentra o None si no la encuentra.
        # este método es útil para luego poder gestionar la reparación de las naves o simplemente para buscar una nave en específico.
        for nave in self.naves:
            if nave.nombre == nombre:
                return nave
        return None
    

    def listar_naves(self):  # Método básico para listar todas las naves del imperio, funciona porque cada nave tiene su propio método __str__ para mostrar su información.
        print(f'Naves del Imperio {self.nombre}:')
        for nave in self.naves:
            print(f'-{nave}')
        print()


    def reparar_nave(self, nave, almacen, repuesto):  # Método importante para gestionar la reparación de las naves del imperio.
        # Es el imperio el que repara la nave con el repuesto de un almacén específico, por eso a este método hay que proporcionarle la nave que ha de ser
        # reparada, el almacén donde se encuentra el repuesto y el repuesto con el que se va a reparar la nave.

        if not isinstance(nave, Nave):
            raise ObjetoErroneo('El objeto proporcionado no es una nave válida. Debe ser una instancia de la clase Nave.')
        if not isinstance(almacen, Almacen):
            raise ObjetoErroneo('El objeto proporcionado no es un almacén válido. Debe ser una instancia de la clase Almacen.')
        if not isinstance(repuesto, Repuesto):
            raise ObjetoErroneo('El objeto proporcionado no es un repuesto válido. Debe ser una instancia de la clase Repuesto.')
        
        nave.solicitar_repuesto(almacen, repuesto) 
    


    def agregar_almacen(self, almacen : Almacen):  # Método para agregar un almacén al imperio
        if not isinstance(almacen, Almacen):
            raise ObjetoErroneo('El objeto proporcionado no es un almacén válido. Debe ser una instancia de la clase Almacen.')
        if almacen in self.almacenes:
            raise PiezaYaIncluida(f'El almacén "{almacen.nombre}" ya existe en el imperio.')
        else:
            self.almacenes.append(almacen)


    def eliminar_almacen(self, almacen : Almacen):  # Método para eliminar un almacén del imperio
        if not isinstance(almacen, Almacen):
            raise ObjetoErroneo('El objeto proporcionado no es un almacén válido. Debe ser una instancia de la clase Almacen.')
        if almacen not in self.almacenes:
            raise PiezaNoEncontradaError(f'El almacén "{almacen.nombre}" no se encuentra en el imperio.')
        else:
            for a in self.almacenes:
                if a.nombre == almacen.nombre:
                    almacen._eliminar_almacen()    # Si se elimina un almacén, también se eliminan todos los repuestos de su catálogo.
                    self.almacenes.remove(a) # y se elimina el almacén de la lista de almacenes del imperio.
    

    def get_almacen(self, nombre : str):  # Método para buscar un almacén por su nombre.
        for almacen in self.almacenes:
            if almacen.nombre == nombre:  # devuelve el almacén si lo encuentra 
                return almacen
        return None                       # o None si no lo encuentra.
    

    def listar_almacenes(self):  # Método básico para listar todos los almacenes del imperio, funciona porque cada almacén tiene su propio método __str__ para mostrar su información.
        print(f'Almacenes del Imperio {self.nombre}:')
        for almacen in self.almacenes:
            print(f'-{almacen}')
        print()
    

    def comprar_repuesto(self, repuesto : Repuesto, almacen : Almacen):  # Método para comprar un repuesto. 
        # Necesita el repuesto que se va a comprar y el almacén donde se va a agregar el repuesto
        if not isinstance(repuesto, Repuesto):
            raise ObjetoErroneo('El objeto proporcionado no es un repuesto válido. Debe ser una instancia de la clase Repuesto.')
        if not isinstance(almacen, Almacen):
            raise ObjetoErroneo('El objeto proporcionado no es un almacén válido. Debe ser una instancia de la clase Almacen.')
        if self.balance < repuesto.get_precio():
            raise StockInsuficienteError(f'No se puede comprar el repuesto "{repuesto.nombre}". Balance insuficiente. Balance actual: ${self.balance:.2f}, Precio del repuesto: ${repuesto.get_precio():.2f}')
        self.balance -= repuesto.get_precio()  # Se descuenta el precio del repuesto del balance del imperio
        almacen.agregar_repuesto(repuesto)     # El imperio debe gestionar la agregación de repuestos a los almacenes a través de este método
        self.repuestos.append(repuesto)        # y añadirlo a su lista de repuestos para poder llevar un control de todas las piezas del imperio.
    

    def vender_repuesto(self, repuesto : Repuesto):  # Método para vender un repuesto si ya no se necesita.
        if not isinstance(repuesto, Repuesto):
            raise ObjetoErroneo('El objeto proporcionado no es un repuesto válido. Debe ser una instancia de la clase Repuesto.')
            
        encontrado = False
        for almacen in self.almacenes:
            if repuesto in almacen.catalogo:
                almacen.eliminar_repuesto(repuesto, 1)  # El imperio debe gestionar la eliminación de repuestos de los almacenes a través de este método
                encontrado = True
                break
        if not encontrado:   # Con esto nos aseguramos de que si el repuesto no se encuentra en ningún almacén del imperio, no se pueda vender y se lance una excepción.
            raise PiezaNoEncontradaError(f'El repuesto "{repuesto.nombre}" no se encuentra en ningún almacén del imperio.')
        
        self.balance += repuesto.get_precio()           # Se suma el precio del repuesto al balance del imperio
        self.repuestos.remove(repuesto)                 # y eliminarlo de su lista de repuestos.
    


    def listar_repuestos(self):  # Método básico para listar todos los repuestos del imperio, muestra los repuestos de cada almacén.
        print(f'Repuestos del Imperio {self.nombre}:')
        for almacen in self.almacenes:  
            almacen.ver_catalogo()
        print()










if __name__ == "__main__":
    try:
        print("=== PROTOCOLO DE PRUEBAS DEL SISTEMA IMPERIAL ===\n")
        imperio = MiImperio("Imperio Galáctico", 500000000.0)
    
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
        imperio.agregar_almacen(almacen_central)
        imperio.comprar_repuesto(r_motor, almacen_central)
        imperio.comprar_repuesto(r_laser, almacen_central)
        print(almacen_central)
        almacen_central.ver_catalogo()

        almacen_jhonson = Almacen("Almacén de Jhonson", "Sector 7")
        imperio.agregar_almacen(almacen_jhonson)
        imperio.comprar_repuesto(r_lanzallamas, almacen_jhonson)
        imperio.comprar_repuesto(r_rueda, almacen_jhonson)
        imperio.comprar_repuesto(r_motor2, almacen_jhonson)
        imperio.comprar_repuesto(r_pantalla, almacen_jhonson)
        print(almacen_jhonson)
        almacen_jhonson.ver_catalogo()


        # 3. PRUEBA DE LA CLASE: Caza (Herencia de Nave)
        print("\n-------------Probando cazas:-------------")
        tie_vader = Caza("TIE Advanced x1", [], "VADER-01", 1138, 1)
        imperio.agregar_nave(tie_vader)
        print(tie_vader)
        imperio.reparar_nave(tie_vader, almacen_central, r_motor)
        almacen_central.ver_catalogo()
        imperio.reparar_nave(tie_vader, almacen_jhonson, r_rueda)
        print(tie_vader)
        tie_vader.ver_piezas()


        # 4. PRUEBA DE LA CLASE: Nave_estelar (Herencia Múltiple y Enum Clase)
        print("\n-------------Probando Nave Estelar:-------------")
        ejecutor1 = Nave_estelar("Ejecutor-001", [], "EXEC-001", 9003, 50000, 38000, Clase.EJECUTOR)
        imperio.agregar_nave(ejecutor1)
        print(ejecutor1)
        print(ejecutor1.get_clase().name)
        imperio.reparar_nave(ejecutor1, almacen_jhonson, r_pantalla)
        ejecutor1.ver_piezas()


        # 5. PRUEBA DE LA CLASE: Estacion_espacial (Herencia Múltiple y Enum Ubicación)
        print("\n-------------Probando Estación Espacial:-------------")
        estrella_muerte = Estacion_espacial("Estrella de la Muerte", [], "DS-01", 4439, 250000, 1000000, Ubicacion.ENDOR)
        imperio.agregar_nave(estrella_muerte)
        imperio.reparar_nave(estrella_muerte, almacen_central, r_laser)
        imperio.reparar_nave(estrella_muerte, almacen_jhonson, r_lanzallamas)
        print(estrella_muerte)
        print(estrella_muerte.get_ubicacion().name)
        print(f'Capacidad total de la estación: {estrella_muerte.get_capacidad()} mandalorianos')


        # 6. PRUEBA DE LA CLASE: MiImperio (Gestión de colecciones)
        print("\n-------------Probando Imperio:-------------")
        imperio.listar_naves()
        imperio.get_nave("TIE Advanced x1").ver_piezas()
        imperio.listar_almacenes()
        imperio.listar_repuestos()
        print(f'Balance del imperio: ${imperio.get_balance():.2f}')
        imperio.vender_repuesto(r_motor)
        print(f'Balance del imperio después de vender un repuesto: ${imperio.get_balance():.2f}')


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