# -*- coding: utf-8 -*-
"""
Script para consultar USDT/VES desde Binance P2P
"""

import urllib.request
import json
from datetime import datetime

print("=" * 70)
print("CONSULTA BINANCE P2P - USDT/VES")
print("=" * 70)
print(f"\nFecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n" + "=" * 70)

try:
    # API de Binance P2P para Venezuela
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    
    # Payload para buscar ofertas de COMPRA de USDT en VES
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "merchantCheck": False,
        "page": 1,
        "payTypes": [],
        "publisherType": None,
        "rows": 10,
        "tradeType": "BUY"
    }
    
    # Convertir payload a JSON
    data = json.dumps(payload).encode('utf-8')
    
    # Crear request
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
    )
    
    print("\n🔍 Consultando Binance P2P...")
    print("-" * 70)
    
    # Hacer la petición
    with urllib.request.urlopen(req, timeout=10) as response:
        result = json.loads(response.read().decode('utf-8'))
    
    # Procesar resultados
    if result.get('data') and len(result['data']) > 0:
        print(f"\n✅ Se encontraron {len(result['data'])} ofertas\n")
        
        prices = []
        
        print("📊 OFERTAS DE COMPRA DE USDT:")
        print("-" * 70)
        print(f"{'#':<4} {'Precio (VES)':<15} {'Límites':<25} {'Comerciante':<20}")
        print("-" * 70)
        
        for i, ad in enumerate(result['data'][:10], 1):
            adv = ad.get('adv', {})
            advertiser = ad.get('advertiser', {})
            
            price = float(adv.get('price', 0))
            min_amount = float(adv.get('minSingleTransAmount', 0))
            max_amount = float(adv.get('dynamicMaxSingleTransAmount', 0))
            nickname = advertiser.get('nickName', 'N/A')
            
            prices.append(price)
            
            print(f"{i:<4} {price:>12,.2f}   {min_amount:>8,.0f} - {max_amount:>8,.0f}   {nickname:<20}")
        
        print("-" * 70)
        
        # Calcular estadísticas
        if prices:
            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)
            
            print(f"\n📈 ESTADÍSTICAS:")
            print("-" * 70)
            print(f"   Precio Promedio:  {avg_price:>12,.4f} VES")
            print(f"   Precio Mínimo:    {min_price:>12,.4f} VES")
            print(f"   Precio Máximo:    {max_price:>12,.4f} VES")
            print(f"   Diferencia:       {max_price - min_price:>12,.4f} VES ({((max_price/min_price - 1) * 100):.2f}%)")
            
            print(f"\n💡 RECOMENDACIÓN:")
            print("-" * 70)
            print(f"   Usar precio promedio: {avg_price:,.4f} VES por USDT")
            print(f"   Este es el precio real del mercado P2P venezolano")
    else:
        print("\n❌ No se encontraron ofertas")
        print("   Esto puede deberse a:")
        print("   - Problemas de conexión")
        print("   - Binance P2P no disponible temporalmente")
        print("   - No hay ofertas activas en este momento")

except urllib.error.HTTPError as e:
    print(f"\n❌ Error HTTP: {e.code}")
    print(f"   Mensaje: {e.reason}")
except urllib.error.URLError as e:
    print(f"\n❌ Error de conexión: {e.reason}")
except Exception as e:
    print(f"\n❌ Error inesperado: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("NOTA: Estos son precios reales del mercado P2P de Binance")
print("Representan el valor al que los venezolanos compran/venden USDT")
print("=" * 70)
