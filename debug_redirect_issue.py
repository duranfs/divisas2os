#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para diagnosticar por qué redirige al index después de venta
"""

import sqlite3

def debug_redirect_issue():
    """
    Diagnostica el problema del redirect al index
    """
    print("=== DEBUG DEL REDIRECT AL INDEX ===")
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        print("\n1. Verificando última transacción de venta...")
        
        cursor.execute("""
            SELECT 
                id,
                numero_comprobante,
                estado,
                fecha_transaccion
            FROM transacciones 
            WHERE tipo_operacion = 'venta'
            ORDER BY fecha_transaccion DESC
            LIMIT 1
        """)
        
        ultima_venta = cursor.fetchone()
        
        if ultima_venta:
            print(f"   📊 Última venta:")
            print(f"      ID: {ultima_venta[0]}")
            print(f"      Comprobante: {ultima_venta[1]}")
            print(f"      Estado: {ultima_venta[2]}")
            print(f"      Fecha: {ultima_venta[3]}")
            
            transaccion_id_test = ultima_venta[0]
        else:
            print("   ⚠️  No hay ventas registradas")
            transaccion_id_test = None
        
        print("\n2. Verificando función comprobante() con ID real...")
        
        if transaccion_id_test:
            # Simular acceso al comprobante
            cursor.execute("""
                SELECT 
                    t.id,
                    t.cuenta_id,
                    c.cliente_id,
                    cl.user_id
                FROM transacciones t
                JOIN cuentas c ON t.cuenta_id = c.id
                JOIN clientes cl ON c.cliente_id = cl.id
                WHERE t.id = ?
            """, (transaccion_id_test,))
            
            datos_transaccion = cursor.fetchone()
            
            if datos_transaccion:
                print(f"   ✅ Transacción encontrada:")
                print(f"      Transacción ID: {datos_transaccion[0]}")
                print(f"      Cuenta ID: {datos_transaccion[1]}")
                print(f"      Cliente ID: {datos_transaccion[2]}")
                print(f"      User ID: {datos_transaccion[3]}")
            else:
                print("   ❌ No se encontraron datos de la transacción")
        
        print("\n3. Verificando redirects en función comprobante()...")
        
        # Leer el controlador
        with open('controllers/divisas.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        # Buscar todos los redirects en la función comprobante
        redirects_comprobante = [
            ("Redirect por ID faltante", "redirect(URL('divisas', 'index'))"),
            ("Redirect por acceso no autorizado", "Acceso no autorizado"),
            ("Redirect por transacción no encontrada", "Transacción no encontrada"),
            ("Redirect por cuenta no encontrada", "Cuenta no encontrada")
        ]
        
        redirects_encontrados = []
        for nombre, redirect_text in redirects_comprobante:
            if redirect_text in controller_content:
                redirects_encontrados.append(nombre)
                print(f"   ⚠️  {nombre}")
        
        if not redirects_encontrados:
            print("   ✅ No se encontraron redirects problemáticos")
        
        print("\n4. Verificando si transaccion_id es válido...")
        
        # Buscar el patrón de validación de transaccion_id
        if "if transaccion_id and transaccion_id > 0:" in controller_content:
            print("   ✅ Validación de transaccion_id encontrada")
            
            if ultima_venta:
                transaccion_id_valido = ultima_venta[0] and ultima_venta[0] > 0
                print(f"   📊 Última transacción ID válido: {transaccion_id_valido}")
                print(f"   📊 Valor: {ultima_venta[0]}")
        else:
            print("   ❌ Validación de transaccion_id NO encontrada")
        
        print("\n5. Verificando posibles causas del redirect...")
        
        # Buscar otros redirects que puedan estar causando el problema
        posibles_redirects = [
            ("Redirect en catch de excepción", "except.*redirect"),
            ("Redirect por permisos", "auth.*redirect"),
            ("Redirect por error", "error.*redirect")
        ]
        
        import re
        for nombre, patron in posibles_redirects:
            matches = re.findall(patron, controller_content, re.IGNORECASE)
            if matches:
                print(f"   ⚠️  {nombre}: {len(matches)} encontrados")
            else:
                print(f"   ✅ {nombre}: No encontrado")
        
        conn.close()
        
        print("\n6. Análisis del problema:")
        
        if ultima_venta and ultima_venta[0] > 0:
            print("   ✅ Hay transacciones válidas con ID > 0")
            print("   🔍 Problema probable: función comprobante() redirige por permisos")
        else:
            print("   ⚠️  No hay transacciones válidas o ID es 0/None")
            print("   🔍 Problema probable: transaccion_id inválido")
        
        print("\n7. Solución recomendada:")
        print("   1. Verificar logs de web2py para ver qué redirect se ejecuta")
        print("   2. Temporalmente deshabilitar redirect al comprobante")
        print("   3. Mostrar mensaje de éxito en la misma página de venta")
        print("   4. Agregar logging detallado en función comprobante()")
        
        return ultima_venta is not None and ultima_venta[0] > 0
        
    except Exception as e:
        print(f"❌ Error durante el debug: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = debug_redirect_issue()
    print(f"\n{'='*60}")
    if resultado:
        print("🔍 TRANSACCIONES VÁLIDAS - Problema en función comprobante()")
    else:
        print("🔧 TRANSACCIONES INVÁLIDAS - Problema en transaccion_id")
    print(f"{'='*60}")