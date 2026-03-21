import pytest
from MiImperio import *


# --- FIXTURES  ---
@pytest.fixture
def sistema_basico():
    imperio = MiImperio("Imperio de Prueba", 4400000000.0)
    almacen = Almacen("Almacen 7", "Sector 0")
    nave = Caza("Caza 1", [], "C-001", 1234, 1)
    repuesto = Repuesto("Laser", 2, "proveedor1", 500.0)
    
    imperio.agregar_almacen(almacen)
    imperio.agregar_nave(nave)
    imperio.comprar_repuesto(repuesto, almacen)
    
    return imperio, nave, almacen, repuesto



def test_reparar_nave_exito(sistema_basico):
    # Verifica que se puede reparar una nave con un repuesto disponible en un almacén.
    imperio, nave, almacen, repuesto = sistema_basico
    
    # Acción
    imperio.reparar_nave(nave, almacen, repuesto)
    
    # Verificaciones
    assert repuesto in nave.piezas  # La nave tiene la pieza
    assert repuesto.get_cantidad() == 1  # El stock bajó de 2 a 1



def test_error_pieza_duplicada(sistema_basico):
    # Verifica que no se puede reparar una nave con una pieza que ya tiene.
    imperio, nave, almacen, repuesto = sistema_basico
    
    imperio.reparar_nave(nave, almacen, repuesto)  # Primera reparación
    
    with pytest.raises(PiezaYaIncluida):  # Segunda reparación (debe fallar)
        imperio.reparar_nave(nave, almacen, repuesto)



def test_error_stock_insuficiente(sistema_basico):
    # Verifica que falla si el almacén se queda sin stock.
    imperio, nave, almacen, repuesto = sistema_basico
    
    repuesto.actualiza_stock(-2)  # Gastamos el stock (había 2 unidades)
    
    with pytest.raises(StockInsuficienteError):
        imperio.reparar_nave(nave, almacen, repuesto)



def test_error_objeto_erroneo(sistema_basico):
    # Verifica la validación de tipos en reparar_nave.
    imperio, nave, almacen, repuesto = sistema_basico
    
    with pytest.raises(ObjetoErroneo):
        # Pasamos un string en lugar de un objeto Almacen para comprobar la validación de tipos
        imperio.reparar_nave(nave, "almacen", repuesto)



def test_vender_repuesto_imperio(sistema_basico):
    # Prueba el método vender_repuesto de la clase MiImperio.
    imperio, nave, almacen, repuesto = sistema_basico
    cantidad_inicial = repuesto.get_cantidad()
    
    imperio.vender_repuesto(repuesto)
    
    assert repuesto.get_cantidad() == cantidad_inicial - 1  # El stock bajó en 1    
    assert repuesto in almacen.catalogo