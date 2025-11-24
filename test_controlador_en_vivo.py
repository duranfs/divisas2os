# -*- coding: utf-8 -*-
"""
Test del controlador en vivo - Simular lo que hace el dashboard
"""

import sys
import os

# Agregar el path de web2py
sys.path.insert(0, 'C:/web2py')

def test_controlador():
    print("=" * 70)
    print("TEST: SIMULAR FUNCIÓN obtener_disponibilidad_moneda()")
    print("=" * 70)
    
    # Importar módulos necesarios
    from gluon import DAL, Field
    from datetime import datetime
    
    # Conectar a la base de datos
    db = DAL('sqlite://storage.sqlite', folder='databases')
    
    # Definir tabla remesas_diarias
    db.define_table('remesas_diarias',
        Field('fecha', 'date'),
        Field('moneda', 'string'),
        Field('monto_recibido', 'decimal(15,2)'),
        Field('monto_disponible', 'decimal(15,2)'),
        Field('monto_vendido', 'decimal(15,2)'),
        Field('activa', 'string')
    )
    
    fecha = datetime.now().date()
    moneda = 'USD'
    
    print(f"\n📅 Fecha: {fecha}")
    print(f"💱 Moneda: {moneda}\n")
    
    # Test 1: Con activa == True (el código viejo)
    print("1️⃣ TEST CON activa == True (código viejo):")
    print("-" * 70)
    
    try:
        remesas_true = db((db.remesas_diarias.fecha == fecha) & 
                         (db.remesas_diarias.moneda == moneda) &
                         (db.remesas_diarias.activa == True)).select()
        
        total_true = sum([float(r.monto_disponible) for r in remesas_true]) if remesas_true else 0
        print(f"Remesas encontradas: {len(remesas_true)}")
        print(f"Total disponible: ${total_true:,.2f}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Con activa == 'T' (el código nuevo)
    print("\n2️⃣ TEST CON activa == 'T' (código nuevo):")
    print("-" * 70)
    
    try:
        remesas_t = db((db.remesas_diarias.fecha == fecha) & 
                      (db.remesas_diarias.moneda == moneda) &
                      (db.remesas_diarias.activa == 'T')).select()
        
        total_t = sum([float(r.monto_disponible) for r in remesas_t]) if remesas_t else 0
        print(f"Remesas encontradas: {len(remesas_t)}")
        print(f"Total disponible: ${total_t:,.2f}")
        
        if len(remesas_t) > 0:
            print("\nDetalle de remesas:")
            for i, r in enumerate(remesas_t, 1):
                print(f"  Remesa {i}: ${float(r.monto_disponible):,.2f}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Sin filtro de activa
    print("\n3️⃣ TEST SIN FILTRO DE ACTIVA:")
    print("-" * 70)
    
    try:
        remesas_all = db((db.remesas_diarias.fecha == fecha) & 
                        (db.remesas_diarias.moneda == moneda)).select()
        
        print(f"Remesas encontradas: {len(remesas_all)}")
        
        if len(remesas_all) > 0:
            print("\nDetalle de todas las remesas:")
            for i, r in enumerate(remesas_all, 1):
                print(f"  Remesa {i}:")
                print(f"    Disponible: ${float(r.monto_disponible):,.2f}")
                print(f"    Activa: '{r.activa}' (tipo: {type(r.activa)})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Conclusión
    print("\n" + "=" * 70)
    print("\nCONCLUSIÓN:")
    print("-" * 70)
    
    if total_t == 500.0:
        print("\n✅ El código con activa == 'T' funciona correctamente")
        print("   Pero el dashboard sigue mostrando $100")
        print("\n🔍 POSIBLES CAUSAS:")
        print("   1. El servidor no recargó los cambios")
        print("   2. Hay caché en el navegador")
        print("   3. El controlador tiene un error de sintaxis")
        print("   4. Hay otro lugar en el código que no corregimos")
    else:
        print(f"\n❌ El código con activa == 'T' no funciona: ${total_t:,.2f}")
    
    print("\n" + "=" * 70)
    
    db.close()

if __name__ == '__main__':
    try:
        test_controlador()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
