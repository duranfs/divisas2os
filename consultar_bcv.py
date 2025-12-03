# -*- coding: utf-8 -*-
"""
Script para consultar tasas oficiales del BCV
"""

import urllib.request
import json
from datetime import datetime

print("=" * 70)
print("CONSULTA TASAS OFICIALES DEL BCV")
print("=" * 70)
print(f"\nFecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n" + "=" * 70)

# Método 1: Intentar obtener del sitio web del BCV
print("\n🔍 Método 1: Scraping del sitio web del BCV")
print("-" * 70)
try:
    url = "https://www.bcv.org.ve/"
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    )
    
    with urllib.request.urlopen(req, timeout=15) as response:
        html = response.read().decode('utf-8', errors='ignore')
    
    # Buscar patrones comunes en el HTML del BCV
    import re
    
    # Patrón para USD
    usd_patterns = [
        r'USD.*?(\d+[,\.]\d+)',
        r'D[oó]lar.*?(\d+[,\.]\d+)',
        r'usd.*?(\d+[,\.]\d+)',
    ]
    
    # Patrón para EUR
    eur_patterns = [
        r'EUR.*?(\d+[,\.]\d+)',
        r'Euro.*?(\d+[,\.]\d+)',
        r'eur.*?(\d+[,\.]\d+)',
    ]
    
    usd_found = None
    eur_found = None
    
    for pattern in usd_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            usd_str = match.group(1).replace(',', '.')
            try:
                usd_found = float(usd_str)
                if 30 < usd_found < 100:  # Rango razonable
                    break
            except:
                pass
    
    for pattern in eur_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            eur_str = match.group(1).replace(',', '.')
            try:
                eur_found = float(eur_str)
                if 30 < eur_found < 100:  # Rango razonable
                    break
            except:
                pass
    
    if usd_found:
        print(f"   ✅ USD/VES: {usd_found:.4f} Bs")
    else:
        print("   ⚠️  No se pudo extraer USD/VES del HTML")
    
    if eur_found:
        print(f"   ✅ EUR/VES: {eur_found:.4f} Bs")
    else:
        print("   ⚠️  No se pudo extraer EUR/VES del HTML")

except Exception as e:
    print(f"   ❌ Error: {str(e)}")

# Método 2: API alternativa (DolarToday)
print("\n🔍 Método 2: DolarToday API")
print("-" * 70)
try:
    url = "https://s3.amazonaws.com/dolartoday/data.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    # DolarToday tiene varias tasas
    if 'USD' in data:
        usd_dt = data['USD'].get('promedio', 0)
        if usd_dt:
            print(f"   USD/VES (Promedio): {usd_dt:.4f} Bs")
        
        usd_bcv = data['USD'].get('sicad2', 0)
        if usd_bcv:
            print(f"   USD/VES (BCV ref): {usd_bcv:.4f} Bs")
    
    if 'EUR' in data:
        eur_dt = data['EUR'].get('promedio', 0)
        if eur_dt:
            print(f"   EUR/VES (Promedio): {eur_dt:.4f} Bs")

except Exception as e:
    print(f"   ❌ Error: {str(e)}")

# Método 3: ExchangeRate-API (referencia internacional)
print("\n🔍 Método 3: ExchangeRate-API (Referencia Internacional)")
print("-" * 70)
try:
    # USD/VES
    url_usd = "https://api.exchangerate-api.com/v4/latest/USD"
    with urllib.request.urlopen(url_usd, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    if 'rates' in data and 'VES' in data['rates']:
        usd_ves = data['rates']['VES']
        print(f"   ✅ USD/VES: {usd_ves:.4f} Bs")
    
    # EUR/VES
    url_eur = "https://api.exchangerate-api.com/v4/latest/EUR"
    with urllib.request.urlopen(url_eur, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    if 'rates' in data and 'VES' in data['rates']:
        eur_ves = data['rates']['VES']
        print(f"   ✅ EUR/VES: {eur_ves:.4f} Bs")

except Exception as e:
    print(f"   ❌ Error: {str(e)}")

# Método 4: Calcular EUR desde USD
print("\n🔍 Método 4: Calcular EUR/VES desde USD/VES")
print("-" * 70)
try:
    # Obtener EUR/USD
    url = "https://api.exchangerate-api.com/v4/latest/EUR"
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    if 'rates' in data and 'USD' in data['rates']:
        eur_usd = data['rates']['USD']
        print(f"   EUR/USD: {eur_usd:.4f}")
        
        # Si tenemos USD/VES, calcular EUR/VES
        if 'usd_ves' in locals():
            eur_ves_calc = usd_ves / eur_usd
            print(f"   EUR/VES calculado: {eur_ves_calc:.4f} Bs")
            print(f"   (Basado en USD/VES ÷ EUR/USD)")

except Exception as e:
    print(f"   ❌ Error: {str(e)}")

print("\n" + "=" * 70)
print("RESUMEN")
print("=" * 70)
print("\nNOTA: El BCV actualiza sus tasas diariamente.")
print("Las tasas mostradas son referencias de diferentes fuentes.")
print("Para operaciones oficiales, consultar directamente www.bcv.org.ve")
print("\n" + "=" * 70)
