#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Diagnóstico del sistema de ventas de divisas
"""

import sqlite3

def diagnosticar_ventas():
    """
    Diagnóstica el sistema de ventas de divisas
    """
    print("=== DIAGNÓSTICO DEL SISTEMA DE VENTAS ===")
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        print("\n1. Verificando transacciones de venta...")
        
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
            WHERE tipo_operacion = 'venta'
            ORDER BY fecha_transaccion DESC
            LIMIT 10
        """)
        
        ventas = cursor.fetchall()
        
        if ventas:
            print(f"   📊 Ventas encontradas: {len(ventas)}")
            print("   " + "-" * 100)
            print("   ID | Tipo  | Origen | Destino | Monto Orig | Monto Dest | Tasa   | Comprobante | Estado")
            print("   " + "-" * 100)
            
            for venta in ventas:
                print(f"   {venta[0]:2d} | {venta[1]:5s} | {venta[2]:6s} | {venta[3]:7s} | {venta[4]:10.2f} | {venta[5]:10.2f} | {venta[6]:6.2f} | {venta[7]:11s} | {venta[8]}")
        else:
            print("   ⚠️  No hay transacciones de venta registradas")
        
        print("\n2. Verificando función vender() en el controlador...")
        
        # Leer el controlador
        with open('controllers/divisas.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        # Verificar elementos clave de la función vender
        elementos_vender = [
            ('Función vender existe', 'def vender():'),
            ('Llama a procesar_venta_divisa', 'resultado = procesar_venta_divisa()'),
            ('Maneja resultado exitoso', "resultado['success']"),
            ('Maneja errores', "resultado['error']"),
            ('Logging de venta', 'Procesando venta para usuario'),
            ('Obtiene tasas actuales', 'tasas = obtener_tasas_actuales()')
        ]
        
        elementos_encontrados = 0
        for nombre, elemento in elementos_vender:
            if elemento in controller_content:
                elementos_encontrados += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Elementos de vender(): {elementos_encontrados}/{len(elementos_vender)}")
        
        print("\n3. Verificando función procesar_venta_divisa()...")
        
        # Verificar elementos de procesar_venta_divisa
        elementos_procesar = [
            ('Función procesar_venta_divisa existe', 'def procesar_venta_divisa():'),
            ('Validación de moneda USDT', "elif moneda_origen == 'USDT':"),
            ('Manejo de saldo USDT nulo', 'saldo_usdt_actual = cuenta.saldo_usdt if cuenta.saldo_usdt is not None'),
            ('Actualización saldo USDT', 'nuevo_saldo_usdt = saldo_usdt_actual - monto_origen'),
            ('Validación fondos USDT', 'saldo_disponible = cuenta.saldo_usdt if cuenta.saldo_usdt is not None'),
            ('Registro en transacciones', 'db.transacciones.insert('),
            ('Generación de comprobante', 'generar_comprobante_unico(\'VENT\')')
        ]
        
        procesar_encontrados = 0
        for nombre, elemento in elementos_procesar:
            if elemento in controller_content:
                procesar_encontrados += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Elementos de procesar_venta_divisa(): {procesar_encontrados}/{len(elementos_procesar)}")
        
        print("\n4. Verificando cuentas con saldos para vender...")
        
        cursor.execute("""
            SELECT 
                numero_cuenta,
                saldo_usd,
                saldo_eur,
                saldo_usdt
            FROM cuentas 
            WHERE estado = 'activa' 
            AND (saldo_usd > 0 OR saldo_eur > 0 OR saldo_usdt > 0)
            ORDER BY (saldo_usd + saldo_eur + saldo_usdt) DESC
            LIMIT 5
        """)
        
        cuentas_con_divisas = cursor.fetchall()
        
        if cuentas_con_divisas:
            print("   📊 Cuentas con divisas para vender:")
            print("   " + "-" * 60)
            print("   Cuenta               | USD      | EUR      | USDT")
            print("   " + "-" * 60)
            
            for cuenta in cuentas_con_divisas:
                print(f"   {cuenta[0]} | {cuenta[1]:8.2f} | {cuenta[2]:8.2f} | {cuenta[3]:8.2f}")
        else:
            print("   ⚠️  No hay cuentas con divisas para vender")
        
        print("\n5. Comparando compras vs ventas...")
        
        cursor.execute("SELECT tipo_operacion, COUNT(*) FROM transacciones GROUP BY tipo_operacion")
        tipos_transacciones = cursor.fetchall()
        
        compras = 0
        ventas_count = 0
        
        for tipo, count in tipos_transacciones:
            if tipo == 'compra':
                compras = count
            elif tipo == 'venta':
                ventas_count = count
            print(f"   📊 {tipo.capitalize()}: {count}")
        
        if compras > 0 and ventas_count == 0:
            print("   ⚠️  Hay compras pero no ventas - posible problema en ventas")
        elif compras > 0 and ventas_count > 0:
            print("   ✅ Tanto compras como ventas están funcionando")
        else:
            print("   ⚠️  No hay suficientes transacciones para comparar")
        
        conn.close()
        
        print("\n6. Resumen del diagnóstico:")
        
        problemas_detectados = []
        
        if elementos_encontrados < len(elementos_vender):
            problemas_detectados.append("Función vender() incompleta")
        
        if procesar_encontrados < len(elementos_procesar):
            problemas_detectados.append("Función procesar_venta_divisa() incompleta")
        
        if not cuentas_con_divisas:
            problemas_detectados.append("No hay cuentas con divisas para vender")
        
        if compras > 0 and ventas_count == 0:
            problemas_detectados.append("Las ventas no se están registrando")
        
        if problemas_detectados:
            print("   ⚠️  Problemas detectados:")
            for i, problema in enumerate(problemas_detectados, 1):
                print(f"      {i}. {problema}")
        else:
            print("   ✅ No se detectaron problemas obvios")
        
        print("\n7. Instrucciones para probar ventas:")
        print("   1. Reiniciar web2py si está ejecutándose")
        print("   2. Ir a: http://127.0.0.1:8000/divisas2os/divisas/vender")
        print("   3. Seleccionar cuenta con saldo en USD/EUR/USDT")
        print("   4. Seleccionar moneda a vender")
        print("   5. Ingresar cantidad a vender")
        print("   6. Confirmar la venta")
        print("   7. Verificar que se registre la transacción")
        
        return len(problemas_detectados) == 0
        
    except Exception as e:
        print(f"❌ Error durante el diagnóstico: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = diagnosticar_ventas()
    print(f"\n{'='*60}")
    if resultado:
        print("🎉 SISTEMA DE VENTAS FUNCIONANDO CORRECTAMENTE")
    else:
        print("🔧 PROBLEMAS DETECTADOS EN VENTAS - Revisar arriba")
    print(f"{'='*60}")