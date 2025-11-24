# -*- coding: utf-8 -*-
"""
Diagnosticar el campo 'activo' en limites_venta
"""

import sqlite3
from datetime import datetime

def diagnosticar():
    print("=" * 70)
    print("DIAGNÓSTICO: CAMPO 'ACTIVO' EN LIMITES_VENTA")
    print("=" * 70)
    
    conn = sqlite3.connect('databases/storage.sqlite')
    cursor = conn.cursor()
    
    fecha_hoy = datetime.now().date().isoformat()
    
    # 1. Ver todos los límites
    print(f"\n📅 Fecha: {fecha_hoy}\n")
    print("1️⃣ TODOS LOS LÍMITES:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT id, fecha, moneda, limite_diario, activo, typeof(activo)
        FROM limites_venta
        ORDER BY id DESC
        LIMIT 10
    """)
    
    limites = cursor.fetchall()
    
    if limites:
        for limite in limites:
            id_l, fecha, moneda, limite_diario, activo, tipo = limite
            print(f"\nID {id_l}:")
            print(f"  Fecha: {fecha}")
            print(f"  Moneda: {moneda}")
            print(f"  Límite: ${limite_diario:,.2f}")
            print(f"  Activo: '{activo}' (tipo: {tipo})")
    else:
        print("No hay límites en la base de datos")
    
    # 2. Probar consultas
    print("\n" + "=" * 70)
    print("\n2️⃣ PROBAR CONSULTAS:")
    print("-" * 70)
    
    # Con activo = 1
    cursor.execute("""
        SELECT COUNT(*) FROM limites_venta
        WHERE fecha = ? AND activo = 1
    """, (fecha_hoy,))
    count1 = cursor.fetchone()[0]
    print(f"\nWHERE activo = 1: {count1} resultados")
    
    # Con activo = True
    cursor.execute("""
        SELECT COUNT(*) FROM limites_venta
        WHERE fecha = ? AND activo = True
    """, (fecha_hoy,))
    count2 = cursor.fetchone()[0]
    print(f"WHERE activo = True: {count2} resultados")
    
    # Con activo = 'T'
    cursor.execute("""
        SELECT COUNT(*) FROM limites_venta
        WHERE fecha = ? AND activo = 'T'
    """, (fecha_hoy,))
    count3 = cursor.fetchone()[0]
    print(f"WHERE activo = 'T': {count3} resultados")
    
    # 3. Conclusión
    print("\n" + "=" * 70)
    print("\nCONCLUSIÓN:")
    print("-" * 70)
    
    if count1 > 0:
        print(f"\n✅ Los límites usan activo = 1 (entero)")
        print("   El código del controlador está correcto con activo=True")
    elif count3 > 0:
        print(f"\n⚠️  Los límites usan activo = 'T' (texto)")
        print("   Necesitamos cambiar el código para usar activo='T'")
    else:
        print("\n❓ No hay límites activos para hoy")
    
    print("\n" + "=" * 70)
    
    conn.close()

if __name__ == '__main__':
    try:
        diagnosticar()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
