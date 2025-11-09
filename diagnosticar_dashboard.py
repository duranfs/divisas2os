#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para diagnosticar por qué no se ven las tasas en el dashboard
"""

import sqlite3
import sys

def diagnosticar_dashboard():
    """Diagnosticar problemas del dashboard"""
    print("🔍 DIAGNÓSTICO DEL DASHBOARD")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect("databases/storage.sqlite")
        cursor = conn.cursor()
        
        # 1. Verificar tasas en BD
        print("📊 1. VERIFICANDO TASAS EN BASE DE DATOS")
        print("-" * 40)
        
        cursor.execute("SELECT COUNT(*) FROM tasas_cambio")
        total_tasas = cursor.fetchone()[0]
        print(f"   Total de tasas en BD: {total_tasas}")
        
        cursor.execute("SELECT COUNT(*) FROM tasas_cambio WHERE activa = 1")
        tasas_activas = cursor.fetchone()[0]
        print(f"   Tasas activas: {tasas_activas}")
        
        if tasas_activas == 0:
            print("   ❌ PROBLEMA: No hay tasas activas")
            
            # Activar la más reciente
            cursor.execute("""
                UPDATE tasas_cambio SET activa = 0;
                UPDATE tasas_cambio SET activa = 1 
                WHERE id = (SELECT id FROM tasas_cambio ORDER BY fecha DESC, hora DESC LIMIT 1)
            """)
            conn.commit()
            print("   🔧 Activada la tasa más reciente")
        
        # Mostrar tasa activa
        cursor.execute("""
            SELECT id, fecha, hora, usd_ves, eur_ves, usdt_ves, fuente, activa
            FROM tasas_cambio 
            WHERE activa = 1
            LIMIT 1
        """)
        
        tasa_activa = cursor.fetchone()
        
        if tasa_activa:
            print(f"\n   ✅ Tasa activa encontrada:")
            print(f"      ID: {tasa_activa[0]}")
            print(f"      Fecha: {tasa_activa[1]} {tasa_activa[2]}")
            print(f"      USD/VES: {tasa_activa[3]}")
            print(f"      EUR/VES: {tasa_activa[4]}")
            print(f"      USDT/VES: {tasa_activa[5]}")
            print(f"      Fuente: {tasa_activa[6]}")
            
            # Verificar campos NULL
            if tasa_activa[3] is None:
                print("      ❌ USD/VES es NULL")
            if tasa_activa[4] is None:
                print("      ❌ EUR/VES es NULL")
            if tasa_activa[5] is None:
                print("      ❌ USDT/VES es NULL")
        else:
            print("   ❌ No hay tasa activa")
        
        # 2. Simular función obtener_tasas_actuales()
        print(f"\n📡 2. SIMULANDO obtener_tasas_actuales()")
        print("-" * 40)
        
        cursor.execute("""
            SELECT * FROM tasas_cambio 
            WHERE activa = 1
            ORDER BY fecha DESC, hora DESC 
            LIMIT 1
        """)
        
        tasa_simulada = cursor.fetchone()
        
        if tasa_simulada:
            print("   ✅ Función obtener_tasas_actuales() debería funcionar")
            print(f"   Retornaría: ID {tasa_simulada[0]} con tasas USD={tasa_simulada[3]}, EUR={tasa_simulada[4]}, USDT={tasa_simulada[5]}")
        else:
            print("   ❌ Función obtener_tasas_actuales() retornaría None")
        
        # 3. Verificar dashboard público
        print(f"\n🌐 3. VERIFICANDO DASHBOARD PÚBLICO")
        print("-" * 40)
        
        # Simular la función index() para usuarios no autenticados
        if tasa_activa:
            print("   ✅ Dashboard público debería mostrar:")
            print(f"      USD/VES: {tasa_activa[3]:,.4f}")
            print(f"      EUR/VES: {tasa_activa[4]:,.4f}")
            print(f"      USDT/VES: {tasa_activa[5]:,.4f}")
        else:
            print("   ❌ Dashboard público mostraría 'No hay tasas disponibles'")
        
        # 4. Verificar dashboard de cliente
        print(f"\n👤 4. VERIFICANDO DASHBOARD DE CLIENTE")
        print("-" * 40)
        
        # Buscar un cliente
        cursor.execute("""
            SELECT c.id, u.first_name, u.last_name
            FROM clientes c
            JOIN auth_user u ON c.user_id = u.id
            LIMIT 1
        """)
        
        cliente = cursor.fetchone()
        
        if cliente:
            cliente_id = cliente[0]
            nombre = f"{cliente[1]} {cliente[2]}"
            print(f"   👤 Cliente de prueba: {nombre} (ID: {cliente_id})")
            
            # Obtener cuentas del cliente
            cursor.execute("SELECT COUNT(*) FROM cuentas WHERE cliente_id = ?", (cliente_id,))
            num_cuentas = cursor.fetchone()[0]
            print(f"   💳 Número de cuentas: {num_cuentas}")
            
            if num_cuentas > 0:
                # Calcular saldos
                cursor.execute("""
                    SELECT 
                        COALESCE(SUM(saldo_ves), 0) as total_ves,
                        COALESCE(SUM(saldo_usd), 0) as total_usd,
                        COALESCE(SUM(saldo_eur), 0) as total_eur,
                        COALESCE(SUM(saldo_usdt), 0) as total_usdt
                    FROM cuentas 
                    WHERE cliente_id = ?
                """, (cliente_id,))
                
                saldos = cursor.fetchone()
                print(f"   💰 Saldos: VES={saldos[0]}, USD={saldos[1]}, EUR={saldos[2]}, USDT={saldos[3]}")
                
                # Verificar si se mostrarían las tasas
                if tasa_activa:
                    print("   ✅ Dashboard de cliente debería mostrar tasas correctamente")
                else:
                    print("   ❌ Dashboard de cliente mostraría 'No hay tasas disponibles'")
            else:
                print("   ⚠️ Cliente no tiene cuentas")
        else:
            print("   ❌ No hay clientes en el sistema")
        
        # 5. Verificar posibles errores
        print(f"\n🔧 5. VERIFICANDO POSIBLES ERRORES")
        print("-" * 40)
        
        # Verificar si hay errores de formato en las tasas
        cursor.execute("SELECT id, usd_ves, eur_ves, usdt_ves FROM tasas_cambio WHERE activa = 1")
        tasa_check = cursor.fetchone()
        
        if tasa_check:
            try:
                usd_formatted = "{:,.4f}".format(float(tasa_check[1])) if tasa_check[1] else 'N/A'
                eur_formatted = "{:,.4f}".format(float(tasa_check[2])) if tasa_check[2] else 'N/A'
                usdt_formatted = "{:,.4f}".format(float(tasa_check[3])) if tasa_check[3] else 'N/A'
                
                print("   ✅ Formato de tasas correcto:")
                print(f"      USD: {usd_formatted}")
                print(f"      EUR: {eur_formatted}")
                print(f"      USDT: {usdt_formatted}")
                
            except Exception as e:
                print(f"   ❌ Error de formato: {e}")
        
        conn.close()
        
        # 6. Recomendaciones
        print(f"\n" + "=" * 60)
        print("📋 RECOMENDACIONES")
        print("=" * 60)
        
        if tasas_activas == 0:
            print("1. ✅ Se activó automáticamente la tasa más reciente")
        
        print("2. 🌐 Acceder al dashboard en: http://127.0.0.1:8000/divisas2os")
        print("3. 🔄 Si no se ven las tasas, verificar:")
        print("   • Que web2py esté ejecutándose")
        print("   • Que no haya errores en el log de web2py")
        print("   • Que la función obtener_tasas_actuales() funcione")
        
        print("\n4. 🧪 Para probar manualmente:")
        print("   • Dashboard público: Acceder sin login")
        print("   • Dashboard cliente: Login con credenciales de cliente")
        print("   • Dashboard admin: Login con credenciales de admin")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el diagnóstico: {e}")
        return False

if __name__ == '__main__':
    diagnosticar_dashboard()