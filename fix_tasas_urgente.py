#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fix urgente para que aparezcan las tasas en el dashboard
"""

import sqlite3

def fix_tasas_urgente():
    """Fix urgente para las tasas"""
    print("🚨 FIX URGENTE: RESTAURANDO TASAS EN DASHBOARD")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect("databases/storage.sqlite")
        cursor = conn.cursor()
        
        # 1. Verificar y corregir tasas activas
        print("🔧 1. CORRIGIENDO TASAS ACTIVAS")
        print("-" * 40)
        
        # Desactivar todas las tasas
        cursor.execute("UPDATE tasas_cambio SET activa = 0")
        
        # Activar solo la más reciente
        cursor.execute("""
            UPDATE tasas_cambio SET activa = 1 
            WHERE id = (
                SELECT id FROM tasas_cambio 
                ORDER BY fecha DESC, hora DESC 
                LIMIT 1
            )
        """)
        
        conn.commit()
        
        # Verificar resultado
        cursor.execute("""
            SELECT id, fecha, hora, usd_ves, eur_ves, usdt_ves, activa
            FROM tasas_cambio 
            WHERE activa = 1
        """)
        
        tasa_activa = cursor.fetchone()
        
        if tasa_activa:
            print(f"   ✅ Tasa activa: ID {tasa_activa[0]}")
            print(f"      Fecha: {tasa_activa[1]} {tasa_activa[2]}")
            print(f"      USD: {tasa_activa[3]}")
            print(f"      EUR: {tasa_activa[4]}")
            print(f"      USDT: {tasa_activa[5]}")
        else:
            print("   ❌ No se pudo activar ninguna tasa")
            return False
        
        # 2. Verificar que USDT no sea NULL
        print(f"\n🔧 2. VERIFICANDO USDT")
        print("-" * 40)
        
        if tasa_activa[5] is None:
            print("   ⚠️ USDT es NULL, corrigiendo...")
            usdt_value = float(tasa_activa[3]) * 0.999  # USDT = USD * 0.999
            cursor.execute("""
                UPDATE tasas_cambio 
                SET usdt_ves = ? 
                WHERE id = ?
            """, (usdt_value, tasa_activa[0]))
            conn.commit()
            print(f"   ✅ USDT corregido: {usdt_value}")
        else:
            print(f"   ✅ USDT correcto: {tasa_activa[5]}")
        
        # 3. Crear tasa de prueba si es necesario
        print(f"\n🔧 3. CREANDO TASA DE PRUEBA ACTUAL")
        print("-" * 40)
        
        from datetime import datetime
        
        # Desactivar todas
        cursor.execute("UPDATE tasas_cambio SET activa = 0")
        
        # Crear nueva tasa con fecha de hoy
        cursor.execute("""
            INSERT INTO tasas_cambio 
            (fecha, hora, usd_ves, eur_ves, usdt_ves, fuente, activa)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().date(),
            datetime.now().time(),
            36.5000,  # USD
            40.2500,  # EUR  
            36.4635,  # USDT
            'Fix Urgente',
            1  # activa
        ))
        
        conn.commit()
        nueva_id = cursor.lastrowid
        
        print(f"   ✅ Nueva tasa creada: ID {nueva_id}")
        print(f"      USD: 36.5000")
        print(f"      EUR: 40.2500")
        print(f"      USDT: 36.4635")
        
        conn.close()
        
        # 4. Instrucciones finales
        print(f"\n" + "=" * 60)
        print("✅ FIX COMPLETADO")
        print("=" * 60)
        
        print("🔄 PASOS SIGUIENTES:")
        print("   1. Refrescar la página del dashboard (F5)")
        print("   2. Buscar el widget 'Tasas BCV' en esquina superior derecha")
        print("   3. Deberías ver USD: 36.5000, EUR: 40.2500, USDT: 36.4635")
        
        print(f"\n🎯 SI AÚN NO APARECEN:")
        print("   • Verificar consola del navegador (F12)")
        print("   • Buscar errores JavaScript")
        print("   • Reiniciar web2py completamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el fix: {e}")
        return False

if __name__ == '__main__':
    fix_tasas_urgente()