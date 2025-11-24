# -*- coding: utf-8 -*-
"""
Diagnosticar qué está pasando realmente en el dashboard
"""

import sqlite3
from datetime import datetime

def diagnosticar():
    print("=" * 70)
    print("DIAGNÓSTICO: ¿POR QUÉ EL DASHBOARD MUESTRA $100?")
    print("=" * 70)
    
    conn = sqlite3.connect('databases/storage.sqlite')
    cursor = conn.cursor()
    
    fecha_hoy = datetime.now().date().isoformat()
    
    print(f"\n📅 Fecha: {fecha_hoy}\n")
    
    # 1. Ver TODAS las remesas de USD
    print("1️⃣ TODAS LAS REMESAS DE USD (sin filtros):")
    print("-" * 70)
    
    cursor.execute("""
        SELECT id, fecha, monto_disponible, activa
        FROM remesas_diarias
        WHERE moneda = 'USD'
        ORDER BY id DESC
        LIMIT 10
    """)
    
    todas = cursor.fetchall()
    
    for remesa in todas:
        id_r, fecha, disponible, activa = remesa
        print(f"ID {id_r}: Fecha={fecha}, Disponible=${disponible:,.2f}, Activa='{activa}'")
    
    # 2. Remesas de HOY con activa = 'T'
    print("\n" + "=" * 70)
    print("\n2️⃣ REMESAS DE HOY CON activa = 'T':")
    print("-" * 70)
    
    cursor.execute("""
        SELECT id, monto_disponible
        FROM remesas_diarias
        WHERE fecha = ? AND moneda = 'USD' AND activa = 'T'
    """, (fecha_hoy,))
    
    remesas_t = cursor.fetchall()
    total_t = sum([r[1] for r in remesas_t])
    
    print(f"Cantidad: {len(remesas_t)}")
    print(f"Total: ${total_t:,.2f}")
    
    for remesa in remesas_t:
        print(f"  ID {remesa[0]}: ${remesa[1]:,.2f}")
    
    # 3. ¿Hay remesas con activa = 1 o True?
    print("\n" + "=" * 70)
    print("\n3️⃣ ¿HAY REMESAS CON activa = 1 o True?")
    print("-" * 70)
    
    cursor.execute("""
        SELECT id, monto_disponible, activa
        FROM remesas_diarias
        WHERE fecha = ? AND moneda = 'USD' AND (activa = 1 OR activa = 'True')
    """, (fecha_hoy,))
    
    remesas_1 = cursor.fetchall()
    
    if remesas_1:
        print(f"⚠️  SÍ, hay {len(remesas_1)} remesas con activa = 1 o True")
        for r in remesas_1:
            print(f"  ID {r[0]}: ${r[1]:,.2f}, activa='{r[2]}'")
    else:
        print("✅ No hay remesas con activa = 1 o True")
    
    # 4. Ver si hay límites configurados
    print("\n" + "=" * 70)
    print("\n4️⃣ LÍMITES CONFIGURADOS:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT id, limite_diario, monto_disponible, activo
        FROM limites_venta
        WHERE fecha = ? AND moneda = 'USD'
        ORDER BY id DESC
    """, (fecha_hoy,))
    
    limites = cursor.fetchall()
    
    if limites:
        print(f"Hay {len(limites)} límites:")
        for limite in limites:
            id_l, limite_diario, disponible, activo = limite
            estado = "ACTIVO" if activo else "INACTIVO"
            print(f"  ID {id_l}: Límite=${limite_diario:,.2f}, Disponible=${disponible:,.2f}, {estado}")
    else:
        print("No hay límites configurados")
    
    # 5. HIPÓTESIS
    print("\n" + "=" * 70)
    print("\n5️⃣ HIPÓTESIS:")
    print("-" * 70)
    
    if total_t == 500.0:
        print("\n✅ Los datos en BD son correctos: $500.00")
        print("\n🔍 El problema está en:")
        print("   A) El servidor web2py no recargó el código")
        print("   B) Hay caché en el navegador")
        print("   C) La vista está mostrando otro valor")
        print("\n💡 SOLUCIONES:")
        print("   1. DETÉN el servidor web2py completamente")
        print("   2. Espera 5 segundos")
        print("   3. Inicia el servidor de nuevo")
        print("   4. Abre el navegador en modo incógnito")
        print("   5. Ve a la página de remesas")
    elif total_t == 100.0:
        print("\n⚠️  Solo encuentra UNA remesa de $100")
        print("   Esto significa que el filtro activa = 'T' no funciona")
        print("   o hay un problema con las fechas")
    else:
        print(f"\n❓ Total inesperado: ${total_t:,.2f}")
    
    # 6. Ver el valor exacto de activa en bytes
    print("\n" + "=" * 70)
    print("\n6️⃣ VALOR EXACTO DEL CAMPO 'ACTIVA':")
    print("-" * 70)
    
    cursor.execute("""
        SELECT id, activa, hex(activa), length(activa)
        FROM remesas_diarias
        WHERE fecha = ? AND moneda = 'USD'
    """, (fecha_hoy,))
    
    valores = cursor.fetchall()
    
    for v in valores:
        id_r, activa, hex_val, length = v
        print(f"ID {id_r}: '{activa}' (hex: {hex_val}, length: {length})")
    
    print("\n" + "=" * 70)
    
    conn.close()

if __name__ == '__main__':
    try:
        diagnosticar()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
