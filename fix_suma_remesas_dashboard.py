# -*- coding: utf-8 -*-
"""
Fix: Corregir suma de remesas en dashboard
El problema es que el dashboard muestra $100 en lugar de $500
"""

import sqlite3
from datetime import datetime

def verificar_y_corregir():
    print("=" * 70)
    print("DIAGNÓSTICO Y CORRECCIÓN: SUMA DE REMESAS")
    print("=" * 70)
    
    conn = sqlite3.connect('databases/storage.sqlite')
    cursor = conn.cursor()
    
    fecha_hoy = datetime.now().date().isoformat()
    
    # 1. Verificar remesas actuales
    print(f"\n📅 Fecha: {fecha_hoy}\n")
    
    cursor.execute("""
        SELECT id, moneda, monto_recibido, monto_disponible, activa
        FROM remesas_diarias
        WHERE fecha = ? AND moneda = 'USD'
        ORDER BY id
    """, (fecha_hoy,))
    
    remesas = cursor.fetchall()
    
    print("REMESAS DE USD:")
    print("-" * 70)
    
    total = 0
    for remesa in remesas:
        id_r, moneda, recibido, disponible, activa = remesa
        estado = "✅ ACTIVA" if activa else "❌ INACTIVA"
        print(f"ID {id_r}: ${disponible:,.2f} - {estado}")
        if activa:
            total += disponible
    
    print(f"\nTOTAL ESPERADO: ${total:,.2f}")
    
    # 2. Probar la consulta exacta del controlador
    print("\n" + "=" * 70)
    print("\nPRUEBA DE LA CONSULTA DEL CONTROLADOR:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT monto_recibido, monto_disponible, monto_vendido
        FROM remesas_diarias
        WHERE fecha = ? AND moneda = 'USD' AND activa = 1
    """, (fecha_hoy,))
    
    rows = cursor.fetchall()
    
    print(f"\nNúmero de remesas encontradas: {len(rows)}")
    
    suma_disponible = sum([float(r[1]) for r in rows]) if rows else 0
    
    print(f"Suma calculada: ${suma_disponible:,.2f}")
    
    # 3. Verificar si hay problema con el tipo de dato
    print("\n" + "=" * 70)
    print("\nVERIFICAR TIPOS DE DATOS:")
    print("-" * 70)
    
    for i, row in enumerate(rows, 1):
        recibido, disponible, vendido = row
        print(f"\nRemesa {i}:")
        print(f"  Valor: {disponible}")
        print(f"  Tipo: {type(disponible)}")
        print(f"  Float: {float(disponible)}")
    
    # 4. Conclusión
    print("\n" + "=" * 70)
    print("\nCONCLUSIÓN:")
    print("-" * 70)
    
    if suma_disponible == 500.0:
        print("\n✅ LA CONSULTA SQL FUNCIONA CORRECTAMENTE")
        print(f"   Suma: ${suma_disponible:,.2f}")
        print("\n🔍 El problema debe estar en:")
        print("   1. Caché del navegador (Ctrl+F5 para refrescar)")
        print("   2. El controlador no está ejecutando esta función")
        print("   3. Hay un error en el código Python del controlador")
        print("\n💡 SOLUCIÓN:")
        print("   1. Cierra el navegador completamente")
        print("   2. Reinicia el servidor web2py")
        print("   3. Abre el navegador y ve a la página de remesas")
    else:
        print(f"\n❌ LA SUMA ES INCORRECTA: ${suma_disponible:,.2f}")
        print("   Hay un problema con los datos en la base de datos")
    
    print("\n" + "=" * 70)
    
    conn.close()

if __name__ == '__main__':
    try:
        verificar_y_corregir()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
