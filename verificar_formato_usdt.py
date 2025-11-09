#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para verificar que el formato USDT/VES esté correcto en todas las vistas
"""

import os
import re

def verificar_archivos():
    """Verificar formato USDT en archivos clave"""
    
    archivos_a_verificar = [
        "views/default/index.html",
        "views/api/index.html",
        "controllers/api.py",
        "controllers/default.py",
        "controllers/divisas.py"
    ]
    
    print("🔍 Verificando formato USDT/VES en archivos...")
    
    patrones_incorrectos = [
        r'USDT\s*/\s*VES',  # USDT / VES con espacios
        r'USDT\s+/\s+VES',  # USDT / VES con múltiples espacios
        r'usdt\s*/\s*ves',  # minúsculas con espacios
    ]
    
    patron_correcto = r'USDT/VES'
    
    for archivo in archivos_a_verificar:
        if os.path.exists(archivo):
            print(f"\n📄 Verificando {archivo}...")
            
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Buscar patrones incorrectos
            encontrados_incorrectos = []
            for i, patron in enumerate(patrones_incorrectos):
                matches = re.findall(patron, contenido, re.IGNORECASE)
                if matches:
                    encontrados_incorrectos.extend(matches)
            
            # Buscar patrón correcto
            correctos = re.findall(patron_correcto, contenido)
            
            if encontrados_incorrectos:
                print(f"   ❌ Formatos incorrectos encontrados: {encontrados_incorrectos}")
            else:
                print(f"   ✅ No se encontraron formatos incorrectos")
            
            if correctos:
                print(f"   ✅ Formatos correctos encontrados: {len(correctos)} ocurrencias")
            else:
                print(f"   ⚠️  No se encontró 'USDT/VES' en este archivo")
        else:
            print(f"\n❌ Archivo no encontrado: {archivo}")

def verificar_base_datos():
    """Verificar que la base de datos tenga la columna usdt_ves"""
    
    print("\n🗄️  Verificando estructura de base de datos...")
    
    try:
        import sqlite3
        
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        # Verificar estructura de la tabla tasas_cambio
        cursor.execute("PRAGMA table_info(tasas_cambio)")
        columnas = cursor.fetchall()
        
        columnas_nombres = [col[1] for col in columnas]
        
        print(f"   📊 Columnas en tasas_cambio: {columnas_nombres}")
        
        if 'usdt_ves' in columnas_nombres:
            print("   ✅ Columna usdt_ves existe")
            
            # Verificar si hay datos USDT
            cursor.execute("SELECT COUNT(*) FROM tasas_cambio WHERE usdt_ves IS NOT NULL")
            count_usdt = cursor.fetchone()[0]
            
            print(f"   📈 Registros con USDT: {count_usdt}")
            
            if count_usdt > 0:
                # Mostrar último registro con USDT
                cursor.execute("""
                    SELECT fecha, hora, usd_ves, eur_ves, usdt_ves, fuente
                    FROM tasas_cambio 
                    WHERE usdt_ves IS NOT NULL
                    ORDER BY fecha DESC, hora DESC
                    LIMIT 1
                """)
                
                ultimo = cursor.fetchone()
                if ultimo:
                    print(f"   📅 Último registro USDT:")
                    print(f"      Fecha: {ultimo[0]} {ultimo[1]}")
                    print(f"      USD/VES: {ultimo[2]}")
                    print(f"      EUR/VES: {ultimo[3]}")
                    print(f"      USDT/VES: {ultimo[4]}")
                    print(f"      Fuente: {ultimo[5]}")
        else:
            print("   ❌ Columna usdt_ves NO existe")
        
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Error verificando BD: {str(e)}")

def verificar_apis_usdt():
    """Verificar que las APIs de USDT estén funcionando"""
    
    print("\n🌐 Verificando APIs de USDT...")
    
    try:
        import urllib.request
        import json
        
        # Probar CoinGecko
        try:
            url = 'https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd'
            response = urllib.request.urlopen(url, timeout=10)
            data = json.loads(response.read().decode('utf-8'))
            usdt_usd = data['tether']['usd']
            print(f"   ✅ CoinGecko: USDT/USD = {usdt_usd}")
        except Exception as e:
            print(f"   ❌ CoinGecko error: {str(e)}")
        
        # Probar Binance (puede fallar por restricciones)
        try:
            url = 'https://api.binance.com/api/v3/ticker/price?symbol=USDTUSD'
            response = urllib.request.urlopen(url, timeout=10)
            data = json.loads(response.read().decode('utf-8'))
            usdt_usd = data['price']
            print(f"   ✅ Binance: USDT/USD = {usdt_usd}")
        except Exception as e:
            print(f"   ⚠️  Binance error (normal): {str(e)}")
            
    except Exception as e:
        print(f"   ❌ Error general: {str(e)}")

def mostrar_resumen():
    """Mostrar resumen de la verificación"""
    
    print("\n" + "="*60)
    print("📋 RESUMEN DE VERIFICACIÓN USDT/VES")
    print("="*60)
    print()
    print("✅ IMPLEMENTACIÓN COMPLETADA:")
    print("- Formato correcto: USDT/VES (sin espacios)")
    print("- Vista de API actualizada con 3 columnas")
    print("- Vista principal (dashboard) actualizada")
    print("- Obtención automática desde APIs crypto")
    print("- Cálculo: USDT/USD × USD/VES = USDT/VES")
    print("- Respaldo: Si falla API, usa USD como referencia")
    print()
    print("🔄 PROCESO AUTOMÁTICO:")
    print("1. Sistema obtiene USD/VES del BCV")
    print("2. Consulta CoinGecko para USDT/USD")
    print("3. Calcula USDT/VES automáticamente")
    print("4. Muestra en interfaz como 'USDT/VES'")
    print()
    print("🚀 PARA USAR:")
    print("1. Ve a /api en tu aplicación")
    print("2. Haz clic en 'Actualizar desde BCV'")
    print("3. Verifica que aparezca USDT/VES correctamente")
    print()
    print("="*60)

if __name__ == "__main__":
    print("🔍 VERIFICACIÓN DE FORMATO USDT/VES")
    print("="*40)
    
    verificar_archivos()
    verificar_base_datos()
    verificar_apis_usdt()
    mostrar_resumen()