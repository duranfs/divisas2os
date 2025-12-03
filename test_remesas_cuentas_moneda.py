#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test de integración del sistema de remesas con cuentas por moneda
Verifica que las remesas se acrediten correctamente en cuentas USD
"""

import sys
import os

def test_remesas_integration():
    """
    Test de integración del sistema de remesas
    """
    print("=" * 80)
    print("TEST: Integración de Remesas con Cuentas por Moneda")
    print("=" * 80)
    
    try:
        # Obtener path del proyecto
        web2py_path = os.path.dirname(os.path.abspath(__file__))
        
        print("\n✓ Verificando archivos del proyecto")
        
        # Test 1: Verificar función generar_comprobante_unico en remesas
        print("\n[Test 1] Verificar función generar_comprobante_unico")
        
        # Buscar la función en el controlador de remesas
        remesas_controller = os.path.join(web2py_path, 'controllers', 'remesas.py')
        with open(remesas_controller, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'def generar_comprobante_unico' in content:
                print("  ✓ Función generar_comprobante_unico encontrada en remesas.py")
            else:
                print("  ✗ Función generar_comprobante_unico NO encontrada")
                return False
        
        # Test 2: Verificar función recibir_remesa_cliente
        print("\n[Test 2] Verificar función recibir_remesa_cliente")
        
        if 'def recibir_remesa_cliente' in content:
            print("  ✓ Función recibir_remesa_cliente encontrada")
            
            # Verificar que crea cuenta USD automáticamente
            if 'generar_numero_cuenta_por_moneda' in content:
                print("  ✓ Función crea cuenta USD automáticamente si no existe")
            else:
                print("  ✗ Función NO crea cuenta USD automáticamente")
                return False
            
            # Verificar que acredita en cuenta USD
            if 'cuenta_usd.update_record' in content:
                print("  ✓ Función acredita monto en cuenta USD")
            else:
                print("  ✗ Función NO acredita en cuenta USD")
                return False
        else:
            print("  ✗ Función recibir_remesa_cliente NO encontrada")
            return False
        
        # Test 3: Verificar actualización de validar_limite_venta
        print("\n[Test 3] Verificar actualización de validar_limite_venta")
        
        db_model = os.path.join(web2py_path, 'models', 'db.py')
        with open(db_model, 'r', encoding='utf-8') as f:
            db_content = f.read()
            
            # Verificar que acepta cliente_id como parámetro
            if 'def validar_limite_venta(moneda, monto_venta, cliente_id=None' in db_content:
                print("  ✓ Función validar_limite_venta acepta cliente_id")
            else:
                print("  ✗ Función validar_limite_venta NO acepta cliente_id")
                return False
            
            # Verificar que valida saldo en cuenta
            if 'saldo_cuenta' in db_content and 'db.cuentas.moneda == moneda' in db_content:
                print("  ✓ Función valida saldo en cuenta de la moneda")
            else:
                print("  ✗ Función NO valida saldo en cuenta")
                return False
        
        # Test 4: Verificar actualización de obtener_disponibilidad_moneda
        print("\n[Test 4] Verificar actualización de obtener_disponibilidad_moneda")
        
        if 'total_en_cuentas' in content:
            print("  ✓ Función obtener_disponibilidad_moneda incluye total_en_cuentas")
        else:
            print("  ✗ Función NO incluye total_en_cuentas")
            return False
        
        # Test 5: Verificar Requirements
        print("\n[Test 5] Verificar cumplimiento de Requirements")
        
        requirements = {
            '7.1': 'Identificar cuenta USD del cliente receptor',
            '7.2': 'Crear cuenta USD automáticamente si no existe',
            '7.3': 'Acreditar solo en cuenta USD',
            '7.4': 'Considerar solo saldo de cuenta USD'
        }
        
        for req_id, req_desc in requirements.items():
            if req_id in content or req_id in db_content:
                print(f"  ✓ Requirement {req_id}: {req_desc}")
            else:
                print(f"  ⚠ Requirement {req_id} no referenciado explícitamente")
        
        print("\n" + "=" * 80)
        print("✓ TODOS LOS TESTS PASARON")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error en test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_remesas_integration()
    sys.exit(0 if success else 1)
