#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para probar el acceso al historial de transacciones
"""

import requests

# URL del historial
url = "http://127.0.0.1:8000/divisas2os_multiple/divisas/historial_transacciones"

print("=" * 80)
print("PRUEBA: Acceso al Historial de Transacciones")
print("=" * 80)
print(f"\nURL: {url}")

try:
    # Hacer la petición
    response = requests.get(url, allow_redirects=False)
    
    print(f"\nCódigo de respuesta: {response.status_code}")
    print(f"Headers de respuesta:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    
    if response.status_code in [301, 302, 303, 307, 308]:
        print(f"\n⚠️ REDIRECCIÓN DETECTADA")
        print(f"Redirigiendo a: {response.headers.get('Location', 'N/A')}")
    elif response.status_code == 200:
        print(f"\n✅ Respuesta exitosa")
        print(f"Longitud del contenido: {len(response.text)} caracteres")
        
        # Verificar si contiene el título esperado
        if "Historial de Transacciones" in response.text:
            print("✅ La página contiene 'Historial de Transacciones'")
        else:
            print("❌ La página NO contiene 'Historial de Transacciones'")
            
        if "Sistema de Divisas" in response.text and "Comprar Divisas" in response.text:
            print("⚠️ Parece ser la página de divisas/index en lugar del historial")
    else:
        print(f"\n❌ Error: {response.status_code}")
        
except Exception as e:
    print(f"\n❌ Error en la petición: {str(e)}")

print("\n" + "=" * 80)
