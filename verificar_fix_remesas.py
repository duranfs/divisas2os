# -*- coding: utf-8 -*-
"""
Verificar que el fix de remesas funciona correctamente
"""

import sqlite3
from datetime import datetime

def verificar_fix():
    print("=" * 70)
    print("VERIFICACIÓN: FIX DE SUMA DE REMESAS")
    print("=" * 70)
    
    conn = sqlite3.connect('databases/storage.sqlite')
    cursor = conn.cursor()
    
    fecha_hoy = '2025-11-22'
    
    # 1. Verificar remesas con activa = 'T'
    print(f"\n📅 Fecha: {fecha_hoy}\n")
    
    cursor.execute("""
        SELECT monto_recibido, monto_disponible, monto_vendido
        FROM remesas_diarias
        WHERE fecha = ? AND moneda = 'USD' AND activa = 'T'
    """, (fecha_hoy,))
    
    rows = cursor.fetchall()
    
    print("REMESAS DE USD CON activa = 'T':")
    print("-" * 70)
    
    total_recibido = 0
    total_disponible = 0
    total_vendido = 0
    
    for i, row in enumerate(rows, 1):
        recibido, disponible, vendido = row
        print(f"\nRemesa {i}:")
        print(f"  Recibido:    ${float(recibido):,.2f}")
        print(f"  Disponible:  ${float(disponible):,.2f}")
        print(f"  Vendido:     ${float(vendido):,.2f}")
        
        total_recibido += float(recibido)
        total_disponible += float(disponible)
        total_vendido += float(vendido)
    
    print("\n" + "=" * 70)
    print("\nTOTALES:")
    print("-" * 70)
    print(f"Total Recibido:    ${total_recibido:,.2f}")
    print(f"Total Disponible:  ${total_disponible:,.2f}")
    print(f"Total Vendido:     ${total_vendido:,.2f}")
    
    # 2. Verificación
    print("\n" + "=" * 70)
    print("\nRESULTADO:")
    print("-" * 70)
    
    if total_disponible == 500.0:
        print("\n✅ ¡PERFECTO! El fix funciona correctamente")
        print(f"   El dashboard ahora mostrará: ${total_disponible:,.2f}")
        print("\n📋 PASOS SIGUIENTES:")
        print("   1. Reinicia el servidor web2py")
        print("   2. Refresca el navegador (Ctrl+F5)")
        print("   3. Ve a la página de remesas")
        print("   4. Deberías ver $500.00 en 'Remesa Disponible'")
    else:
        print(f"\n❌ ERROR: La suma es ${total_disponible:,.2f} en lugar de $500.00")
    
    print("\n" + "=" * 70)
    
    conn.close()

if __name__ == '__main__':
    try:
        verificar_fix()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
