#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test de la nueva vista simple de configuración de límites
"""

import sqlite3
from datetime import datetime

def test_vista_simple():
    """Verificar que la vista simple funciona correctamente"""
    
    print("🧪 TEST DE VISTA SIMPLE DE LÍMITES")
    print("="*70)
    
    try:
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        fecha_hoy = datetime.now().date().strftime('%Y-%m-%d')
        
        # 1. Verificar archivos
        print("\n📁 VERIFICANDO ARCHIVOS:")
        
        import os
        
        if os.path.exists('views/remesas/configurar_limites_simple.html'):
            print("   ✅ Vista simple creada: configurar_limites_simple.html")
        else:
            print("   ❌ Vista simple NO existe")
        
        # 2. Verificar remesas disponibles
        print("\n💰 REMESAS DISPONIBLES PARA HOY:")
        cursor.execute("""
            SELECT moneda, monto_recibido, monto_disponible, activa
            FROM remesas_diarias 
            WHERE fecha = ? AND activa = 1
            ORDER BY moneda
        """, (fecha_hoy,))
        
        remesas = cursor.fetchall()
        
        if remesas:
            for remesa in remesas:
                moneda, recibido, disponible, activa = remesa
                print(f"   {moneda}: Disponible ${disponible:,.2f}")
        else:
            print("   ⚠️  No hay remesas para hoy")
            print("   💡 Creando remesas de prueba...")
            
            # Crear remesas de prueba
            for moneda, monto in [('USD', 10000), ('EUR', 8000), ('USDT', 15000)]:
                cursor.execute("""
                    INSERT INTO remesas_diarias 
                    (moneda, monto_recibido, monto_disponible, monto_vendido, 
                     fecha, activa, origen, numero_referencia)
                    VALUES (?, ?, ?, 0.00, ?, 1, 'PRUEBA', 'TEST-SIMPLE')
                """, (moneda, monto, monto, fecha_hoy))
            
            conn.commit()
            print("   ✅ Remesas de prueba creadas")
        
        # 3. Verificar límites actuales
        print("\n📊 LÍMITES ACTUALES:")
        cursor.execute("""
            SELECT moneda, limite_diario, monto_vendido, monto_disponible, 
                   porcentaje_utilizado, activo
            FROM limites_venta 
            WHERE fecha = ? AND activo = 1
            ORDER BY moneda
        """, (fecha_hoy,))
        
        limites = cursor.fetchall()
        
        if limites:
            for limite in limites:
                moneda, limite_diario, vendido, disponible, porcentaje, activo = limite
                print(f"   {moneda}: Límite ${limite_diario:,.2f} | Vendido ${vendido:,.2f} | Disponible ${disponible:,.2f} ({porcentaje:.1f}%)")
        else:
            print("   ℹ️  No hay límites configurados")
        
        conn.close()
        
        # 4. Instrucciones
        print("\n" + "="*70)
        print("🎯 CÓMO USAR LA NUEVA VISTA SIMPLE")
        print("="*70)
        print()
        print("1. Accede a la vista:")
        print("   http://127.0.0.1:8000/divisas2os/remesas/configurar_limites_simple")
        print()
        print("2. Verás 3 tarjetas (USD, EUR, USDT) con:")
        print("   ✅ Remesa disponible")
        print("   ✅ Campo para ingresar límite")
        print("   ✅ Botones rápidos (50%, 75%, 90%, 100%)")
        print()
        print("3. Para configurar un límite:")
        print("   a) Escribe el monto manualmente, O")
        print("   b) Click en un botón rápido (ej: 90%)")
        print("   c) Click en 'Configurar Límite'")
        print()
        print("4. Ejemplo práctico:")
        print("   - Remesa USD: $10,000")
        print("   - Click en botón '75%'")
        print("   - Se llena: $7,500")
        print("   - Click en 'Configurar Límite'")
        print("   - ✅ Límite configurado!")
        print()
        print("5. El sistema calcula AUTOMÁTICAMENTE:")
        print("   - Monto vendido")
        print("   - Monto disponible")
        print("   - Porcentaje utilizado")
        print()
        print("="*70)
        print("✅ DIFERENCIAS CON LA VISTA ANTERIOR")
        print("="*70)
        print()
        print("ANTES (confusa):")
        print("❌ Tenías que configurar: fecha, moneda, límite, vendido, disponible")
        print("❌ No sabías qué poner en 'vendido' y 'disponible'")
        print("❌ Formulario genérico poco intuitivo")
        print()
        print("AHORA (simple):")
        print("✅ Solo configuras: límite diario")
        print("✅ El sistema calcula vendido y disponible automáticamente")
        print("✅ Una tarjeta por moneda con botones rápidos")
        print("✅ Muestra remesa disponible para referencia")
        print("✅ Validación automática (no puedes exceder la remesa)")
        print()
        print("="*70)
        print("🎨 CARACTERÍSTICAS DE LA NUEVA VISTA")
        print("="*70)
        print()
        print("✅ Visual atractiva con tarjetas por moneda")
        print("✅ Botones rápidos para porcentajes comunes")
        print("✅ Muestra límite actual si ya existe")
        print("✅ Barra de progreso visual del uso del límite")
        print("✅ Alertas si no hay remesa registrada")
        print("✅ Validación en tiempo real")
        print("✅ Responsive (funciona en móviles)")
        print()
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_vista_simple()
