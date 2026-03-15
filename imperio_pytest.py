import pytest
from MiImperio import *


# --- TESTS CLASE REPUESTO ---
def test_repuesto_encapsulamiento():
    r = Repuesto("Tuerca G-7", 10, "Sienar", 5.0)
    assert r.get_cantidad() == 10
    r.actualiza_stock(-3)
    assert r.get_cantidad() == 7
    with pytest.raises(StockInsuficienteError):
        r.actualiza_stock(-10)

# --- TESTS CLASE ALMACEN ---
def test_almacen_gestion():
    alm = Almacen("Base", "Hoth")
    r = Repuesto("Panel", 1, "Kuat", 100.0)
    alm.agregar_repuesto(r)
    
    assert alm.buscar_repuesto("Panel") == r
    # Sacamos la pieza
    alm.eliminar_repuesto("Panel", 1)
    # Al llegar a 0, debería eliminarse del catálogo
    assert alm.buscar_repuesto("Panel") is None

# --- TESTS CLASE CAZA (Herencia de Nave) ---
def test_caza_seguridad():
    caza = Caza("TIE", [], "ID-1", 1234, 1)
    # Clave correcta no debería hacer nada
    caza.validar_clave(1234)
    # Clave incorrecta lanza error
    with pytest.raises(ClaveIncorrectaError):
        caza.validar_clave(0000)

# --- TESTS CLASE ESTACION ESPACIAL (Herencia Múltiple) ---
def test_estacion_propiedades():
    ee = Estacion_espacial("Estrella", [], "ID-S", 1, 100, 50, Ubicacion.ENDOR)
    assert ee.get_capacidad() == 150
    assert ee.ubicacion == Ubicacion.ENDOR

# --- TEST INTEGRACIÓN: SOLICITAR REPUESTO (Con el objeto instancia) ---
def test_flujo_solicitud_objeto():
    alm = Almacen("Terminal", "Coruscant")
    motor = Repuesto("Hyperdrive", 1, "Corellia", 5000.0)
    alm.agregar_repuesto(motor)
    
    nave = Caza("Ala-X", [], "X-01", 111, 1)
    
    # Probamos tu nueva lógica: pasar la instancia 'motor'
    nave.solicitar_repuesto(alm, motor, 111)
    
    assert len(nave.piezas) == 1
    assert motor in nave.piezas
    
    # Test de error: Pieza ya incluida
    with pytest.raises(PiezaYaIncluida):
        nave.solicitar_repuesto(alm, motor, 111)