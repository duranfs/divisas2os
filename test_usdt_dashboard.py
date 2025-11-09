#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para probar que el dashboard muestre correctamente las tasas USDT
"""

import sqlite3
import sys
import os

def test_dashboard_usdt():
    """Probar que el dashboard tenga acceso a tasas USDT"""
    print("🔍 PROBANDO DASHBOARD CON TASAS USDT")
    print("=" * 60)
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("databases/storage.sqlite")
        cursor = conn.cursor()
        
        # Simular la consulta que hace obtener_tasas_actuales()
        cursor.execute("""
            SELECT id, fecha, hora, usd_ves, eur_ves, usdt_ves, fuente, activa
            FROM tasas_cambio 
            WHERE activa = 1
            ORDER BY fecha DESC, hora DESC 
            LIMIT 1
        """)
        
        tasa_activa = cursor.fetchone()
        
        if tasa_activa:
            print("✅ Tasa activa encontrada:")
            print(f"  ID: {tasa_activa[0]}")
            print(f"  Fecha: {tasa_activa[1]} {tasa_activa[2]}")
            print(f"  USD/VES: {tasa_activa[3]}")
            print(f"  EUR/VES: {tasa_activa[4]}")
            print(f"  USDT/VES: {tasa_activa[5]}")
            print(f"  Fuente: {tasa_activa[6]}")
            print(f"  Activa: {'Sí' if tasa_activa[7] else 'No'}")
            
            # Verificar que USDT no sea None
            if tasa_activa[5] is not None:
                print("\n✅ USDT está disponible para el dashboard")
                
                # Simular el formato que usa la vista
                usdt_formatted = "{:,.4f}".format(float(tasa_activa[5]))
                print(f"  Formato para vista: {usdt_formatted}")
                
                # Verificar que sea un valor razonable
                usdt_value = float(tasa_activa[5])
                usd_value = float(tasa_activa[3])
                
                if 0.95 <= (usdt_value / usd_value) <= 1.05:
                    print("✅ Relación USDT/USD es razonable")
                else:
                    print("⚠️ Relación USDT/USD parece incorrecta")
                    
            else:
                print("❌ USDT es NULL - no se mostrará en el dashboard")
                
        else:
            print("❌ No hay tasa activa")
            
            # Buscar la más reciente
            cursor.execute("""
                SELECT id, fecha, hora, usd_ves, eur_ves, usdt_ves, fuente, activa
                FROM tasas_cambio 
                ORDER BY fecha DESC, hora DESC 
                LIMIT 1
            """)
            
            tasa_reciente = cursor.fetchone()
            if tasa_reciente:
                print("\n📊 Tasa más reciente (no activa):")
                print(f"  ID: {tasa_reciente[0]}")
                print(f"  USDT/VES: {tasa_reciente[5]}")
        
        # Probar la consulta para dashboard de cliente
        print("\n🔍 Probando consulta para dashboard de cliente...")
        
        # Simular obtener_tasas_actuales() completa
        cursor.execute("""
            SELECT * FROM tasas_cambio 
            WHERE activa = 1
            ORDER BY fecha DESC, hora DESC 
            LIMIT 1
        """)
        
        tasa_completa = cursor.fetchone()
        if tasa_completa:
            print("✅ Consulta de dashboard funcionará correctamente")
        else:
            print("⚠️ Dashboard podría no mostrar tasas")
        
        # Probar API dashboard data
        print("\n🔍 Probando datos para API dashboard...")
        
        if tasa_activa and tasa_activa[5]:
            api_response = {
                'tasa_usd': float(tasa_activa[3]),
                'tasa_eur': float(tasa_activa[4]),
                'tasa_usdt': float(tasa_activa[5])
            }
            print("✅ API response incluirá USDT:")
            print(f"  {api_response}")
        else:
            print("❌ API response no incluirá USDT válido")
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ PRUEBA COMPLETADA")
        print("=" * 60)
        
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Acceder al dashboard: http://127.0.0.1:8000/divisas2os")
        print("2. Verificar que aparezca 'USDT / VES' en las tasas actuales")
        print("3. Confirmar que el valor sea similar al USD pero ligeramente menor")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False

if __name__ == '__main__':
    test_dashboard_usdt()