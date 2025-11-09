#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para debuggear específicamente por qué no aparecen las tasas en el dashboard
"""

import sqlite3
import sys

def debug_tasas_dashboard():
    """Debuggear el problema de las tasas en el dashboard"""
    print("🔍 DEBUG: TASAS EN DASHBOARD ADMINISTRATIVO")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect("databases/storage.sqlite")
        cursor = conn.cursor()
        
        # 1. Verificar tasas en BD
        print("📊 1. VERIFICANDO TASAS EN BASE DE DATOS")
        print("-" * 40)
        
        cursor.execute("""
            SELECT id, fecha, hora, usd_ves, eur_ves, usdt_ves, fuente, activa
            FROM tasas_cambio 
            ORDER BY fecha DESC, hora DESC
        """)
        
        todas_tasas = cursor.fetchall()
        
        print(f"   Total de tasas en BD: {len(todas_tasas)}")
        
        for tasa in todas_tasas:
            activa_str = "🟢 ACTIVA" if tasa[7] else "⚪ Inactiva"
            print(f"   ID {tasa[0]}: {tasa[1]} {tasa[2]} - {activa_str}")
            print(f"      USD: {tasa[3]}, EUR: {tasa[4]}, USDT: {tasa[5]}")
        
        # 2. Simular obtener_tasas_actuales()
        print(f"\n📡 2. SIMULANDO obtener_tasas_actuales()")
        print("-" * 40)
        
        cursor.execute("""
            SELECT id, fecha, hora, usd_ves, eur_ves, usdt_ves, fuente, activa
            FROM tasas_cambio 
            WHERE activa = 1
            ORDER BY fecha DESC, hora DESC 
            LIMIT 1
        """)
        
        tasa_activa = cursor.fetchone()
        
        if tasa_activa:
            print("   ✅ obtener_tasas_actuales() retornaría:")
            print(f"      ID: {tasa_activa[0]}")
            print(f"      Fecha: {tasa_activa[1]} {tasa_activa[2]}")
            print(f"      USD/VES: {tasa_activa[3]}")
            print(f"      EUR/VES: {tasa_activa[4]}")
            print(f"      USDT/VES: {tasa_activa[5]}")
            print(f"      Fuente: {tasa_activa[6]}")
            
            # Verificar que no sean None
            if tasa_activa[3] is None:
                print("      ❌ USD/VES es NULL")
            if tasa_activa[4] is None:
                print("      ❌ EUR/VES es NULL")
            if tasa_activa[5] is None:
                print("      ❌ USDT/VES es NULL")
                
        else:
            print("   ❌ obtener_tasas_actuales() retornaría None")
            print("   🔧 Activando la tasa más reciente...")
            
            # Activar la más reciente
            cursor.execute("UPDATE tasas_cambio SET activa = 0")
            cursor.execute("""
                UPDATE tasas_cambio SET activa = 1 
                WHERE id = (SELECT id FROM tasas_cambio ORDER BY fecha DESC, hora DESC LIMIT 1)
            """)
            conn.commit()
            
            # Verificar nuevamente
            cursor.execute("""
                SELECT id, fecha, hora, usd_ves, eur_ves, usdt_ves, fuente, activa
                FROM tasas_cambio 
                WHERE activa = 1
                LIMIT 1
            """)
            
            tasa_activa = cursor.fetchone()
            if tasa_activa:
                print("   ✅ Tasa activada correctamente")
            else:
                print("   ❌ No se pudo activar ninguna tasa")
        
        # 3. Simular dashboard_administrativo()
        print(f"\n🔧 3. SIMULANDO dashboard_administrativo()")
        print("-" * 40)
        
        if tasa_activa:
            print("   ✅ dashboard_administrativo() debería pasar:")
            print(f"      tasas_actuales = objeto con:")
            print(f"         .usd_ves = {tasa_activa[3]}")
            print(f"         .eur_ves = {tasa_activa[4]}")
            print(f"         .usdt_ves = {tasa_activa[5]}")
            print(f"         .fecha = {tasa_activa[1]}")
            
            # Simular el dict que retorna dashboard_administrativo()
            dashboard_dict = {
                'tipo_dashboard': 'administrativo',
                'tasas_actuales': 'objeto_tasa',  # Simulado
                'transacciones_hoy': 0,
                'clientes_activos': 0,
                'cuentas_activas': 0,
                # ... otros campos
            }
            
            print(f"\n   📋 Dict retornado incluye:")
            for key in dashboard_dict:
                print(f"      {key}: {dashboard_dict[key]}")
                
        else:
            print("   ❌ dashboard_administrativo() pasaría tasas_actuales = None")
        
        # 4. Verificar vista
        print(f"\n🎨 4. VERIFICANDO VISTA (views/default/index.html)")
        print("-" * 40)
        
        if tasa_activa:
            print("   ✅ La vista debería mostrar:")
            print(f"      {{{{if tasas_actuales:}}}} → True")
            print(f"      USD: {{{{=tasas_actuales.usd_ves}}}} → {tasa_activa[3]}")
            print(f"      EUR: {{{{=tasas_actuales.eur_ves}}}} → {tasa_activa[4]}")
            print(f"      USDT: {{{{=tasas_actuales.usdt_ves}}}} → {tasa_activa[5]}")
            
            # Simular el formato
            try:
                usd_formatted = "{:,.4f}".format(float(tasa_activa[3]))
                eur_formatted = "{:,.4f}".format(float(tasa_activa[4]))
                usdt_formatted = "{:,.4f}".format(float(tasa_activa[5])) if tasa_activa[5] else 'N/A'
                
                print(f"\n   🎯 Widget mostraría:")
                print(f"      USD: {usd_formatted}")
                print(f"      EUR: {eur_formatted}")
                print(f"      USDT: {usdt_formatted}")
                
            except Exception as e:
                print(f"   ❌ Error de formato: {e}")
                
        else:
            print("   ❌ La vista mostraría:")
            print(f"      {{{{if tasas_actuales:}}}} → False")
            print(f"      Mensaje: 'No disponible'")
        
        # 5. Verificar posibles problemas
        print(f"\n🔍 5. VERIFICANDO POSIBLES PROBLEMAS")
        print("-" * 40)
        
        # Problema 1: Campo usdt_ves NULL
        cursor.execute("SELECT COUNT(*) FROM tasas_cambio WHERE usdt_ves IS NULL")
        tasas_sin_usdt = cursor.fetchone()[0]
        
        if tasas_sin_usdt > 0:
            print(f"   ⚠️ {tasas_sin_usdt} tasas sin USDT")
            print("   🔧 Actualizando tasas sin USDT...")
            
            cursor.execute("""
                UPDATE tasas_cambio 
                SET usdt_ves = usd_ves * 0.999 
                WHERE usdt_ves IS NULL AND usd_ves IS NOT NULL
            """)
            conn.commit()
            print("   ✅ Tasas USDT actualizadas")
        
        # Problema 2: Verificar estructura de tabla
        cursor.execute("PRAGMA table_info(tasas_cambio)")
        columns = cursor.fetchall()
        
        usdt_column_exists = any(col[1] == 'usdt_ves' for col in columns)
        
        if usdt_column_exists:
            print("   ✅ Columna usdt_ves existe en la tabla")
        else:
            print("   ❌ Columna usdt_ves NO existe en la tabla")
        
        # Problema 3: Verificar cache
        print("   🔄 Cache de tasas puede estar desactualizado")
        print("      → Reiniciar web2py para limpiar cache")
        
        conn.close()
        
        # 6. Recomendaciones
        print(f"\n" + "=" * 60)
        print("📋 DIAGNÓSTICO Y RECOMENDACIONES")
        print("=" * 60)
        
        if tasa_activa:
            print("✅ DATOS CORRECTOS EN BASE DE DATOS")
            print("\n🔧 Si aún no ves las tasas:")
            print("   1. Refrescar la página (Ctrl+F5)")
            print("   2. Verificar consola del navegador por errores JavaScript")
            print("   3. Reiniciar web2py para limpiar cache")
            print("   4. Verificar que estés en el dashboard administrativo")
            
            print(f"\n🎯 Deberías ver:")
            print("   • Widget 'Tasas BCV' en esquina superior derecha")
            print("   • USD, EUR y USDT con valores numéricos")
            print("   • Sin mensajes de 'No disponible'")
            
        else:
            print("❌ PROBLEMA EN BASE DE DATOS")
            print("   • No hay tasas activas")
            print("   • Se intentó activar automáticamente")
            print("   • Verificar que la activación funcionó")
        
        return tasa_activa is not None
        
    except Exception as e:
        print(f"❌ Error durante el debug: {e}")
        return False

if __name__ == '__main__':
    debug_tasas_dashboard()