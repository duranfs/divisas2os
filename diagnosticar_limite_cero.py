#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Diagnosticar por qué el límite muestra $0.00
"""

import sqlite3
from datetime import datetime

def diagnosticar():
    """Diagnosticar el problema del límite en $0.00"""
    
    print("🔍 DIAGNÓSTICO: LÍMITE EN $0.00")
    print("="*70)
    
    try:
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        fecha_hoy = datetime.now().date().strftime('%Y-%m-%d')
        
        # 1. Ver TODOS los límites de USD (activos e inactivos)
        print("\n📊 TODOS LOS LÍMITES DE USD PARA HOY:")
        cursor.execute("""
            SELECT id, moneda, limite_diario, monto_vendido, monto_disponible, 
                   porcentaje_utilizado, activo
            FROM limites_venta 
            WHERE fecha = ? AND moneda = 'USD'
            ORDER BY id DESC
        """, (fecha_hoy,))
        
        limites = cursor.fetchall()
        
        if limites:
            for limite in limites:
                lid, moneda, limite_diario, vendido, disponible, porcentaje, activo = limite
                estado = "✅ ACTIVO" if activo else "❌ INACTIVO"
                print(f"   ID:{lid} | Límite ${limite_diario:,.2f} | Vendido ${vendido:,.2f} | Disponible ${disponible:,.2f} | {estado}")
        else:
            print("   ❌ NO HAY LÍMITES DE USD")
        
        # 2. Ver cuál límite está usando la validación
        print("\n🔍 LÍMITE QUE USA LA VALIDACIÓN:")
        cursor.execute("""
            SELECT id, limite_diario, monto_vendido, monto_disponible, activo
            FROM limites_venta 
            WHERE fecha = ? AND moneda = 'USD' AND activo = 1
            ORDER BY id DESC
            LIMIT 1
        """, (fecha_hoy,))
        
        limite_activo = cursor.fetchone()
        
        if limite_activo:
            lid, limite_diario, vendido, disponible, activo = limite_activo
            print(f"   ID:{lid} | Límite ${limite_diario:,.2f} | Vendido ${vendido:,.2f} | Disponible ${disponible:,.2f}")
            
            if disponible == 0:
                print("\n   ⚠️  PROBLEMA ENCONTRADO:")
                print(f"   El límite activo tiene monto_disponible = $0.00")
                print(f"   Pero el límite_diario es ${limite_diario:,.2f}")
                print()
                print("   🔧 POSIBLES CAUSAS:")
                print("   1. El límite se configuró con monto_disponible = 0")
                print("   2. Ya se vendió todo el límite")
                print("   3. Error en el cálculo al configurar")
        else:
            print("   ❌ NO HAY LÍMITE ACTIVO")
        
        # 3. Ver remesas
        print("\n💰 REMESAS DE USD:")
        cursor.execute("""
            SELECT id, monto_recibido, monto_disponible, monto_vendido, activa
            FROM remesas_diarias 
            WHERE fecha = ? AND moneda = 'USD'
            ORDER BY id DESC
        """, (fecha_hoy,))
        
        remesas = cursor.fetchall()
        
        if remesas:
            for remesa in remesas:
                rid, recibido, disponible, vendido, activa = remesa
                estado = "✅ ACTIVA" if activa else "❌ INACTIVA"
                print(f"   ID:{rid} | Recibido ${recibido:,.2f} | Disponible ${disponible:,.2f} | Vendido ${vendido:,.2f} | {estado}")
        else:
            print("   ❌ NO HAY REMESAS")
        
        # 4. Solución
        print("\n" + "="*70)
        print("🔧 SOLUCIÓN:")
        print("="*70)
        
        if limite_activo and disponible == 0 and limite_diario > 0:
            print()
            print("El problema es que el límite tiene monto_disponible = $0.00")
            print()
            print("Voy a corregirlo automáticamente...")
            
            # Corregir el límite
            cursor.execute("""
                UPDATE limites_venta 
                SET monto_disponible = limite_diario - monto_vendido,
                    porcentaje_utilizado = (monto_vendido / limite_diario * 100)
                WHERE id = ?
            """, (lid,))
            
            conn.commit()
            
            # Verificar corrección
            cursor.execute("""
                SELECT limite_diario, monto_vendido, monto_disponible, porcentaje_utilizado
                FROM limites_venta 
                WHERE id = ?
            """, (lid,))
            
            corregido = cursor.fetchone()
            limite_diario, vendido, disponible, porcentaje = corregido
            
            print()
            print("✅ LÍMITE CORREGIDO:")
            print(f"   Límite diario: ${limite_diario:,.2f}")
            print(f"   Monto vendido: ${vendido:,.2f}")
            print(f"   Monto disponible: ${disponible:,.2f}")
            print(f"   Porcentaje: {porcentaje:.1f}%")
            print()
            print("🎯 Ahora intenta comprar de nuevo!")
        
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    diagnosticar()
