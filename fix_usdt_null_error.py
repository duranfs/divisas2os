#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar y corregir el error de USDT con valores NULL
"""

import sqlite3

def fix_usdt_null_error():
    """
    Verifica y corrige el error de USDT con valores NULL
    """
    print("=== CORRECCIÓN DEL ERROR USDT NULL ===")
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        print("\n1. Verificando cuentas con saldo_usdt NULL...")
        
        cursor.execute("SELECT COUNT(*) FROM cuentas WHERE saldo_usdt IS NULL")
        cuentas_null = cursor.fetchone()[0]
        
        if cuentas_null > 0:
            print(f"   ⚠️  Encontradas {cuentas_null} cuentas con saldo_usdt NULL")
            print("   🔧 Actualizando a 0.0...")
            
            cursor.execute("UPDATE cuentas SET saldo_usdt = 0.0 WHERE saldo_usdt IS NULL")
            conn.commit()
            
            print("   ✅ Cuentas actualizadas")
        else:
            print("   ✅ No hay cuentas con saldo_usdt NULL")
        
        print("\n2. Verificando correcciones en el código...")
        
        # Leer el controlador
        with open('controllers/divisas.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        # Verificar correcciones aplicadas
        correcciones = [
            ('Manejo NULL en compra USDT', 'saldo_usdt_actual = cuenta.saldo_usdt if cuenta.saldo_usdt is not None else Decimal(\'0.0\')'),
            ('Manejo NULL en venta USDT', 'saldo_disponible = cuenta.saldo_usdt if cuenta.saldo_usdt is not None else Decimal(\'0.0\')'),
            ('Validación USDT compra', 'elif moneda_destino == \'USDT\':'),
            ('Validación USDT venta', 'elif moneda_origen == \'USDT\':')
        ]
        
        correcciones_aplicadas = 0
        for nombre, codigo in correcciones:
            if codigo in controller_content:
                correcciones_aplicadas += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Correcciones aplicadas: {correcciones_aplicadas}/{len(correcciones)}")
        
        print("\n3. Verificando estructura de cuentas...")
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(saldo_usdt) as con_usdt,
                AVG(saldo_usdt) as promedio_usdt,
                MAX(saldo_usdt) as max_usdt
            FROM cuentas 
            WHERE estado = 'activa'
        """)
        
        stats = cursor.fetchone()
        
        print(f"   📊 Total cuentas activas: {stats[0]}")
        print(f"   📊 Cuentas con saldo USDT: {stats[1]}")
        print(f"   📊 Promedio saldo USDT: {stats[2]:.2f}" if stats[2] else "   📊 Promedio saldo USDT: 0.00")
        print(f"   📊 Máximo saldo USDT: {stats[3]:.2f}" if stats[3] else "   📊 Máximo saldo USDT: 0.00")
        
        print("\n4. Probando simulación de compra USDT...")
        
        # Buscar una cuenta con saldo VES suficiente
        cursor.execute("""
            SELECT numero_cuenta, saldo_ves, saldo_usdt
            FROM cuentas 
            WHERE estado = 'activa' AND saldo_ves > 2000
            ORDER BY saldo_ves DESC
            LIMIT 1
        """)
        
        cuenta_test = cursor.fetchone()
        
        if cuenta_test:
            print(f"   ✅ Cuenta de prueba: {cuenta_test[0]}")
            print(f"      Saldo VES: {cuenta_test[1]:.2f}")
            print(f"      Saldo USDT: {cuenta_test[2]:.2f}" if cuenta_test[2] is not None else "      Saldo USDT: 0.00")
            
            # Simular operación
            cantidad_usdt = 10.0
            tasa_usdt = 212.46
            ves_necesarios = cantidad_usdt * tasa_usdt
            
            print(f"   📊 Simulación: Comprar {cantidad_usdt} USDT")
            print(f"      VES necesarios: {ves_necesarios:.2f}")
            print(f"      Fondos suficientes: {'✅ Sí' if cuenta_test[1] >= ves_necesarios else '❌ No'}")
            
            if cuenta_test[1] >= ves_necesarios:
                nuevo_saldo_ves = cuenta_test[1] - ves_necesarios
                saldo_usdt_actual = cuenta_test[2] if cuenta_test[2] is not None else 0.0
                nuevo_saldo_usdt = saldo_usdt_actual + cantidad_usdt
                
                print(f"      Nuevo saldo VES: {nuevo_saldo_ves:.2f}")
                print(f"      Nuevo saldo USDT: {nuevo_saldo_usdt:.2f}")
                print("   🎯 La operación debería funcionar correctamente")
        else:
            print("   ⚠️  No hay cuentas con fondos suficientes para la prueba")
        
        conn.close()
        
        print("\n5. Instrucciones para probar:")
        print("   1. Reiniciar web2py para cargar los cambios")
        print("   2. Ir a la página de compra de divisas")
        print("   3. Seleccionar USDT como moneda destino")
        print("   4. Ingresar una cantidad pequeña (ej: 1 USDT)")
        print("   5. Confirmar la compra")
        print("   6. Verificar que no aparezca el error de NoneType")
        
        return correcciones_aplicadas == len(correcciones) and cuentas_null == 0
        
    except Exception as e:
        print(f"❌ Error durante la corrección: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = fix_usdt_null_error()
    print(f"\n{'='*60}")
    if resultado:
        print("🎉 ERROR USDT NULL CORREGIDO - Debería funcionar ahora")
    else:
        print("🔧 CORRECCIÓN INCOMPLETA - Revisar problemas")
    print(f"{'='*60}")