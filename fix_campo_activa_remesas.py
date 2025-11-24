# -*- coding: utf-8 -*-
"""
Fix: Corregir campo 'activa' en remesas
El problema es que está guardado como 'T' en lugar de 1 o True
"""

import sqlite3

def fix_campo_activa():
    print("=" * 70)
    print("FIX: CAMPO 'ACTIVA' EN REMESAS")
    print("=" * 70)
    
    conn = sqlite3.connect('databases/storage.sqlite')
    cursor = conn.cursor()
    
    # 1. Ver el problema actual
    print("\n1️⃣ PROBLEMA ACTUAL:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT id, moneda, activa, typeof(activa)
        FROM remesas_diarias
        WHERE fecha = '2025-11-22'
    """)
    
    remesas = cursor.fetchall()
    
    for remesa in remesas:
        id_r, moneda, activa, tipo = remesa
        print(f"ID {id_r} ({moneda}): activa = '{activa}' (tipo: {tipo})")
    
    # 2. Probar consultas
    print("\n" + "=" * 70)
    print("\n2️⃣ PROBAR CONSULTAS:")
    print("-" * 70)
    
    # Con = 1
    cursor.execute("""
        SELECT COUNT(*) FROM remesas_diarias
        WHERE fecha = '2025-11-22' AND activa = 1
    """)
    count1 = cursor.fetchone()[0]
    print(f"\nWHERE activa = 1: {count1} resultados")
    
    # Con = 'T'
    cursor.execute("""
        SELECT COUNT(*) FROM remesas_diarias
        WHERE fecha = '2025-11-22' AND activa = 'T'
    """)
    count2 = cursor.fetchone()[0]
    print(f"WHERE activa = 'T': {count2} resultados ← ESTE FUNCIONA")
    
    # Con = True
    cursor.execute("""
        SELECT COUNT(*) FROM remesas_diarias
        WHERE fecha = '2025-11-22' AND activa = True
    """)
    count3 = cursor.fetchone()[0]
    print(f"WHERE activa = True: {count3} resultados")
    
    # 3. Aplicar fix
    print("\n" + "=" * 70)
    print("\n3️⃣ APLICAR CORRECCIÓN:")
    print("-" * 70)
    
    print("\nOpción 1: Cambiar el controlador para usar activa = 'T'")
    print("Opción 2: Cambiar los datos para usar activa = 1")
    
    print("\n💡 RECOMENDACIÓN: Cambiar el controlador")
    print("   Es más seguro y no afecta los datos existentes")
    
    # 4. Mostrar el fix necesario
    print("\n" + "=" * 70)
    print("\n4️⃣ FIX NECESARIO EN EL CONTROLADOR:")
    print("-" * 70)
    
    print("""
En controllers/remesas.py, función obtener_disponibilidad_moneda():

CAMBIAR:
    remesas = db((db.remesas_diarias.fecha == fecha) & 
                 (db.remesas_diarias.moneda == moneda) &
                 (db.remesas_diarias.activa == True)).select()

POR:
    remesas = db((db.remesas_diarias.fecha == fecha) & 
                 (db.remesas_diarias.moneda == moneda) &
                 (db.remesas_diarias.activa == 'T')).select()

O MEJOR AÚN (más robusto):
    remesas = db((db.remesas_diarias.fecha == fecha) & 
                 (db.remesas_diarias.moneda == moneda)).select()
    # Y filtrar solo las activas en Python si es necesario
    """)
    
    # 5. Verificar si el fix funciona
    print("\n" + "=" * 70)
    print("\n5️⃣ VERIFICAR QUE EL FIX FUNCIONARÁ:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT monto_recibido, monto_disponible, monto_vendido
        FROM remesas_diarias
        WHERE fecha = '2025-11-22' AND moneda = 'USD' AND activa = 'T'
    """)
    
    rows = cursor.fetchall()
    
    suma_disponible = sum([float(r[1]) for r in rows]) if rows else 0
    
    print(f"\nCon activa = 'T':")
    print(f"  Remesas encontradas: {len(rows)}")
    print(f"  Suma disponible: ${suma_disponible:,.2f}")
    
    if suma_disponible == 500.0:
        print("\n✅ ¡PERFECTO! Con este fix mostrará $500.00")
    
    print("\n" + "=" * 70)
    
    conn.close()

if __name__ == '__main__':
    try:
        fix_campo_activa()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
