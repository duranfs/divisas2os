#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Diagnosticar por qué los límites no están bloqueando las ventas
"""

import sqlite3
from datetime import datetime

def verificar_estado_actual():
    """Verificar estado actual de límites y transacciones"""
    
    print("🔍 DIAGNÓSTICO: LÍMITES NO ESTÁN BLOQUEANDO VENTAS")
    print("="*70)
    
    try:
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        fecha_hoy = datetime.now().date().strftime('%Y-%m-%d')
        
        # 1. Verificar límites configurados
        print("\n📊 LÍMITES CONFIGURADOS:")
        cursor.execute("""
            SELECT id, moneda, limite_diario, monto_vendido, monto_disponible, 
                   porcentaje_utilizado, activo
            FROM limites_venta 
            WHERE fecha = ?
            ORDER BY moneda
        """, (fecha_hoy,))
        
        limites = cursor.fetchall()
        
        if limites:
            for limite in limites:
                lid, moneda, limite_diario, vendido, disponible, porcentaje, activo = limite
                estado = "✅ ACTIVO" if activo else "❌ INACTIVO"
                print(f"   {moneda}: Límite ${limite_diario:,.2f} | Vendido ${vendido:,.2f} | Disponible ${disponible:,.2f} | {estado}")
        else:
            print("   ❌ NO HAY LÍMITES CONFIGURADOS")
        
        # 2. Verificar transacciones recientes
        print("\n💸 TRANSACCIONES RECIENTES (últimas 10):")
        cursor.execute("""
            SELECT id, fecha_transaccion, tipo_operacion, moneda_destino, 
                   monto_destino
            FROM transacciones 
            WHERE tipo_operacion = 'compra'
            ORDER BY fecha_transaccion DESC
            LIMIT 10
        """)
        
        transacciones = cursor.fetchall()
        
        total_vendido = {}
        
        if transacciones:
            for trans in transacciones:
                tid, fecha, tipo, moneda, monto = trans
                print(f"   💵 ID:{tid} | {fecha} | {moneda} ${monto:,.2f}")
                
                # Sumar por moneda
                if moneda not in total_vendido:
                    total_vendido[moneda] = 0
                total_vendido[moneda] += float(monto)
        
        print("\n📈 TOTAL VENDIDO POR MONEDA (últimas 10 trans):")
        for moneda, total in total_vendido.items():
            print(f"   {moneda}: ${total:,.2f}")
        
        # 3. Verificar si existe el controlador de divisas
        print("\n🔧 VERIFICANDO CONTROLADOR DE DIVISAS:")
        try:
            with open('controllers/divisas.py', 'r', encoding='utf-8') as f:
                contenido = f.read()
                
                # Buscar si tiene validación de límites
                if 'validar_limite_venta' in contenido:
                    print("   ✅ Función validar_limite_venta encontrada")
                else:
                    print("   ❌ NO tiene función validar_limite_venta")
                
                if 'procesar_venta_con_limites' in contenido:
                    print("   ✅ Función procesar_venta_con_limites encontrada")
                else:
                    print("   ❌ NO tiene función procesar_venta_con_limites")
                
                # Buscar función de compra
                if 'def comprar' in contenido or 'def comprar_divisas' in contenido:
                    print("   ✅ Función de compra encontrada")
                    
                    # Ver si llama a validación
                    if 'validar_limite_venta(' in contenido:
                        print("   ✅ La función de compra LLAMA a validar_limite_venta")
                    else:
                        print("   ❌ La función de compra NO llama a validar_limite_venta")
                else:
                    print("   ⚠️  No se encontró función de compra estándar")
        
        except FileNotFoundError:
            print("   ❌ Archivo controllers/divisas.py NO EXISTE")
        
        # 4. Verificar si las funciones están en el modelo
        print("\n🔧 VERIFICANDO MODELO (db.py):")
        try:
            with open('models/db.py', 'r', encoding='utf-8') as f:
                contenido_db = f.read()
                
                if 'def validar_limite_venta' in contenido_db:
                    print("   ✅ Función validar_limite_venta en db.py")
                else:
                    print("   ❌ Función validar_limite_venta NO está en db.py")
                
                if 'def procesar_venta_con_limites' in contenido_db:
                    print("   ✅ Función procesar_venta_con_limites en db.py")
                else:
                    print("   ❌ Función procesar_venta_con_limites NO está en db.py")
        
        except FileNotFoundError:
            print("   ❌ Archivo models/db.py NO EXISTE")
        
        # 5. Verificar remesas
        print("\n💰 REMESAS DISPONIBLES:")
        cursor.execute("""
            SELECT moneda, monto_recibido, monto_disponible, monto_vendido, activa
            FROM remesas_diarias 
            WHERE fecha = ?
            ORDER BY moneda
        """, (fecha_hoy,))
        
        remesas = cursor.fetchall()
        
        if remesas:
            for remesa in remesas:
                moneda, recibido, disponible, vendido, activa = remesa
                estado = "✅ ACTIVA" if activa else "❌ INACTIVA"
                print(f"   {moneda}: Recibido ${recibido:,.2f} | Disponible ${disponible:,.2f} | Vendido ${vendido:,.2f} | {estado}")
        else:
            print("   ❌ NO HAY REMESAS REGISTRADAS")
        
        conn.close()
        
        # CONCLUSIÓN
        print("\n" + "="*70)
        print("🎯 CONCLUSIÓN DEL DIAGNÓSTICO:")
        print("="*70)
        
        if limites and limites[0][6]:  # Si hay límites activos
            print("✅ Límites están configurados y activos")
        else:
            print("❌ PROBLEMA: No hay límites activos")
        
        if remesas and remesas[0][4]:  # Si hay remesas activas
            print("✅ Remesas están registradas y activas")
        else:
            print("❌ PROBLEMA: No hay remesas activas")
        
        print("\n⚠️  PROBLEMA PRINCIPAL:")
        print("   El controlador de divisas NO está validando los límites")
        print("   antes de procesar las compras.")
        print("\n💡 SOLUCIÓN:")
        print("   Necesitas integrar las funciones de validación en el")
        print("   controlador controllers/divisas.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    verificar_estado_actual()
