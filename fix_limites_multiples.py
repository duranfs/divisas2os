#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Corregir problema de múltiples límites activos
"""

import sqlite3
from datetime import datetime

def fix_limites():
    """Limpiar límites duplicados y dejar solo el más reciente"""
    
    print("🔧 CORRIGIENDO LÍMITES MÚLTIPLES")
    print("="*70)
    
    try:
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        fecha_hoy = datetime.now().date().strftime('%Y-%m-%d')
        
        # 1. Ver límites actuales
        print("\n📊 LÍMITES ACTUALES DE USD:")
        cursor.execute("""
            SELECT id, limite_diario, monto_vendido, monto_disponible, activo
            FROM limites_venta 
            WHERE fecha = ? AND moneda = 'USD'
            ORDER BY id DESC
        """, (fecha_hoy,))
        
        limites = cursor.fetchall()
        
        for limite in limites:
            lid, limite_diario, vendido, disponible, activo = limite
            estado = "✅ ACTIVO" if activo else "❌ INACTIVO"
            print(f"   ID:{lid} | Límite ${limite_diario:,.2f} | Disponible ${disponible:,.2f} | {estado}")
        
        # 2. Desactivar TODOS los límites de USD para hoy
        print("\n🔧 Desactivando todos los límites de USD...")
        cursor.execute("""
            UPDATE limites_venta 
            SET activo = 0
            WHERE fecha = ? AND moneda = 'USD'
        """, (fecha_hoy,))
        
        print(f"   ✅ {cursor.rowcount} límites desactivados")
        
        # 3. Activar solo el más reciente con monto_disponible > 0
        print("\n🔧 Activando solo el límite más reciente válido...")
        cursor.execute("""
            SELECT id, limite_diario, monto_disponible
            FROM limites_venta 
            WHERE fecha = ? AND moneda = 'USD' AND monto_disponible > 0
            ORDER BY id DESC
            LIMIT 1
        """, (fecha_hoy,))
        
        limite_valido = cursor.fetchone()
        
        if limite_valido:
            lid, limite_diario, disponible = limite_valido
            
            cursor.execute("""
                UPDATE limites_venta 
                SET activo = 1
                WHERE id = ?
            """, (lid,))
            
            print(f"   ✅ Límite ID:{lid} activado")
            print(f"   Límite diario: ${limite_diario:,.2f}")
            print(f"   Disponible: ${disponible:,.2f}")
        else:
            print("   ⚠️  No hay límites válidos, creando uno nuevo...")
            
            # Crear límite de $200 por defecto
            cursor.execute("""
                INSERT INTO limites_venta 
                (fecha, moneda, limite_diario, monto_vendido, monto_disponible, 
                 porcentaje_utilizado, activo, alerta_80_enviada, alerta_95_enviada)
                VALUES (?, 'USD', 200.00, 0.00, 200.00, 0.0, 1, 0, 0)
            """, (fecha_hoy,))
            
            print("   ✅ Nuevo límite de $200 USD creado")
        
        conn.commit()
        
        # 4. Verificar resultado final
        print("\n✅ RESULTADO FINAL:")
        cursor.execute("""
            SELECT id, limite_diario, monto_vendido, monto_disponible, 
                   porcentaje_utilizado, activo
            FROM limites_venta 
            WHERE fecha = ? AND moneda = 'USD' AND activo = 1
        """, (fecha_hoy,))
        
        limite_final = cursor.fetchone()
        
        if limite_final:
            lid, limite_diario, vendido, disponible, porcentaje, activo = limite_final
            print(f"   ID: {lid}")
            print(f"   Límite diario: ${limite_diario:,.2f}")
            print(f"   Monto vendido: ${vendido:,.2f}")
            print(f"   Monto disponible: ${disponible:,.2f}")
            print(f"   Porcentaje usado: {porcentaje:.1f}%")
            print(f"   Estado: {'✅ ACTIVO' if activo else '❌ INACTIVO'}")
        
        conn.close()
        
        print("\n" + "="*70)
        print("✅ CORRECCIÓN COMPLETADA")
        print("="*70)
        print()
        print("🎯 Ahora intenta comprar $70 USD de nuevo")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    fix_limites()
