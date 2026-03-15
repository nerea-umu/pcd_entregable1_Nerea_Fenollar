import pytest
from MiImperio import *


# creamos fixtures para los tests:
@pytest.fixture
def almacen_pruebas():
    almacen = Almacen("Base de Pruebas", "Sistema Alfa")
    repuesto = Repuesto("Motor Iónico", 2, "Sienar", 1000.0)
    almacen.agregar_repuesto(repuesto)
    return almacen

@pytest.fixture
def mi_caza():
    """Crea un caza para los tests."""
    return Caza("TIE-Test", [], "ID-999", 1234, 1)


# TEST DE SOLICITUD DE REPUESTOS
def test_solicitar_repuesto_exitoso(almacen_pruebas, mi_caza):
    repuesto = almacen_pruebas.buscar_repuesto('Motor Iónico')
    mi_caza.solicitar_repuesto(almacen_pruebas, repuesto, 1234)

    assert len(mi_caza.piezas) == 1
    assert mi_caza.piezas[0].nombre == 'Motor Iónico'
    assert repuesto.get_cantidad() == 1  


# TEST DE SOLICITUD DE REPUESTOS CON CLAVE INCORRECTA
def test_solicitar_repuesto_error_clave(almacen_pruebas, mi_caza):
    repuesto = almacen_pruebas.buscar_repuesto('Motor Iónico')
    with pytest.raises(ErrorImperio) as exc_info:
        mi_caza.solicitar_repuesto(almacen_pruebas, repuesto, 9999)  # Clave incorrecta


# TEST DE PIEZA YA INCLUIDA
def test_pieza_ya_incluida(almacen_pruebas, mi_caza):
    repuesto = almacen_pruebas.buscar_repuesto('Motor Iónico')
    mi_caza.solicitar_repuesto(almacen_pruebas, repuesto, 1234)  # Primera solicitud exitosa
    with pytest.raises(PiezaYaIncluida):
        mi_caza.solicitar_repuesto(almacen_pruebas, repuesto, 1234)


# TEST DE STOCK INSUFICIENTE
def test_stock_limite_con_objeto(almacen_pruebas, mi_caza):
    """Verifica que el objeto actualiza su stock correctamente hasta agotarse."""
    repuesto = almacen_pruebas.buscar_repuesto("Motor Iónico")
    
    # El stock inicial es 2 (definido en la fixture)
    mi_caza.solicitar_repuesto(almacen_pruebas, repuesto, 1234) # Queda 1
    
    # Creamos otra nave para agotar el stock
    otra_nave = Caza("TIE-2", [], "ID-002", 5555, 1)
    otra_nave.solicitar_repuesto(almacen_pruebas, repuesto, 5555) # Queda 0
    
    # Intentar sacar una tercera unidad del mismo objeto debe dar error
    with pytest.raises(StockInsuficienteError):
        repuesto.actualiza_stock(-1)