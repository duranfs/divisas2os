# -*- coding: utf-8 -*-
"""
Script para consultar tasas actuales del mercado
"""

import requests
import json
from datetime import datetime

print("=" * 70)
print("CONSULTA DE TASAS ACTUALES DEL MERCADO")
print("=" * 70)
print(f"\nFecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n" + "=" * 70)

# 1. USD/VES desde ExchangeRate-API
print("\n📊 USD/VES:")
print("-" * 70)
try:
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
    if response.status_code == 200:
        data = response.json()
        if 'rates' in data and 'VES' in data['rates']:
            usd_ves = data['rates']['VES']
            print(f"   ExchangeRate-API: {usd_ves:,.4f} VES")
        else:
            print("   ❌ No se encontró VES en la respuesta")
    else:
        print(f"   ❌ Error HTTP: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

# 2. EUR/VES desde ExchangeRate-API
print("\n📊 EUR/VES:")
print("-" * 70)
try:
    response = requests.get("https://api.exchangerate-api.com/v4/latest/EUR", timeout=10)
    if response.status_code == 200:
        data = response.json()
        if 'rates' in data and 'VES' in data['rates']:
            eur_ves = data['rates']['VES']
            print(f"   ExchangeRate-API: {eur_ves:,.4f} VES")
        else:
            print("   ❌ No se encontró VES en la respuesta")
    else:
        print(f"   ❌ Error HTTP: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

# 3. USDT/VES desde CoinGecko
print("\n📊 USDT/VES:")
print("-" * 70)
try:
    # Obtener precio de USDT en USD
    response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd", timeout=10)
    if response.status_code == 200:
        data = response.json()
        usdt_usd = data.get('tether', {}).get('usd', 1.0)
        print(f"   CoinGecko USDT/USD: {usdt_usd:.4f}")
        
        # Calcular USDT/VES usando USD/VES
        if 'usd_ves' in locals():
            usdt_ves_calculated = usd_ves * usdt_usd
            print(f"   USDT/VES calculado: {usdt_ves_calculated:,.4f} VES")
            print(f"   (Basado en USD/VES × USDT/USD)")
    else:
        print(f"   ❌ Error HTTP: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

# 4. Binance P2P (USDT/VES)
print("\n📊 USDT/VES desde Binance P2P:")
print("-" * 70)
try:
    # API de Binance P2P para Venezuela
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "merchantCheck": False,
        "page": 1,
        "payTypes": [],
        "publisherType": None,
        "rows": 5,
        "tradeType": "BUY"
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        if data.get('data') and len(data['data']) > 0:
            prices = [float(ad['adv']['price']) for ad in data['data'][:5]]
            avg_price = sum(prices) / len(prices)
            print(f"   Binance P2P (promedio 5 ofertas): {avg_price:,.4f} VES")
            print(f"   Rango: {min(prices):,.4f} - {max(prices):,.4f} VES")
        else:
            print("   ❌ No se encontraron ofertas")
    else:
        print(f"   ❌ Error HTTP: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

# 5. Reserve (USDT/VES)
print("\n📊 USDT/VES desde Reserve:")
print("-" * 70)
try:
    response = requests.get("https://reserve.org/api/v1/rates", timeout=10)
    if response.status_code == 200:
        data = response.json()
        # Buscar USDT/VES en la respuesta
        for rate in data.get('rates', []):
            if rate.get('from') == 'USDT' and rate.get('to') == 'VES':
                print(f"   Reserve: {float(rate['rate']):,.4f} VES")
                break
        else:
            print("   ℹ️  No disponible en Reserve")
    else:
        print(f"   ❌ Error HTTP: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

print("\n" + "=" * 70)
print("RESUMEN")
print("=" * 70)
print("\nNOTA: Las tasas pueden variar según la fuente y el momento.")
print("Para USDT, se recomienda usar Binance P2P ya que refleja")
print("el mercado real venezolano.")
print("\n" + "=" * 70)
