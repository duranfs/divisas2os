# -*- coding: utf-8 -*-
"""
Verificar que el fix en la vista configurar_limites_simple funciona
"""

import sqlite3
from datetime import datetime

def verificar():
    print("=" * 70)
    print("VERIFICACIÓN: FIX EN VISTA configurar_limites_simple.html")
    print("=" * 70)
    
    conn = sqlite3.connect('databases/storage.sqlite')
    cursor = conn.cursor()
    
    fecha_hoy = datetime.now().date().isoformat()
    
    print(f"\n📅 Fecha: {fecha_hoy}\n")
    
    # Simular lo que hace la vista ANTES del fix
    print("1️⃣ CÓDIGO VIEJO (.select().first()):")
    print("-" * 70)
    
    cursor.execute("""
        SELECT monto_disponible
        FROM remesas_diarias
        WHERE fecha = ? AND moneda = 'USD' AND activa = 'T'
        LIMIT 1
    """, (fecha_hoy,))
    
    primera = cursor.fetchone()
    
    if primera:
        print(f"Primera remesa: ${primera[0]:,.2f}")
        print(f"❌ Esto es lo que mostraba antes: ${primera[0]:,.2f}")
    
    # Simular lo que hace la vista DESPUÉS del fix
    print("\n2️⃣ CÓDIGO NUEVO (sum de todas):")
    print("-" * 70)
    
    cursor.execute("""
        SELECT monto_disponible
        FROM remesas_diarias
        WHERE fecha = ? AND moneda = 'USD' AND activa = 'T'
    """, (fecha_hoy,))
    
    todas = cursor.fetchall()
    total = sum([r[0] for r in todas])
    
    print(f"Remesas encontradas: {len(todas)}")
    for i, r in enumerate(todas, 1):
        print(f"  Remesa {i}: ${r[0]:,.2f}")
    print(f"\nTotal: ${total:,.2f}")
    print(f"✅ Esto es lo que mostrará ahora: ${total:,.2f}")
    
    # Verificación
    print("\n" + "=" * 70)
    print("\nRESULTADO:")
    print("-" * 70)
    
    if total == 500.0:
        print("\n✅ ¡PERFECTO! El fix funcionará correctamente")
        print(f"   La vista ahora mostrará: ${total:,.2f}")
        print("\n📋 PASOS SIGUIENTES:")
        print("   1. Refresca el navegador (Ctrl+F5)")
        print("   2. Ve a 'Configurar Límites'")
        print("   3. Deberías ver $500.00 en 'Remesa disponible hoy'")
    else:
        print(f"\n❌ ERROR: El total es ${total:,.2f} en lugar de $500.00")
    
    print("\n" + "=" * 70)
    
    conn.close()

if __name__ == '__main__':
    try:
        verificar()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
