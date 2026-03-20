import pytest
from MiImperio import *


# --- FIXTURES (Configuración base para los tests) ---
@pytest.fixture
def sistema_basico():
    imperio = MiImperio("Imperio de Prueba", 4400000000.0)
    almacen = Almacen("Almacen Test", "Sector 0")
    nave = Caza("TIE Test", [], "T-001", 1234, 1)
    repuesto = Repuesto("Laser", 2, "Kuat", 500.0)
    
    imperio.agregar_almacen(almacen)
    imperio.agregar_nave(nave)
    imperio.comprar_repuesto(repuesto, almacen)
    
    return imperio, nave, almacen, repuesto

# --- TESTS DE FUNCIONALIDAD ---

def test_reparar_nave_exito(sistema_basico):
    """Verifica que la reparación centralizada funciona y descuenta stock."""
    imperio, nave, almacen, repuesto = sistema_basico
    
    # Acción
    imperio.reparar_nave(nave, almacen, repuesto)
    
    # Verificaciones
    assert repuesto in nave.piezas  # La nave tiene la pieza
    assert repuesto.get_cantidad() == 1  # El stock bajó de 2 a 1

def test_error_pieza_duplicada(sistema_basico):
    """Verifica que no se puede reparar una nave con una pieza que ya tiene."""
    imperio, nave, almacen, repuesto = sistema_basico
    
    # Primera reparación
    imperio.reparar_nave(nave, almacen, repuesto)
    
    # Segunda reparación (debe fallar)
    with pytest.raises(PiezaYaIncluida):
        imperio.reparar_nave(nave, almacen, repuesto)

def test_error_stock_insuficiente(sistema_basico):
    """Verifica que falla si el almacén se queda sin stock."""
    imperio, nave, almacen, repuesto = sistema_basico
    
    # Gastamos el stock (había 2 unidades)
    repuesto.actualiza_stock(-2) 
    
    with pytest.raises(StockInsuficienteError):
        imperio.reparar_nave(nave, almacen, repuesto)

def test_error_objeto_erroneo(sistema_basico):
    """Verifica la validación de tipos en reparar_nave."""
    imperio, nave, almacen, repuesto = sistema_basico
    
    with pytest.raises(ObjetoErroneo):
        # Pasamos un string en lugar de un objeto Almacen
        imperio.reparar_nave(nave, "Soy un intruso", repuesto)

def test_vender_repuesto_imperio(sistema_basico):
    """Prueba el método vender_repuesto de la clase MiImperio."""
    imperio, nave, almacen, repuesto = sistema_basico
    cantidad_inicial = repuesto.get_cantidad()
    
    imperio.vender_repuesto(repuesto)
    
    assert repuesto.get_cantidad() == cantidad_inicial - 1  # El stock bajó en 1    
    assert repuesto in almacen.catalogo