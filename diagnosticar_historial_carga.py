#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Diagnosticar por qué el historial se queda cargando
"""

import sqlite3
from datetime import datetime

def diagnosticar():
    """Diagnosticar el problema del historial"""
    
    print("🔍 DIAGNÓSTICO: HISTORIAL SE QUEDA CARGANDO")
    print("="*70)
    
    try:
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        # 1. Verificar cantidad de transacciones
        print("\n📊 CANTIDAD DE TRANSACCIONES:")
        cursor.execute("SELECT COUNT(*) FROM transacciones")
        total = cursor.fetchone()[0]
        print(f"   Total de transacciones: {total}")
        
        if total > 1000:
            print(f"   ⚠️  PROBLEMA: Hay {total} transacciones, puede ser lento")
        
        # 2. Verificar si hay índices
        print("\n🔍 ÍNDICES EN LA TABLA transacciones:")
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='index' AND tbl_name='transacciones'
        """)
        indices = cursor.fetchall()
        
        if indices:
            for idx in indices:
                print(f"   ✅ {idx[0]}")
        else:
            print("   ⚠️  NO HAY ÍNDICES - Esto puede causar lentitud")
        
        # 3. Probar la consulta problemática
        print("\n🧪 PROBANDO CONSULTA DEL HISTORIAL:")
        print("   Ejecutando consulta con JOIN...")
        
        inicio = datetime.now()
        
        cursor.execute("""
            SELECT 
                t.*,
                c.numero_cuenta,
                cl.first_name,
                cl.last_name
            FROM transacciones t
            JOIN cuentas c ON t.cuenta_id = c.id
            JOIN clientes cl ON c.cliente_id = cl.id
            ORDER BY t.fecha_transaccion DESC
            LIMIT 50
        """)
        
        resultados = cursor.fetchall()
        fin = datetime.now()
        tiempo = (fin - inicio).total_seconds()
        
        print(f"   ✅ Consulta completada en {tiempo:.2f} segundos")
        print(f"   Registros obtenidos: {len(resultados)}")
        
        if tiempo > 2:
            print(f"   ⚠️  LENTO: La consulta tarda {tiempo:.2f} segundos")
            print("   Recomendación: Agregar índices")
        
        # 4. Verificar estructura de tablas
        print("\n📋 ESTRUCTURA DE TABLAS:")
        
        # Transacciones
        cursor.execute("PRAGMA table_info(transacciones)")
        campos_trans = cursor.fetchall()
        print(f"   transacciones: {len(campos_trans)} campos")
        
        # Cuentas
        cursor.execute("PRAGMA table_info(cuentas)")
        campos_cuentas = cursor.fetchall()
        print(f"   cuentas: {len(campos_cuentas)} campos")
        
        # Clientes
        cursor.execute("PRAGMA table_info(clientes)")
        campos_clientes = cursor.fetchall()
        print(f"   clientes: {len(campos_clientes)} campos")
        
        # 5. Verificar si hay transacciones sin cuenta o cliente
        print("\n🔍 VERIFICANDO INTEGRIDAD:")
        
        cursor.execute("""
            SELECT COUNT(*) FROM transacciones t
            LEFT JOIN cuentas c ON t.cuenta_id = c.id
            WHERE c.id IS NULL
        """)
        sin_cuenta = cursor.fetchone()[0]
        
        if sin_cuenta > 0:
            print(f"   ⚠️  {sin_cuenta} transacciones sin cuenta válida")
        else:
            print("   ✅ Todas las transacciones tienen cuenta válida")
        
        cursor.execute("""
            SELECT COUNT(*) FROM cuentas c
            LEFT JOIN clientes cl ON c.cliente_id = cl.id
            WHERE cl.id IS NULL
        """)
        sin_cliente = cursor.fetchone()[0]
        
        if sin_cliente > 0:
            print(f"   ⚠️  {sin_cliente} cuentas sin cliente válido")
        else:
            print("   ✅ Todas las cuentas tienen cliente válido")
        
        conn.close()
        
        # 6. Solución
        print("\n" + "="*70)
        print("🔧 SOLUCIÓN:")
        print("="*70)
        
        if total > 500 and not indices:
            print()
            print("El problema es la falta de índices en la tabla transacciones.")
            print()
            print("Voy a crear índices para mejorar el rendimiento...")
            
            conn = sqlite3.connect('databases/storage.sqlite')
            cursor = conn.cursor()
            
            # Crear índices
            try:
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_transacciones_cuenta_id 
                    ON transacciones(cuenta_id)
                """)
                print("   ✅ Índice en cuenta_id creado")
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_transacciones_fecha 
                    ON transacciones(fecha_transaccion)
                """)
                print("   ✅ Índice en fecha_transaccion creado")
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_cuentas_cliente_id 
                    ON cuentas(cliente_id)
                """)
                print("   ✅ Índice en cliente_id creado")
                
                conn.commit()
                conn.close()
                
                print()
                print("✅ ÍNDICES CREADOS")
                print("   El historial debería cargar mucho más rápido ahora")
                
            except Exception as e:
                print(f"   ❌ Error creando índices: {str(e)}")
        
        elif tiempo > 2:
            print()
            print(f"La consulta tarda {tiempo:.2f} segundos.")
            print("Esto puede ser normal si hay muchas transacciones.")
        else:
            print()
            print("✅ La consulta es rápida, el problema puede ser otro:")
            print("   - Verifica la consola del navegador (F12)")
            print("   - Revisa los logs de web2py")
            print("   - Verifica que la vista exista")
        
        print()
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    diagnosticar()
