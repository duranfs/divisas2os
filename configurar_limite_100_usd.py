#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configurar límite de $100 USD para pruebas
"""

import sqlite3
from datetime import datetime

def configurar_limite_prueba():
    """Configurar límite de $100 USD"""
    
    print("🔧 CONFIGURANDO LÍMITE DE PRUEBA: $100 USD")
    print("="*70)
    
    try:
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        fecha_hoy = datetime.now().date().strftime('%Y-%m-%d')
        
        # Desactivar límites anteriores de USD para hoy
        cursor.execute("""
            UPDATE limites_venta 
            SET activo = 0
            WHERE fecha = ? AND moneda = 'USD'
        """, (fecha_hoy,))
        
        print(f"   ✅ Límites anteriores de USD desactivados")
        
        # Crear nuevo límite de $100
        cursor.execute("""
            INSERT INTO limites_venta 
            (moneda, limite_diario, monto_vendido, monto_disponible, 
             porcentaje_utilizado, activo, fecha, alerta_80_enviada, alerta_95_enviada)
            VALUES ('USD', 100.00, 0.00, 100.00, 0.0, 1, ?, 0, 0)
        """, (fecha_hoy,))
        
        print(f"   ✅ Nuevo límite de $100 USD creado para {fecha_hoy}")
        
        # Verificar que existe remesa
        cursor.execute("""
            SELECT COUNT(*) FROM remesas_diarias 
            WHERE fecha = ? AND moneda = 'USD' AND activa = 1
        """, (fecha_hoy,))
        
        tiene_remesa = cursor.fetchone()[0] > 0
        
        if not tiene_remesa:
            print(f"   ⚠️  No hay remesa de USD para hoy, creando una...")
            cursor.execute("""
                INSERT INTO remesas_diarias 
                (moneda, monto_recibido, monto_disponible, monto_vendido, 
                 fecha, activa, origen, numero_referencia)
                VALUES ('USD', 10000.00, 10000.00, 0.00, ?, 1, 'PRUEBA', 'TEST-LIMITE')
            """, (fecha_hoy,))
            print(f"   ✅ Remesa de $10,000 USD creada")
        
        conn.commit()
        conn.close()
        
        print("\n" + "="*70)
        print("✅ CONFIGURACIÓN COMPLETADA")
        print("="*70)
        print()
        print("📊 LÍMITE CONFIGURADO:")
        print("   Moneda: USD")
        print("   Límite diario: $100.00")
        print("   Disponible: $100.00")
        print("   Fecha: " + fecha_hoy)
        print()
        print("🧪 PRUEBAS SUGERIDAS:")
        print()
        print("1. Reinicia el servidor web2py")
        print()
        print("2. Intenta comprar $150 USD:")
        print("   ❌ Debe rechazar con mensaje:")
        print("   'Venta rechazada: Venta de $150.00 excede límite disponible de $100.00'")
        print()
        print("3. Intenta comprar $50 USD:")
        print("   ✅ Debe permitir la compra")
        print("   ✅ Límite debe actualizarse a: $50 vendidos, $50 disponibles")
        print()
        print("4. Intenta comprar otros $60 USD:")
        print("   ❌ Debe rechazar con mensaje:")
        print("   'Venta rechazada: Venta de $60.00 excede límite disponible de $50.00'")
        print()
        print("5. Intenta comprar $40 USD:")
        print("   ✅ Debe permitir la compra")
        print("   ✅ Límite debe actualizarse a: $90 vendidos, $10 disponibles")
        print()
        print("6. Intenta comprar $15 USD:")
        print("   ❌ Debe rechazar (excede límite)")
        print()
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    configurar_limite_prueba()
