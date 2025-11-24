# -*- coding: utf-8 -*-
"""
Test: Verificar que se puede guardar un límite correctamente
"""

import sqlite3
from datetime import datetime

def test_guardar_limite():
    print("=" * 70)
    print("TEST: GUARDAR LÍMITE DE VENTA")
    print("=" * 70)
    
    conn = sqlite3.connect('databases/storage.sqlite')
    cursor = conn.cursor()
    
    fecha_hoy = datetime.now().date().isoformat()
    moneda = 'USD'
    limite_a_configurar = 500.0
    
    print(f"\n📅 Fecha: {fecha_hoy}")
    print(f"💱 Moneda: {moneda}")
    print(f"🎯 Límite a configurar: ${limite_a_configurar:,.2f}\n")
    
    # 1. Verificar remesas disponibles
    print("1️⃣ VERIFICAR REMESAS DISPONIBLES:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT id, monto_disponible
        FROM remesas_diarias
        WHERE fecha = ? AND moneda = ? AND activa = 'T'
    """, (fecha_hoy, moneda))
    
    remesas = cursor.fetchall()
    total_disponible = sum([r[1] for r in remesas])
    
    print(f"Remesas encontradas: {len(remesas)}")
    for r in remesas:
        print(f"  ID {r[0]}: ${r[1]:,.2f}")
    print(f"\nTotal disponible: ${total_disponible:,.2f}")
    
    if total_disponible == 0:
        print("\n❌ ERROR: No hay remesas disponibles")
        conn.close()
        return
    
    if limite_a_configurar > total_disponible:
        print(f"\n❌ ERROR: El límite ${limite_a_configurar:,.2f} excede el disponible ${total_disponible:,.2f}")
        conn.close()
        return
    
    # 2. Desactivar límites anteriores
    print("\n2️⃣ DESACTIVAR LÍMITES ANTERIORES:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT id, limite_diario, activo
        FROM limites_venta
        WHERE fecha = ? AND moneda = ?
    """, (fecha_hoy, moneda))
    
    limites_anteriores = cursor.fetchall()
    
    if limites_anteriores:
        print(f"Límites anteriores encontrados: {len(limites_anteriores)}")
        for l in limites_anteriores:
            print(f"  ID {l[0]}: ${l[1]:,.2f}, Activo={l[2]}")
        
        cursor.execute("""
            UPDATE limites_venta
            SET activo = 0
            WHERE fecha = ? AND moneda = ?
        """, (fecha_hoy, moneda))
        
        print(f"\n✅ Desactivados {cursor.rowcount} límites")
    else:
        print("No hay límites anteriores")
    
    # 3. Insertar nuevo límite
    print("\n3️⃣ INSERTAR NUEVO LÍMITE:")
    print("-" * 70)
    
    cursor.execute("""
        INSERT INTO limites_venta 
        (fecha, moneda, limite_diario, monto_vendido, monto_disponible, 
         porcentaje_utilizado, activo, alerta_80_enviada, alerta_95_enviada)
        VALUES (?, ?, ?, 0.00, ?, 0.0, 1, 0, 0)
    """, (fecha_hoy, moneda, limite_a_configurar, limite_a_configurar))
    
    nuevo_id = cursor.lastrowid
    
    print(f"✅ Límite insertado con ID: {nuevo_id}")
    print(f"   Límite diario: ${limite_a_configurar:,.2f}")
    print(f"   Disponible: ${limite_a_configurar:,.2f}")
    
    conn.commit()
    
    # 4. Verificar que se guardó correctamente
    print("\n4️⃣ VERIFICAR QUE SE GUARDÓ:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT id, limite_diario, monto_disponible, activo
        FROM limites_venta
        WHERE fecha = ? AND moneda = ? AND activo = 1
    """, (fecha_hoy, moneda))
    
    limite_guardado = cursor.fetchone()
    
    if limite_guardado:
        print(f"\n✅ LÍMITE GUARDADO CORRECTAMENTE:")
        print(f"   ID: {limite_guardado[0]}")
        print(f"   Límite diario: ${limite_guardado[1]:,.2f}")
        print(f"   Disponible: ${limite_guardado[2]:,.2f}")
        print(f"   Activo: {limite_guardado[3]}")
    else:
        print("\n❌ ERROR: No se encontró el límite guardado")
    
    print("\n" + "=" * 70)
    
    conn.close()

if __name__ == '__main__':
    try:
        test_guardar_limite()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
