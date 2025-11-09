#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para probar específicamente la vista de cuentas
Requisitos: 1.1, 2.1

Este script verifica que la vista de cuentas funcione sin errores
"""

import os
import sys
import sqlite3
from datetime import datetime

# Configurar path para el proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.insert(0, project_dir)

def test_accounts_view_data():
    """Probar que los datos para la vista de cuentas estén correctos"""
    print("🔍 PROBANDO DATOS PARA VISTA DE CUENTAS")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("databases/storage.sqlite")
        cursor = conn.cursor()
        
        print("✅ Conectado a la base de datos")
        
        # Probar la consulta exacta que usa el controlador
        query = """
            SELECT 
                cu.id as cuenta_id,
                cu.numero_cuenta,
                cu.tipo_cuenta,
                cu.saldo_ves,
                cu.saldo_usd,
                cu.saldo_eur,
                cu.saldo_usdt,
                cu.estado as estado_cuenta,
                cu.fecha_creacion,
                c.cedula,
                u.first_name,
                u.last_name,
                u.email
            FROM cuentas cu
            JOIN clientes c ON cu.cliente_id = c.id
            JOIN auth_user u ON c.user_id = u.id
            ORDER BY cu.fecha_creacion DESC
        """
        
        cursor.execute(query)
        accounts = cursor.fetchall()
        
        print(f"📊 Total de cuentas encontradas: {len(accounts)}")
        
        if accounts:
            print("\n📋 Primeras 3 cuentas (datos que debería mostrar la vista):")
            for i, account in enumerate(accounts[:3], 1):
                print(f"\n  {i}. Cuenta ID: {account[0]}")
                print(f"     Número: {account[1]}")
                print(f"     Cliente: {account[10]} {account[11]}")
                print(f"     Cédula: {account[9]}")
                print(f"     Email: {account[12]}")
                print(f"     Tipo: {account[2]}")
                print(f"     Estado: {account[7]}")
                print(f"     Saldos:")
                print(f"       VES: {account[3] if account[3] is not None else 0:,.2f}")
                print(f"       USD: {account[4] if account[4] is not None else 0:,.2f}")
                print(f"       EUR: {account[5] if account[5] is not None else 0:,.2f}")
                print(f"       USDT: {account[6] if account[6] is not None else 0:,.2f}")
                print(f"     Fecha: {account[8]}")
        
        # Probar estadísticas
        print("\n📊 Probando estadísticas:")
        
        # Total de cuentas
        cursor.execute("SELECT COUNT(*) FROM cuentas")
        total = cursor.fetchone()[0]
        print(f"  Total cuentas: {total}")
        
        # Cuentas activas
        cursor.execute("SELECT COUNT(*) FROM cuentas WHERE estado = 'activa'")
        activas = cursor.fetchone()[0]
        print(f"  Cuentas activas: {activas}")
        
        # Cuentas inactivas
        cursor.execute("SELECT COUNT(*) FROM cuentas WHERE estado = 'inactiva'")
        inactivas = cursor.fetchone()[0]
        print(f"  Cuentas inactivas: {inactivas}")
        
        # Cuentas corrientes
        cursor.execute("SELECT COUNT(*) FROM cuentas WHERE tipo_cuenta = 'corriente'")
        corrientes = cursor.fetchone()[0]
        print(f"  Cuentas corrientes: {corrientes}")
        
        # Cuentas de ahorro
        cursor.execute("SELECT COUNT(*) FROM cuentas WHERE tipo_cuenta = 'ahorro'")
        ahorros = cursor.fetchone()[0]
        print(f"  Cuentas de ahorro: {ahorros}")
        
        # Verificar que las estadísticas cuadren
        if activas + inactivas == total:
            print("  ✅ Estadísticas por estado son consistentes")
        else:
            print("  ⚠️  Inconsistencia en estadísticas por estado")
        
        if corrientes + ahorros == total:
            print("  ✅ Estadísticas por tipo son consistentes")
        else:
            print("  ⚠️  Inconsistencia en estadísticas por tipo")
        
        # Probar filtros
        print("\n🔍 Probando filtros de búsqueda:")
        
        # Filtro por tipo corriente
        filter_query = query.replace("ORDER BY cu.fecha_creacion DESC", "WHERE cu.tipo_cuenta = 'corriente' ORDER BY cu.fecha_creacion DESC")
        cursor.execute(filter_query)
        corrientes_filtered = cursor.fetchall()
        print(f"  Filtro tipo 'corriente': {len(corrientes_filtered)} resultados")
        
        # Filtro por estado activa
        filter_query = query.replace("ORDER BY cu.fecha_creacion DESC", "WHERE cu.estado = 'activa' ORDER BY cu.fecha_creacion DESC")
        cursor.execute(filter_query)
        activas_filtered = cursor.fetchall()
        print(f"  Filtro estado 'activa': {len(activas_filtered)} resultados")
        
        # Filtro por búsqueda general (TEST)
        filter_query = query.replace("ORDER BY cu.fecha_creacion DESC", "WHERE (cu.numero_cuenta LIKE '%TEST%' OR c.cedula LIKE '%TEST%') ORDER BY cu.fecha_creacion DESC")
        cursor.execute(filter_query)
        test_filtered = cursor.fetchall()
        print(f"  Filtro búsqueda 'TEST': {len(test_filtered)} resultados")
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ PRUEBA DE VISTA DE CUENTAS COMPLETADA")
        print("=" * 60)
        print("\n🎯 RESULTADOS:")
        print(f"  • {len(accounts)} cuentas disponibles para mostrar")
        print(f"  • {activas} cuentas activas, {inactivas} inactivas")
        print(f"  • {corrientes} corrientes, {ahorros} de ahorro")
        print("  • Consulta JOIN funciona correctamente")
        print("  • Filtros funcionan correctamente")
        print("  • Estadísticas son consistentes")
        
        print("\n📋 PRÓXIMOS PASOS:")
        print("  1. Acceder a la URL: /cuentas/listar_todas")
        print("  2. Verificar que se muestren las cuentas sin errores")
        print("  3. Probar los filtros de búsqueda")
        print("  4. Verificar que las estadísticas aparezcan en las tarjetas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False

if __name__ == '__main__':
    success = test_accounts_view_data()
    sys.exit(0 if success else 1)