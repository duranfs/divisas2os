# -*- coding: utf-8 -*-
"""
Diagnóstico de Disponibilidad - Remesas vs Límites
"""

import sqlite3
from datetime import datetime

def diagnosticar():
    print("=" * 70)
    print("DIAGNÓSTICO: REMESAS vs LÍMITES")
    print("=" * 70)
    
    conn = sqlite3.connect('databases/storage.sqlite')
    cursor = conn.cursor()
    
    fecha_hoy = datetime.now().date().isoformat()
    
    print(f"\n📅 Fecha: {fecha_hoy}")
    print("\n" + "=" * 70)
    
    # 1. REMESAS DEL DÍA
    print("\n💰 REMESAS DEL DÍA (Dinero físico disponible):")
    print("-" * 70)
    
    cursor.execute("""
        SELECT moneda, monto_recibido, monto_vendido, monto_disponible, activa
        FROM remesas_diarias
        WHERE fecha = ?
        ORDER BY moneda
    """, (fecha_hoy,))
    
    remesas = cursor.fetchall()
    
    if remesas:
        for remesa in remesas:
            moneda, recibido, vendido, disponible, activa = remesa
            estado = "✅ ACTIVA" if activa else "❌ INACTIVA"
            print(f"\n{moneda}:")
            print(f"  Recibido:    ${recibido:,.2f}")
            print(f"  Vendido:     ${vendido:,.2f}")
            print(f"  Disponible:  ${disponible:,.2f}  ← DINERO FÍSICO QUE TIENES")
            print(f"  Estado:      {estado}")
    else:
        print("  ℹ️  No hay remesas registradas para hoy")
    
    # 2. LÍMITES DEL DÍA
    print("\n" + "=" * 70)
    print("\n🚦 LÍMITES DE VENTA DEL DÍA (Control de cuánto puedes vender):")
    print("-" * 70)
    
    cursor.execute("""
        SELECT moneda, limite_diario, monto_vendido, monto_disponible, 
               porcentaje_utilizado, activo
        FROM limites_venta
        WHERE fecha = ?
        ORDER BY moneda
    """, (fecha_hoy,))
    
    limites = cursor.fetchall()
    
    if limites:
        for limite in limites:
            moneda, limite_diario, vendido, disponible, porcentaje, activo = limite
            estado = "✅ ACTIVO" if activo else "❌ INACTIVO"
            print(f"\n{moneda}:")
            print(f"  Límite diario:  ${limite_diario:,.2f}  ← MÁXIMO QUE PUEDES VENDER HOY")
            print(f"  Ya vendido:     ${vendido:,.2f}")
            print(f"  Aún puedes:     ${disponible:,.2f}  ← CUÁNTO MÁS PUEDES VENDER")
            print(f"  Utilizado:      {porcentaje:.1f}%")
            print(f"  Estado:         {estado}")
    else:
        print("  ℹ️  No hay límites configurados para hoy")
    
    # 3. EXPLICACIÓN
    print("\n" + "=" * 70)
    print("\n📖 EXPLICACIÓN:")
    print("-" * 70)
    print("""
SON DOS CONCEPTOS DIFERENTES:

1. REMESA DISPONIBLE (Dinero físico):
   - Es el dinero que realmente tienes en caja
   - Ejemplo: Recibiste $500 USD hoy
   
2. LÍMITE DISPONIBLE (Control de ventas):
   - Es cuánto PUEDES VENDER según tu política
   - Ejemplo: Configuraste límite de $100 USD por día
   
ESCENARIO ACTUAL:
- Tienes $500 en caja (remesa)
- Pero solo puedes vender $100 hoy (límite)
- Esto es CORRECTO si quieres controlar las ventas

SOLUCIÓN:
Si quieres vender los $500 completos:
1. Ve a "Configurar Límites"
2. Cambia el límite de USD a $500
3. Ahora podrás vender hasta $500
    """)
    
    print("\n" + "=" * 70)
    
    conn.close()

if __name__ == '__main__':
    diagnosticar()
