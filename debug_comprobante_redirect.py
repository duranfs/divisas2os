#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para diagnosticar el problema del redirect después de venta
"""

import sqlite3

def debug_comprobante_redirect():
    """
    Diagnostica el problema del redirect al comprobante
    """
    print("=== DEBUG DEL REDIRECT AL COMPROBANTE ===")
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        print("\n1. Verificando últimas transacciones de venta...")
        
        cursor.execute("""
            SELECT 
                id,
                tipo_operacion,
                numero_comprobante,
                estado,
                fecha_transaccion
            FROM transacciones 
            WHERE tipo_operacion = 'venta'
            ORDER BY fecha_transaccion DESC
            LIMIT 3
        """)
        
        ventas_recientes = cursor.fetchall()
        
        if ventas_recientes:
            print("   📊 Últimas ventas:")
            for venta in ventas_recientes:
                print(f"      ID: {venta[0]} | Comprobante: {venta[2]} | Estado: {venta[3]} | Fecha: {venta[4]}")
        else:
            print("   ⚠️  No hay ventas recientes")
        
        print("\n2. Verificando función comprobante() en controlador...")
        
        # Leer el controlador
        with open('controllers/divisas.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        # Verificar elementos de la función comprobante
        elementos_comprobante = [
            ('Función comprobante existe', 'def comprobante():'),
            ('Validación transaccion_id', 'if not request.args(0):'),
            ('Obtiene transacción', 'transaccion = db(db.transacciones.id == transaccion_id)'),
            ('Verifica permisos', 'cuenta.cliente_id == cliente.id'),
            ('Return con datos', 'return dict(')
        ]
        
        comprobante_ok = 0
        for nombre, elemento in elementos_comprobante:
            if elemento in controller_content:
                comprobante_ok += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Función comprobante: {comprobante_ok}/{len(elementos_comprobante)}")
        
        print("\n3. Verificando vista comprobante.html...")
        
        import os
        if os.path.exists('views/divisas/comprobante.html'):
            print("   ✅ Vista comprobante.html existe")
            
            # Leer la vista para verificar contenido básico
            with open('views/divisas/comprobante.html', 'r', encoding='utf-8') as f:
                vista_content = f.read()
            
            elementos_vista = [
                ('Extiende layout', "{{extend 'layout.html'}}"),
                ('Usa variable transaccion', '{{=transaccion'),
                ('Muestra comprobante', 'comprobante'),
                ('Muestra monto', 'monto')
            ]
            
            vista_ok = 0
            for nombre, elemento in elementos_vista:
                if elemento in vista_content:
                    vista_ok += 1
                    print(f"   ✅ {nombre}")
                else:
                    print(f"   ❌ {nombre}")
            
            print(f"\n   📊 Vista comprobante: {vista_ok}/{len(elementos_vista)}")
        else:
            print("   ❌ Vista comprobante.html NO existe")
        
        print("\n4. Verificando problema en transaccion_id...")
        
        # Buscar líneas duplicadas problemáticas
        lineas = controller_content.split('\n')
        lineas_duplicadas = []
        
        for i, linea in enumerate(lineas):
            if 'transaccion_id_return = int(str(transaccion_id_return).strip())' in linea:
                lineas_duplicadas.append(f"Línea {i+1}: {linea.strip()}")
        
        if len(lineas_duplicadas) > 1:
            print(f"   ⚠️  Líneas duplicadas encontradas ({len(lineas_duplicadas)}):")
            for linea_dup in lineas_duplicadas:
                print(f"      {linea_dup}")
        else:
            print("   ✅ No hay líneas duplicadas problemáticas")
        
        print("\n5. Verificando redirect en función vender()...")
        
        # Buscar el redirect específico
        if "redirect(URL('divisas', 'comprobante', args=[resultado['transaccion_id']]))" in controller_content:
            print("   ✅ Redirect al comprobante encontrado")
        else:
            print("   ❌ Redirect al comprobante NO encontrado")
        
        # Verificar manejo de transaccion_id None
        if "if transaccion_id_return else None" in controller_content:
            print("   ✅ Manejo de transaccion_id None implementado")
        else:
            print("   ❌ No hay manejo de transaccion_id None")
        
        conn.close()
        
        print("\n6. Posibles causas del problema:")
        print("   1. transaccion_id es None y causa error en el redirect")
        print("   2. Función comprobante() redirige de vuelta a index por permisos")
        print("   3. Vista comprobante.html tiene errores y falla")
        print("   4. Líneas duplicadas en el código causan problemas")
        
        print("\n7. Soluciones recomendadas:")
        print("   1. Cambiar redirect para manejar transaccion_id None")
        print("   2. Mostrar mensaje de éxito sin redirect")
        print("   3. Corregir líneas duplicadas en el código")
        print("   4. Agregar logging para debug del transaccion_id")
        
        return comprobante_ok == len(elementos_comprobante)
        
    except Exception as e:
        print(f"❌ Error durante el debug: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = debug_comprobante_redirect()
    print(f"\n{'='*60}")
    if resultado:
        print("🔍 FUNCIÓN COMPROBANTE OK - Problema puede ser en transaccion_id")
    else:
        print("🔧 FUNCIÓN COMPROBANTE TIENE PROBLEMAS")
    print(f"{'='*60}")