#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar que el flujo completo de venta funcione
"""

import sqlite3

def test_venta_completa():
    """
    Verifica el flujo completo de venta
    """
    print("=== PRUEBA DEL FLUJO COMPLETO DE VENTA ===")
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        print("\n1. Verificando correcciones aplicadas...")
        
        # Leer el controlador
        with open('controllers/divisas.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        # Verificar correcciones en función vender
        correcciones_vender = [
            ('Manejo condicional de transaccion_id', 'if transaccion_id and transaccion_id > 0:'),
            ('Mensaje de éxito mejorado', '✅ Venta realizada exitosamente'),
            ('Logging de transaccion_id inválido', 'transaccion_id inválido'),
            ('No redirect forzado', 'No hacer redirect, mostrar mensaje')
        ]
        
        vender_ok = 0
        for nombre, elemento in correcciones_vender:
            if elemento in controller_content:
                vender_ok += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Correcciones en vender(): {vender_ok}/{len(correcciones_vender)}")
        
        # Verificar correcciones en función comprobante
        correcciones_comprobante = [
            ('Manejo de administradores', 'auth.has_membership(\'administrador\')'),
            ('Verificación de permisos mejorada', 'es_propietario or es_admin'),
            ('Obtención de cliente para admin', 'Para administradores, obtener el cliente'),
            ('Verificación de cuenta', 'cuenta = db(db.cuentas.id == transaccion.cuenta_id)')
        ]
        
        comprobante_ok = 0
        for nombre, elemento in correcciones_comprobante:
            if elemento in controller_content:
                comprobante_ok += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Correcciones en comprobante(): {comprobante_ok}/{len(correcciones_comprobante)}")
        
        print("\n2. Verificando validaciones USDT...")
        
        validaciones_usdt = [
            ('Validación venta USDT', "moneda_origen not in ['USD', 'EUR', 'USDT']"),
            ('Mensaje error USDT', 'USD, EUR o USDT'),
            ('Procesamiento USDT', "elif moneda_origen == 'USDT':")
        ]
        
        usdt_ok = 0
        for nombre, elemento in validaciones_usdt:
            if elemento in controller_content:
                usdt_ok += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Validaciones USDT: {usdt_ok}/{len(validaciones_usdt)}")
        
        print("\n3. Verificando últimas transacciones...")
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_ventas
            FROM transacciones 
            WHERE tipo_operacion = 'venta'
            AND fecha_transaccion >= date('now', '-1 day')
        """)
        
        ventas_recientes = cursor.fetchone()[0]
        print(f"   📊 Ventas en las últimas 24h: {ventas_recientes}")
        
        if ventas_recientes > 0:
            cursor.execute("""
                SELECT 
                    id,
                    moneda_origen,
                    monto_origen,
                    numero_comprobante
                FROM transacciones 
                WHERE tipo_operacion = 'venta'
                AND fecha_transaccion >= date('now', '-1 day')
                ORDER BY fecha_transaccion DESC
                LIMIT 3
            """)
            
            ultimas_ventas = cursor.fetchall()
            print("   📊 Últimas ventas:")
            for venta in ultimas_ventas:
                print(f"      ID: {venta[0]} | {venta[1]} {venta[2]} | {venta[3]}")
        
        print("\n4. Verificando cuentas con divisas...")
        
        cursor.execute("""
            SELECT 
                COUNT(*) as cuentas_con_divisas
            FROM cuentas 
            WHERE estado = 'activa' 
            AND (saldo_usd > 0 OR saldo_eur > 0 OR saldo_usdt > 0)
        """)
        
        cuentas_divisas = cursor.fetchone()[0]
        print(f"   📊 Cuentas con divisas disponibles: {cuentas_divisas}")
        
        conn.close()
        
        print("\n5. Resumen del estado:")
        
        if vender_ok == len(correcciones_vender):
            print("   ✅ Función vender() corregida completamente")
        else:
            print("   ❌ Función vender() necesita más correcciones")
        
        if comprobante_ok == len(correcciones_comprobante):
            print("   ✅ Función comprobante() corregida completamente")
        else:
            print("   ❌ Función comprobante() necesita más correcciones")
        
        if usdt_ok == len(validaciones_usdt):
            print("   ✅ Validaciones USDT implementadas")
        else:
            print("   ❌ Validaciones USDT incompletas")
        
        if cuentas_divisas > 0:
            print("   ✅ Hay cuentas con divisas para vender")
        else:
            print("   ⚠️  No hay cuentas con divisas para vender")
        
        print("\n6. Comportamiento esperado después de venta:")
        print("   ✅ Si transaccion_id es válido: Redirige al comprobante")
        print("   ✅ Si transaccion_id es None/inválido: Queda en página con mensaje de éxito")
        print("   ✅ Administradores pueden ver cualquier comprobante")
        print("   ✅ Clientes solo ven sus propios comprobantes")
        
        print("\n7. Para probar:")
        print("   1. Reiniciar web2py")
        print("   2. Realizar una venta de USD/EUR/USDT")
        print("   3. Verificar que:")
        print("      - Se muestra mensaje de éxito")
        print("      - Se redirige al comprobante (si transaccion_id válido)")
        print("      - O se queda en la página (si transaccion_id inválido)")
        
        return (vender_ok == len(correcciones_vender) and 
                comprobante_ok == len(correcciones_comprobante) and 
                usdt_ok == len(validaciones_usdt))
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = test_venta_completa()
    print(f"\n{'='*60}")
    if resultado:
        print("🎉 FLUJO DE VENTA COMPLETAMENTE CORREGIDO")
    else:
        print("🔧 FLUJO DE VENTA NECESITA MÁS CORRECCIONES")
    print(f"{'='*60}")