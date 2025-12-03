#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test para verificar la actualización de historial_transacciones()
Requisitos: 6.1, 6.3
"""

import sys
import os

# Configurar el entorno de web2py
web2py_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, web2py_path)

def test_historial_transacciones():
    """
    Verifica que la función historial_transacciones() esté actualizada
    """
    print("=" * 80)
    print("TEST: Verificación de historial_transacciones() actualizado")
    print("=" * 80)
    
    # Verificar que el controlador tiene la función actualizada
    print("\n1. Verificando función en controlador...")
    try:
        with open("controllers/divisas.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        # Verificar que existe la función
        if "def historial_transacciones():" in contenido:
            print("   ✓ Función historial_transacciones() existe")
        else:
            print("   ✗ Función historial_transacciones() NO encontrada")
            return False
        
        # Verificar que usa alias para cuentas origen y destino
        if "cuenta_origen = db.cuentas.with_alias('cuenta_origen')" in contenido:
            print("   ✓ Usa alias para cuenta_origen")
        else:
            print("   ✗ NO usa alias para cuenta_origen")
            return False
        
        if "cuenta_destino = db.cuentas.with_alias('cuenta_destino')" in contenido:
            print("   ✓ Usa alias para cuenta_destino")
        else:
            print("   ✗ NO usa alias para cuenta_destino")
            return False
        
        # Verificar que filtra por cuenta específica
        if "cuenta_especifica_id = request.vars.cuenta_id" in contenido:
            print("   ✓ Obtiene filtro de cuenta específica")
        else:
            print("   ✗ NO obtiene filtro de cuenta específica")
            return False
        
        if "if cuenta_especifica_id:" in contenido:
            print("   ✓ Aplica filtro de cuenta específica")
        else:
            print("   ✗ NO aplica filtro de cuenta específica")
            return False
        
        # Verificar que hace join con ambas cuentas
        if "left=[" in contenido and "cuenta_origen.on" in contenido and "cuenta_destino.on" in contenido:
            print("   ✓ Hace LEFT JOIN con cuentas origen y destino")
        else:
            print("   ✗ NO hace LEFT JOIN correctamente")
            return False
        
        # Verificar que selecciona los números de cuenta
        if "numero_cuenta.with_alias('numero_cuenta_origen')" in contenido:
            print("   ✓ Selecciona número de cuenta origen")
        else:
            print("   ✗ NO selecciona número de cuenta origen")
            return False
        
        if "numero_cuenta.with_alias('numero_cuenta_destino')" in contenido:
            print("   ✓ Selecciona número de cuenta destino")
        else:
            print("   ✗ NO selecciona número de cuenta destino")
            return False
        
        # Verificar que retorna cuentas_cliente para el filtro
        if "cuentas_cliente" in contenido and "return dict(" in contenido:
            print("   ✓ Retorna cuentas_cliente para el filtro")
        else:
            print("   ✗ NO retorna cuentas_cliente")
            return False
        
    except Exception as e:
        print(f"   ✗ Error leyendo controlador: {str(e)}")
        return False
    
    # Verificar que la vista muestra las cuentas origen y destino
    print("\n2. Verificando vista...")
    try:
        with open("views/divisas/historial_transacciones.html", 'r', encoding='utf-8') as f:
            contenido_vista = f.read()
        
        # Verificar que tiene columnas para cuentas origen y destino
        if "<th>Cuenta Origen</th>" in contenido_vista:
            print("   ✓ Tiene columna 'Cuenta Origen'")
        else:
            print("   ✗ NO tiene columna 'Cuenta Origen'")
            return False
        
        if "<th>Cuenta Destino</th>" in contenido_vista:
            print("   ✓ Tiene columna 'Cuenta Destino'")
        else:
            print("   ✗ NO tiene columna 'Cuenta Destino'")
            return False
        
        # Verificar que muestra los números de cuenta
        if "transaccion.cuenta_origen.numero_cuenta" in contenido_vista:
            print("   ✓ Muestra número de cuenta origen")
        else:
            print("   ✗ NO muestra número de cuenta origen")
            return False
        
        if "transaccion.cuenta_destino.numero_cuenta" in contenido_vista:
            print("   ✓ Muestra número de cuenta destino")
        else:
            print("   ✗ NO muestra número de cuenta destino")
            return False
        
        # Verificar que muestra la moneda de cada cuenta
        if "transaccion.cuenta_origen.moneda" in contenido_vista:
            print("   ✓ Muestra moneda de cuenta origen")
        else:
            print("   ✗ NO muestra moneda de cuenta origen")
            return False
        
        if "transaccion.cuenta_destino.moneda" in contenido_vista:
            print("   ✓ Muestra moneda de cuenta destino")
        else:
            print("   ✗ NO muestra moneda de cuenta destino")
            return False
        
        # Verificar que tiene filtro por cuenta específica
        if 'name="cuenta_id"' in contenido_vista:
            print("   ✓ Tiene campo de filtro por cuenta específica")
        else:
            print("   ✗ NO tiene campo de filtro por cuenta específica")
            return False
        
        if "Filtrar por Cuenta Específica" in contenido_vista:
            print("   ✓ Tiene etiqueta para filtro de cuenta")
        else:
            print("   ✗ NO tiene etiqueta para filtro de cuenta")
            return False
        
        # Verificar que itera sobre cuentas_cliente para el filtro
        if "{{for cuenta in cuentas_cliente:}}" in contenido_vista:
            print("   ✓ Itera sobre cuentas_cliente para el filtro")
        else:
            print("   ✗ NO itera sobre cuentas_cliente")
            return False
        
        # Verificar que incluye USDT en el filtro de monedas
        if '<option value="USDT">USDT</option>' in contenido_vista:
            print("   ✓ Incluye USDT en filtro de monedas")
        else:
            print("   ✗ NO incluye USDT en filtro de monedas")
            return False
        
    except Exception as e:
        print(f"   ✗ Error leyendo vista: {str(e)}")
        return False
    
    print("\n" + "=" * 80)
    print("✓ TODAS LAS VERIFICACIONES PASARON")
    print("=" * 80)
    print("\nResumen de cambios implementados:")
    print("  • Función historial_transacciones() actualizada con:")
    print("    - Alias para cuentas origen y destino")
    print("    - LEFT JOIN para obtener información de ambas cuentas")
    print("    - Filtro por cuenta específica (cuenta_id)")
    print("    - Retorna cuentas_cliente para el selector de filtro")
    print("\n  • Vista actualizada con:")
    print("    - Columnas separadas para Cuenta Origen y Cuenta Destino")
    print("    - Muestra número de cuenta y moneda de cada cuenta")
    print("    - Selector de filtro por cuenta específica")
    print("    - Incluye USDT en el filtro de monedas")
    print("\nRequisitos cumplidos: 6.1, 6.3")
    return True

if __name__ == "__main__":
    try:
        resultado = test_historial_transacciones()
        sys.exit(0 if resultado else 1)
    except Exception as e:
        print(f"\n✗ Error ejecutando test: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
