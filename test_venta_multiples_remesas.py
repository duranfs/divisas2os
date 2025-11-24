# -*- coding: utf-8 -*-
"""
Test: Venta con múltiples remesas
"""

import sqlite3
from datetime import datetime

def test_venta():
    print("=" * 70)
    print("TEST: VENTA CON MÚLTIPLES REMESAS")
    print("=" * 70)
    
    conn = sqlite3.connect('databases/storage.sqlite')
    cursor = conn.cursor()
    
    fecha_hoy = datetime.now().date().isoformat()
    moneda = 'USD'
    monto_venta = 282.24
    
    print(f"\n📅 Fecha: {fecha_hoy}")
    print(f"💱 Moneda: {moneda}")
    print(f"💰 Monto a vender: ${monto_venta:,.2f}\n")
    
    # 1. Ver remesas disponibles
    print("1️⃣ REMESAS DISPONIBLES:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT id, monto_disponible
        FROM remesas_diarias
        WHERE fecha = ? AND moneda = ? AND activa = 'T'
        ORDER BY id
    """, (fecha_hoy, moneda))
    
    remesas = cursor.fetchall()
    total_disponible = sum([r[1] for r in remesas])
    
    print(f"Remesas encontradas: {len(remesas)}")
    for r in remesas:
        print(f"  ID {r[0]}: ${r[1]:,.2f}")
    print(f"\nTotal disponible: ${total_disponible:,.2f}")
    
    # 2. Verificar límite
    print("\n2️⃣ LÍMITE CONFIGURADO:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT id, limite_diario, monto_disponible
        FROM limites_venta
        WHERE fecha = ? AND moneda = ? AND activo = 'T'
    """, (fecha_hoy, moneda))
    
    limite = cursor.fetchone()
    
    if limite:
        print(f"Límite ID {limite[0]}:")
        print(f"  Límite diario: ${limite[1]:,.2f}")
        print(f"  Disponible: ${limite[2]:,.2f}")
    else:
        print("❌ No hay límite configurado")
        conn.close()
        return
    
    # 3. Validar si se puede vender
    print("\n3️⃣ VALIDACIÓN:")
    print("-" * 70)
    
    puede_vender = True
    razon = ""
    
    if monto_venta > limite[2]:
        puede_vender = False
        razon = f"Excede límite disponible (${limite[2]:,.2f})"
    elif monto_venta > total_disponible:
        puede_vender = False
        razon = f"Excede remesa disponible (${total_disponible:,.2f})"
    
    if puede_vender:
        print(f"✅ PUEDE VENDER ${monto_venta:,.2f}")
        print(f"   Límite disponible: ${limite[2]:,.2f}")
        print(f"   Remesa disponible: ${total_disponible:,.2f}")
    else:
        print(f"❌ NO PUEDE VENDER: {razon}")
    
    # 4. Simular descuento FIFO
    if puede_vender:
        print("\n4️⃣ SIMULACIÓN DE DESCUENTO FIFO:")
        print("-" * 70)
        
        monto_restante = monto_venta
        
        for remesa in remesas:
            if monto_restante <= 0:
                break
            
            id_remesa, disponible = remesa
            
            if disponible > 0:
                monto_a_descontar = min(monto_restante, disponible)
                nuevo_disponible = disponible - monto_a_descontar
                
                print(f"\nRemesa ID {id_remesa}:")
                print(f"  Disponible antes: ${disponible:,.2f}")
                print(f"  Descontar: ${monto_a_descontar:,.2f}")
                print(f"  Disponible después: ${nuevo_disponible:,.2f}")
                
                monto_restante -= monto_a_descontar
        
        if monto_restante == 0:
            print(f"\n✅ Venta completa de ${monto_venta:,.2f}")
        else:
            print(f"\n❌ Faltaron ${monto_restante:,.2f}")
    
    print("\n" + "=" * 70)
    
    conn.close()

if __name__ == '__main__':
    try:
        test_venta()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
