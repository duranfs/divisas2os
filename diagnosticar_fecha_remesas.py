# -*- coding: utf-8 -*-
"""
Diagnosticar problema con fechas en remesas
"""

import sqlite3
from datetime import datetime, date

def diagnosticar_fechas():
    print("=" * 70)
    print("DIAGNÓSTICO: FORMATO DE FECHAS EN REMESAS")
    print("=" * 70)
    
    conn = sqlite3.connect('databases/storage.sqlite')
    cursor = conn.cursor()
    
    # 1. Ver todas las remesas y sus fechas
    print("\n1️⃣ TODAS LAS REMESAS EN LA BASE DE DATOS:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT id, fecha, moneda, monto_disponible, activa
        FROM remesas_diarias
        ORDER BY id DESC
        LIMIT 10
    """)
    
    remesas = cursor.fetchall()
    
    for remesa in remesas:
        id_r, fecha, moneda, disponible, activa = remesa
        print(f"\nID {id_r}:")
        print(f"  Fecha: '{fecha}' (tipo: {type(fecha)})")
        print(f"  Moneda: {moneda}")
        print(f"  Disponible: ${disponible:,.2f}")
        print(f"  Activa: {activa}")
    
    # 2. Probar diferentes formatos de fecha
    print("\n" + "=" * 70)
    print("\n2️⃣ PROBAR DIFERENTES FORMATOS DE FECHA:")
    print("-" * 70)
    
    # Formato 1: ISO string
    fecha_iso = datetime.now().date().isoformat()
    print(f"\nFormato ISO: '{fecha_iso}'")
    cursor.execute("""
        SELECT COUNT(*) FROM remesas_diarias
        WHERE fecha = ? AND moneda = 'USD' AND activa = 1
    """, (fecha_iso,))
    count1 = cursor.fetchone()[0]
    print(f"  Resultados: {count1}")
    
    # Formato 2: Date object
    fecha_date = datetime.now().date()
    print(f"\nFormato date(): '{fecha_date}'")
    cursor.execute("""
        SELECT COUNT(*) FROM remesas_diarias
        WHERE fecha = ? AND moneda = 'USD' AND activa = 1
    """, (str(fecha_date),))
    count2 = cursor.fetchone()[0]
    print(f"  Resultados: {count2}")
    
    # Formato 3: Sin filtro de fecha, solo ver qué hay
    print(f"\nSin filtro de fecha:")
    cursor.execute("""
        SELECT COUNT(*) FROM remesas_diarias
        WHERE moneda = 'USD' AND activa = 1
    """)
    count3 = cursor.fetchone()[0]
    print(f"  Resultados: {count3}")
    
    # 3. Ver el tipo de dato de la columna fecha
    print("\n" + "=" * 70)
    print("\n3️⃣ ESTRUCTURA DE LA TABLA:")
    print("-" * 70)
    
    cursor.execute("PRAGMA table_info(remesas_diarias)")
    columns = cursor.fetchall()
    
    for col in columns:
        if 'fecha' in col[1].lower():
            print(f"\nColumna: {col[1]}")
            print(f"  Tipo: {col[2]}")
            print(f"  Not Null: {col[3]}")
            print(f"  Default: {col[4]}")
    
    # 4. Ver las fechas únicas en la tabla
    print("\n" + "=" * 70)
    print("\n4️⃣ FECHAS ÚNICAS EN LA TABLA:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT DISTINCT fecha, COUNT(*) as cantidad
        FROM remesas_diarias
        GROUP BY fecha
        ORDER BY fecha DESC
        LIMIT 5
    """)
    
    fechas = cursor.fetchall()
    
    for fecha, cantidad in fechas:
        print(f"\nFecha: '{fecha}'")
        print(f"  Cantidad de remesas: {cantidad}")
        print(f"  Tipo en Python: {type(fecha)}")
        print(f"  Longitud: {len(str(fecha))}")
        print(f"  Repr: {repr(fecha)}")
    
    # 5. Intentar buscar con LIKE
    print("\n" + "=" * 70)
    print("\n5️⃣ BUSCAR CON LIKE:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT id, fecha, moneda, monto_disponible
        FROM remesas_diarias
        WHERE fecha LIKE '2025-11-22%' AND moneda = 'USD' AND activa = 1
    """)
    
    resultados = cursor.fetchall()
    print(f"\nResultados con LIKE '2025-11-22%': {len(resultados)}")
    
    for r in resultados:
        print(f"  ID {r[0]}: {r[1]} - {r[2]} - ${r[3]:,.2f}")
    
    print("\n" + "=" * 70)
    
    conn.close()

if __name__ == '__main__':
    try:
        diagnosticar_fechas()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
