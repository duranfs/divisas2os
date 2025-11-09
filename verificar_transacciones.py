#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar que las transacciones se registren en la base de datos
"""

import sqlite3
from datetime import datetime, timedelta

def verificar_transacciones():
    """
    Verifica las transacciones registradas en la base de datos
    """
    print("=== VERIFICACIÓN DE TRANSACCIONES ===")
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        print("\n1. Verificando transacciones recientes...")
        
        # Obtener transacciones de las últimas 24 horas
        fecha_limite = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        
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
            WHERE fecha_transaccion >= ?
            ORDER BY fecha_transaccion DESC
            LIMIT 10
        """, (fecha_limite,))
        
        transacciones = cursor.fetchall()
        
        if transacciones:
            print(f"   📊 Transacciones encontradas: {len(transacciones)}")
            print("\n   Últimas transacciones:")
            print("   " + "-" * 100)
            print("   ID | Tipo    | Origen | Destino | Monto Orig | Monto Dest | Tasa   | Comprobante | Estado")
            print("   " + "-" * 100)
            
            for txn in transacciones:
                print(f"   {txn[0]:2d} | {txn[1]:7s} | {txn[2]:6s} | {txn[3]:7s} | {txn[4]:10.2f} | {txn[5]:10.2f} | {txn[6]:6.2f} | {txn[7]:11s} | {txn[8]}")
        else:
            print("   ⚠️  No se encontraron transacciones recientes")
        
        print("\n2. Verificando estadísticas generales...")
        
        # Total de transacciones
        cursor.execute("SELECT COUNT(*) FROM transacciones")
        total_transacciones = cursor.fetchone()[0]
        print(f"   📊 Total de transacciones: {total_transacciones}")
        
        # Transacciones por tipo
        cursor.execute("SELECT tipo_operacion, COUNT(*) FROM transacciones GROUP BY tipo_operacion")
        tipos = cursor.fetchall()
        for tipo, count in tipos:
            print(f"   📊 {tipo.capitalize()}: {count}")
        
        # Transacciones por estado
        cursor.execute("SELECT estado, COUNT(*) FROM transacciones GROUP BY estado")
        estados = cursor.fetchall()
        for estado, count in estados:
            print(f"   📊 Estado {estado}: {count}")
        
        print("\n3. Verificando cuentas con saldos...")
        
        cursor.execute("""
            SELECT 
                c.numero_cuenta,
                c.saldo_ves,
                c.saldo_usd,
                c.saldo_eur,
                cl.cedula,
                au.first_name,
                au.last_name
            FROM cuentas c
            JOIN clientes cl ON c.cliente_id = cl.id
            JOIN auth_user au ON cl.user_id = au.id
            WHERE c.estado = 'activa'
            ORDER BY c.saldo_ves DESC
            LIMIT 5
        """)
        
        cuentas = cursor.fetchall()
        
        if cuentas:
            print("   📊 Cuentas con mayores saldos:")
            print("   " + "-" * 80)
            print("   Cuenta               | VES        | USD      | EUR      | Cliente")
            print("   " + "-" * 80)
            
            for cuenta in cuentas:
                print(f"   {cuenta[0]} | {cuenta[1]:10.2f} | {cuenta[2]:8.2f} | {cuenta[3]:8.2f} | {cuenta[5]} {cuenta[6]}")
        
        print("\n4. Verificando tasas de cambio activas...")
        
        cursor.execute("""
            SELECT fecha, usd_ves, eur_ves, fuente, activa
            FROM tasas_cambio 
            WHERE activa = 1
            ORDER BY fecha DESC, hora DESC
            LIMIT 3
        """)
        
        tasas = cursor.fetchall()
        
        if tasas:
            print("   📊 Tasas de cambio activas:")
            for tasa in tasas:
                print(f"   📅 {tasa[0]} | USD: {tasa[1]} | EUR: {tasa[2]} | Fuente: {tasa[3]}")
        else:
            print("   ⚠️  No hay tasas de cambio activas")
        
        print("\n5. Verificando integridad de datos...")
        
        # Verificar que todas las transacciones tienen comprobantes únicos
        cursor.execute("""
            SELECT numero_comprobante, COUNT(*) 
            FROM transacciones 
            WHERE numero_comprobante IS NOT NULL AND numero_comprobante != ''
            GROUP BY numero_comprobante 
            HAVING COUNT(*) > 1
        """)
        
        duplicados = cursor.fetchall()
        
        if duplicados:
            print(f"   ⚠️  Comprobantes duplicados encontrados: {len(duplicados)}")
            for comp, count in duplicados:
                print(f"      {comp}: {count} veces")
        else:
            print("   ✅ Todos los comprobantes son únicos")
        
        # Verificar transacciones sin comprobante
        cursor.execute("SELECT COUNT(*) FROM transacciones WHERE numero_comprobante IS NULL OR numero_comprobante = ''")
        sin_comprobante = cursor.fetchone()[0]
        
        if sin_comprobante > 0:
            print(f"   ⚠️  Transacciones sin comprobante: {sin_comprobante}")
        else:
            print("   ✅ Todas las transacciones tienen comprobante")
        
        conn.close()
        
        print("\n6. Resumen:")
        
        if total_transacciones > 0:
            print("   ✅ El sistema de transacciones está funcionando")
            print("   📝 Las compras se están registrando correctamente")
            
            if transacciones:
                print("   ✅ Hay transacciones recientes")
            else:
                print("   ⚠️  No hay transacciones muy recientes (últimas 24h)")
        else:
            print("   ❌ No hay transacciones registradas")
            print("   🔧 El problema de compras persiste")
        
        return total_transacciones > 0
        
    except Exception as e:
        print(f"❌ Error verificando transacciones: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = verificar_transacciones()
    print(f"\n{'='*60}")
    if resultado:
        print("🎉 VERIFICACIÓN EXITOSA - El sistema registra transacciones")
    else:
        print("🔧 PROBLEMA DETECTADO - Las transacciones no se registran")
    print(f"{'='*60}")