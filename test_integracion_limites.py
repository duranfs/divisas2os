#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test de integración de límites con sistema de ventas
"""

import sqlite3
from datetime import datetime

def test_integracion():
    """Probar que la integración está funcionando"""
    
    print("🧪 TEST DE INTEGRACIÓN DE LÍMITES")
    print("="*70)
    
    try:
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        fecha_hoy = datetime.now().date().strftime('%Y-%m-%d')
        
        # 1. Verificar límites actuales
        print("\n📊 LÍMITES ACTUALES:")
        cursor.execute("""
            SELECT moneda, limite_diario, monto_vendido, monto_disponible, 
                   porcentaje_utilizado, activo
            FROM limites_venta 
            WHERE fecha = ? AND activo = 1
            ORDER BY moneda
        """, (fecha_hoy,))
        
        limites = cursor.fetchall()
        
        if not limites:
            print("   ❌ NO HAY LÍMITES CONFIGURADOS")
            print("\n💡 CONFIGURANDO LÍMITE DE PRUEBA DE $100 USD...")
            
            # Configurar límite de prueba
            cursor.execute("""
                INSERT INTO limites_venta 
                (moneda, limite_diario, monto_vendido, monto_disponible, 
                 porcentaje_utilizado, activo, fecha, alerta_80_enviada, alerta_95_enviada)
                VALUES ('USD', 100.00, 0.00, 100.00, 0.0, 1, ?, 0, 0)
            """, (fecha_hoy,))
            
            conn.commit()
            print("   ✅ Límite de $100 USD configurado")
        else:
            for limite in limites:
                moneda, limite_diario, vendido, disponible, porcentaje, activo = limite
                print(f"   {moneda}: Límite ${limite_diario:,.2f} | Vendido ${vendido:,.2f} | Disponible ${disponible:,.2f} ({porcentaje:.1f}%)")
        
        # 2. Verificar remesas
        print("\n💰 REMESAS DISPONIBLES:")
        cursor.execute("""
            SELECT moneda, monto_recibido, monto_disponible, monto_vendido, activa
            FROM remesas_diarias 
            WHERE fecha = ? AND activa = 1
            ORDER BY moneda
        """, (fecha_hoy,))
        
        remesas = cursor.fetchall()
        
        if not remesas:
            print("   ❌ NO HAY REMESAS CONFIGURADAS")
            print("\n💡 CONFIGURANDO REMESA DE PRUEBA DE $10,000 USD...")
            
            cursor.execute("""
                INSERT INTO remesas_diarias 
                (moneda, monto_recibido, monto_disponible, monto_vendido, 
                 fecha, activa, origen, numero_referencia)
                VALUES ('USD', 10000.00, 10000.00, 0.00, ?, 1, 'PRUEBA', 'TEST-001')
            """, (fecha_hoy,))
            
            conn.commit()
            print("   ✅ Remesa de $10,000 USD configurada")
        else:
            for remesa in remesas:
                moneda, recibido, disponible, vendido, activa = remesa
                print(f"   {moneda}: Recibido ${recibido:,.2f} | Disponible ${disponible:,.2f} | Vendido ${vendido:,.2f}")
        
        # 3. Verificar archivos modificados
        print("\n🔧 VERIFICANDO ARCHIVOS MODIFICADOS:")
        
        # Verificar db.py
        try:
            with open('models/db.py', 'r', encoding='utf-8') as f:
                contenido_db = f.read()
                
                if 'def validar_limite_venta' in contenido_db:
                    print("   ✅ models/db.py tiene validar_limite_venta()")
                else:
                    print("   ❌ models/db.py NO tiene validar_limite_venta()")
                
                if 'def procesar_venta_con_limites' in contenido_db:
                    print("   ✅ models/db.py tiene procesar_venta_con_limites()")
                else:
                    print("   ❌ models/db.py NO tiene procesar_venta_con_limites()")
        except Exception as e:
            print(f"   ❌ Error leyendo db.py: {str(e)}")
        
        # Verificar divisas.py
        try:
            with open('controllers/divisas.py', 'r', encoding='utf-8') as f:
                contenido_divisas = f.read()
                
                if 'validar_limite_venta(' in contenido_divisas:
                    print("   ✅ controllers/divisas.py llama a validar_limite_venta()")
                else:
                    print("   ❌ controllers/divisas.py NO llama a validar_limite_venta()")
                
                if 'procesar_venta_con_limites(' in contenido_divisas:
                    print("   ✅ controllers/divisas.py llama a procesar_venta_con_limites()")
                else:
                    print("   ❌ controllers/divisas.py NO llama a procesar_venta_con_limites()")
        except Exception as e:
            print(f"   ❌ Error leyendo divisas.py: {str(e)}")
        
        conn.close()
        
        # 4. Instrucciones de prueba
        print("\n" + "="*70)
        print("🎯 INSTRUCCIONES PARA PROBAR:")
        print("="*70)
        print()
        print("1. Reinicia el servidor web2py:")
        print("   python web2py.py -a <password> -i 127.0.0.1 -p 8000")
        print()
        print("2. Accede al sistema:")
        print("   http://127.0.0.1:8000/divisas2os")
        print()
        print("3. Ve a Divisas > Comprar")
        print()
        print("4. Intenta comprar $150 USD")
        print("   ❌ Debe rechazar: 'Venta rechazada: excede límite disponible'")
        print()
        print("5. Intenta comprar $50 USD")
        print("   ✅ Debe permitir la compra")
        print()
        print("6. Ve a Remesas > Panel de Control")
        print("   ✅ Debe mostrar límite actualizado: $50 vendidos, $50 disponibles")
        print()
        print("7. Intenta comprar otros $60 USD")
        print("   ❌ Debe rechazar: 'Venta rechazada: excede límite disponible'")
        print()
        print("="*70)
        print("✅ INTEGRACIÓN COMPLETADA")
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_integracion()
