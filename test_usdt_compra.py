#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para probar las compras de USDT
"""

import sqlite3

def test_usdt_compra():
    """
    Prueba las funcionalidades de USDT
    """
    print("=== PRUEBA DE COMPRA USDT ===")
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        print("\n1. Verificando tasas de USDT...")
        
        cursor.execute("""
            SELECT fecha, usd_ves, eur_ves, usdt_ves, fuente, activa
            FROM tasas_cambio 
            WHERE activa = 1
            ORDER BY fecha DESC, hora DESC
            LIMIT 1
        """)
        
        tasa_activa = cursor.fetchone()
        
        if tasa_activa:
            print(f"   ✅ Tasa activa encontrada:")
            print(f"      Fecha: {tasa_activa[0]}")
            print(f"      USD/VES: {tasa_activa[1]}")
            print(f"      EUR/VES: {tasa_activa[2]}")
            print(f"      USDT/VES: {tasa_activa[3]}")
            print(f"      Fuente: {tasa_activa[4]}")
            
            if tasa_activa[3] is not None and tasa_activa[3] > 0:
                print("   ✅ Tasa de USDT válida")
            else:
                print("   ❌ Tasa de USDT inválida o nula")
        else:
            print("   ❌ No hay tasas activas")
        
        print("\n2. Verificando cuentas con saldo USDT...")
        
        cursor.execute("""
            SELECT 
                c.numero_cuenta,
                c.saldo_ves,
                c.saldo_usd,
                c.saldo_eur,
                c.saldo_usdt,
                cl.cedula,
                au.first_name,
                au.last_name
            FROM cuentas c
            JOIN clientes cl ON c.cliente_id = cl.id
            JOIN auth_user au ON cl.user_id = au.id
            WHERE c.estado = 'activa' AND c.saldo_usdt IS NOT NULL
            ORDER BY c.saldo_usdt DESC
            LIMIT 5
        """)
        
        cuentas_usdt = cursor.fetchall()
        
        if cuentas_usdt:
            print("   📊 Cuentas con saldo USDT:")
            print("   " + "-" * 90)
            print("   Cuenta               | VES        | USD      | EUR      | USDT     | Cliente")
            print("   " + "-" * 90)
            
            for cuenta in cuentas_usdt:
                usdt_saldo = cuenta[4] if cuenta[4] is not None else 0.0
                print(f"   {cuenta[0]} | {cuenta[1]:10.2f} | {cuenta[2]:8.2f} | {cuenta[3]:8.2f} | {usdt_saldo:8.2f} | {cuenta[6]} {cuenta[7]}")
        else:
            print("   ⚠️  No hay cuentas con saldo USDT")
        
        print("\n3. Verificando transacciones de USDT...")
        
        cursor.execute("""
            SELECT 
                id,
                tipo_operacion,
                moneda_origen,
                moneda_destino,
                monto_origen,
                monto_destino,
                tasa_aplicada,
                numero_comprobante,
                estado,
                fecha_transaccion
            FROM transacciones 
            WHERE moneda_origen = 'USDT' OR moneda_destino = 'USDT'
            ORDER BY fecha_transaccion DESC
            LIMIT 5
        """)
        
        transacciones_usdt = cursor.fetchall()
        
        if transacciones_usdt:
            print(f"   📊 Transacciones USDT encontradas: {len(transacciones_usdt)}")
            print("   " + "-" * 100)
            print("   ID | Tipo    | Origen | Destino | Monto Orig | Monto Dest | Tasa   | Comprobante | Estado")
            print("   " + "-" * 100)
            
            for txn in transacciones_usdt:
                print(f"   {txn[0]:2d} | {txn[1]:7s} | {txn[2]:6s} | {txn[3]:7s} | {txn[4]:10.2f} | {txn[5]:10.2f} | {txn[6]:6.2f} | {txn[7]:11s} | {txn[8]}")
        else:
            print("   ⚠️  No hay transacciones de USDT registradas")
        
        print("\n4. Verificando controlador de divisas...")
        
        # Leer el controlador para verificar las correcciones
        with open('controllers/divisas.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        correcciones_usdt = [
            ('Tasa USDT en obtener_tasas_actuales', "'usdt_ves': float(tasa_activa.usdt_ves)"),
            ('Validación USDT en compra', "elif moneda_destino == 'USDT':"),
            ('Validación USDT en venta', "elif moneda_origen == 'USDT':"),
            ('Actualización saldo USDT compra', 'nuevo_saldo_usdt = cuenta.saldo_usdt + monto_destino'),
            ('Actualización saldo USDT venta', 'nuevo_saldo_usdt = cuenta.saldo_usdt - monto_origen')
        ]
        
        correcciones_aplicadas = 0
        for nombre, codigo in correcciones_usdt:
            if codigo in controller_content:
                correcciones_aplicadas += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Correcciones USDT aplicadas: {correcciones_aplicadas}/{len(correcciones_usdt)}")
        
        print("\n5. Simulación de compra USDT...")
        
        if tasa_activa and tasa_activa[3] and tasa_activa[3] > 0:
            # Simular una compra de 10 USDT
            cantidad_usdt = 10.0
            tasa_usdt_ves = tasa_activa[3]
            monto_ves_necesario = cantidad_usdt * tasa_usdt_ves
            
            print(f"   📊 Simulación de compra:")
            print(f"      Cantidad USDT: {cantidad_usdt}")
            print(f"      Tasa USDT/VES: {tasa_usdt_ves}")
            print(f"      VES necesarios: {monto_ves_necesario:.2f}")
            
            # Buscar cuenta con suficiente saldo VES
            cursor.execute("""
                SELECT numero_cuenta, saldo_ves
                FROM cuentas 
                WHERE estado = 'activa' AND saldo_ves >= ?
                ORDER BY saldo_ves DESC
                LIMIT 1
            """, (monto_ves_necesario,))
            
            cuenta_suficiente = cursor.fetchone()
            
            if cuenta_suficiente:
                print(f"   ✅ Cuenta con fondos suficientes: {cuenta_suficiente[0]}")
                print(f"      Saldo VES: {cuenta_suficiente[1]:.2f}")
                print("   🎯 La compra de USDT debería funcionar")
            else:
                print("   ⚠️  No hay cuentas con fondos suficientes para la compra")
        
        conn.close()
        
        print("\n6. Instrucciones para probar USDT:")
        print("   1. Reiniciar web2py si está ejecutándose")
        print("   2. Ir a: http://127.0.0.1:8000/divisas2os/divisas/comprar")
        print("   3. Seleccionar USDT como moneda destino")
        print("   4. Ingresar cantidad de USDT a comprar")
        print("   5. Confirmar la compra")
        print("   6. Verificar que se registre la transacción")
        
        return correcciones_aplicadas == len(correcciones_usdt) and tasa_activa and tasa_activa[3] and tasa_activa[3] > 0
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = test_usdt_compra()
    print(f"\n{'='*60}")
    if resultado:
        print("🎉 USDT CONFIGURADO CORRECTAMENTE - Las compras deberían funcionar")
    else:
        print("🔧 PROBLEMA CON USDT - Revisar configuración")
    print(f"{'='*60}")