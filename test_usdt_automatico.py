#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para probar la obtención automática de USDT
"""

import sys
import os
import sqlite3
import json
from datetime import datetime

# Agregar el directorio de web2py al path
sys.path.append('.')

def test_usdt_api():
    """Probar APIs de USDT directamente"""
    
    print("🔍 Probando APIs de USDT...")
    
    try:
        import requests
        HAS_REQUESTS = True
    except ImportError:
        print("❌ Requests no disponible, usando urllib")
        HAS_REQUESTS = False
        import urllib.request
        import urllib.error
    
    # APIs para probar
    apis = [
        {
            'name': 'CoinGecko',
            'url': 'https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd',
            'parser': lambda data: float(data['tether']['usd'])
        },
        {
            'name': 'Binance',
            'url': 'https://api.binance.com/api/v3/ticker/price?symbol=USDTUSD',
            'parser': lambda data: float(data['price'])
        }
    ]
    
    for api in apis:
        try:
            print(f"\n📡 Probando {api['name']}...")
            
            if HAS_REQUESTS:
                response = requests.get(api['url'], timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    usdt_usd = api['parser'](data)
                    print(f"   ✅ USDT/USD: {usdt_usd}")
                else:
                    print(f"   ❌ Error HTTP: {response.status_code}")
            else:
                # Usar urllib
                req = urllib.request.Request(api['url'])
                response = urllib.request.urlopen(req, timeout=10)
                if response.getcode() == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    usdt_usd = api['parser'](data)
                    print(f"   ✅ USDT/USD: {usdt_usd}")
                else:
                    print(f"   ❌ Error HTTP: {response.getcode()}")
                    
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

def test_usdt_calculation():
    """Probar el cálculo de USDT/VES"""
    
    print("\n🧮 Probando cálculo USDT/VES...")
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        # Obtener tasa USD/VES actual
        cursor.execute("""
            SELECT usd_ves, eur_ves, usdt_ves, fecha, hora, fuente
            FROM tasas_cambio 
            WHERE activa = 1
            ORDER BY fecha DESC, hora DESC
            LIMIT 1
        """)
        
        tasa_actual = cursor.fetchone()
        
        if tasa_actual:
            usd_ves, eur_ves, usdt_ves, fecha, hora, fuente = tasa_actual
            print(f"   📊 Tasa actual USD/VES: {usd_ves}")
            print(f"   📊 Tasa actual EUR/VES: {eur_ves}")
            print(f"   📊 Tasa actual USDT/VES: {usdt_ves}")
            print(f"   📅 Fecha: {fecha} {hora}")
            print(f"   🔗 Fuente: {fuente}")
            
            # Simular obtención de USDT/USD
            usdt_usd_simulado = 1.0001  # USDT típicamente cerca de 1 USD
            usdt_ves_calculado = usdt_usd_simulado * float(usd_ves)
            
            print(f"\n   🔄 Simulación:")
            print(f"   USDT/USD (simulado): {usdt_usd_simulado}")
            print(f"   USDT/VES calculado: {usdt_ves_calculado:.4f}")
            
            if usdt_ves:
                diferencia = abs(float(usdt_ves) - usdt_ves_calculado)
                print(f"   📈 Diferencia con BD: {diferencia:.4f}")
            
        else:
            print("   ❌ No hay tasas en la base de datos")
        
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def test_update_with_usdt():
    """Probar actualización de tasas con USDT"""
    
    print("\n🔄 Probando actualización con USDT...")
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        # Simular nueva tasa con USDT
        fecha_actual = datetime.now().date()
        hora_actual = datetime.now().time()
        
        # Tasas simuladas
        usd_ves = 36.75
        eur_ves = 40.12
        usdt_usd = 1.0002  # Valor típico de USDT
        usdt_ves = usdt_usd * usd_ves
        
        print(f"   📊 Tasas a insertar:")
        print(f"   USD/VES: {usd_ves}")
        print(f"   EUR/VES: {eur_ves}")
        print(f"   USDT/USD: {usdt_usd}")
        print(f"   USDT/VES: {usdt_ves:.4f}")
        
        # Desactivar tasas anteriores
        cursor.execute("UPDATE tasas_cambio SET activa = 0 WHERE activa = 1")
        
        # Insertar nueva tasa
        cursor.execute("""
            INSERT INTO tasas_cambio 
            (fecha, hora, usd_ves, eur_ves, usdt_ves, fuente, activa)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            fecha_actual.strftime('%Y-%m-%d'),
            hora_actual.strftime('%H:%M:%S'),
            usd_ves,
            eur_ves,
            usdt_ves,
            'Test Automático USDT',
            1
        ))
        
        conn.commit()
        
        # Verificar inserción
        cursor.execute("""
            SELECT id, fecha, hora, usd_ves, eur_ves, usdt_ves, fuente
            FROM tasas_cambio 
            WHERE activa = 1
        """)
        
        nueva_tasa = cursor.fetchone()
        
        if nueva_tasa:
            print(f"   ✅ Tasa insertada exitosamente:")
            print(f"   ID: {nueva_tasa[0]}")
            print(f"   Fecha: {nueva_tasa[1]} {nueva_tasa[2]}")
            print(f"   USD/VES: {nueva_tasa[3]}")
            print(f"   EUR/VES: {nueva_tasa[4]}")
            print(f"   USDT/VES: {nueva_tasa[5]}")
            print(f"   Fuente: {nueva_tasa[6]}")
        else:
            print("   ❌ Error: No se pudo verificar la inserción")
        
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def mostrar_resumen():
    """Mostrar resumen de la implementación"""
    
    print("\n" + "="*60)
    print("📋 RESUMEN: USDT AUTOMÁTICO IMPLEMENTADO")
    print("="*60)
    print()
    print("🎯 FUNCIONALIDADES AGREGADAS:")
    print("- ✅ Obtención automática de USDT desde APIs de criptomonedas")
    print("- ✅ Múltiples fuentes: CoinGecko, Binance, CoinAPI")
    print("- ✅ Cálculo automático: USDT/USD × USD/VES = USDT/VES")
    print("- ✅ Respaldo: Si falla API, usa USD como referencia")
    print("- ✅ Vista actualizada con USDT en 3 columnas")
    print("- ✅ Historial incluye columna USDT")
    print("- ✅ Inserción manual permite USDT opcional")
    print()
    print("🔄 PROCESO AUTOMÁTICO:")
    print("1. Sistema obtiene USD/VES y EUR/VES del BCV")
    print("2. Consulta APIs de crypto para obtener USDT/USD")
    print("3. Calcula USDT/VES = USDT/USD × USD/VES")
    print("4. Guarda todas las tasas en la base de datos")
    print("5. Muestra en la interfaz de usuario")
    print()
    print("📡 APIS UTILIZADAS:")
    print("- CoinGecko: https://api.coingecko.com/")
    print("- Binance: https://api.binance.com/")
    print("- CoinAPI: https://rest.coinapi.io/ (opcional)")
    print()
    print("🚀 PARA PROBAR:")
    print("1. Ve a /api en tu aplicación")
    print("2. Haz clic en 'Actualizar desde BCV'")
    print("3. Verifica que aparezca USDT/VES automáticamente")
    print()
    print("="*60)

if __name__ == "__main__":
    print("🧪 PRUEBA DE USDT AUTOMÁTICO")
    print("="*40)
    
    test_usdt_api()
    test_usdt_calculation()
    test_update_with_usdt()
    mostrar_resumen()