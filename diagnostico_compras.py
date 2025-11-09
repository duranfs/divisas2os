#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Diagnóstico del sistema de compras de divisas
"""

def diagnosticar_compras():
    """
    Diagnóstica el sistema de compras de divisas
    """
    print("=== DIAGNÓSTICO DEL SISTEMA DE COMPRAS ===")
    
    try:
        print("\n1. Verificando controlador de divisas...")
        
        # Leer el controlador
        with open('controllers/divisas.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        # Verificar funciones clave
        funciones_clave = [
            ('Función comprar', 'def comprar():'),
            ('Función comprar_simple', 'def comprar_simple():'),
            ('Función procesar_compra_divisa', 'def procesar_compra_divisa():'),
            ('Función procesar_venta_divisa', 'def procesar_venta_divisa():'),
            ('Función generar_comprobante_unico', 'def generar_comprobante_unico('),
            ('Función calcular_comision', 'def calcular_comision(')
        ]
        
        funciones_encontradas = 0
        for nombre, funcion in funciones_clave:
            if funcion in controller_content:
                funciones_encontradas += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Funciones encontradas: {funciones_encontradas}/{len(funciones_clave)}")
        
        print("\n2. Verificando corrección de funciones de compra...")
        
        # Verificar que las funciones llamen a procesar_compra_divisa
        correcciones = [
            ('Función comprar llama procesar_compra_divisa', 'resultado = procesar_compra_divisa()'),
            ('Función comprar_simple llama procesar_compra_divisa', 'resultado = procesar_compra_divisa()'),
            ('Manejo de resultado exitoso', "resultado.get('success')"),
            ('Manejo de errores', "resultado.get('error'"),
            ('Logging de compra real', 'Procesando compra REAL')
        ]
        
        correcciones_aplicadas = 0
        for nombre, codigo in correcciones:
            if codigo in controller_content:
                correcciones_aplicadas += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Correcciones aplicadas: {correcciones_aplicadas}/{len(correcciones)}")
        
        print("\n3. Verificando estructura de base de datos...")
        
        # Verificar que existe la tabla de transacciones
        import os
        if os.path.exists('databases/storage.sqlite'):
            print("   ✅ Base de datos encontrada")
            
            # Verificar estructura básica
            try:
                import sqlite3
                conn = sqlite3.connect('databases/storage.sqlite')
                cursor = conn.cursor()
                
                # Verificar tablas clave
                tablas_requeridas = ['transacciones', 'cuentas', 'clientes', 'tasas_cambio']
                tablas_encontradas = 0
                
                for tabla in tablas_requeridas:
                    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tabla}';")
                    if cursor.fetchone():
                        tablas_encontradas += 1
                        print(f"   ✅ Tabla {tabla}")
                    else:
                        print(f"   ❌ Tabla {tabla}")
                
                print(f"\n   📊 Tablas encontradas: {tablas_encontradas}/{len(tablas_requeridas)}")
                
                # Verificar si hay cuentas con saldos
                cursor.execute("SELECT COUNT(*) FROM cuentas WHERE saldo_ves > 0;")
                cuentas_con_saldo = cursor.fetchone()[0]
                print(f"   📊 Cuentas con saldo VES: {cuentas_con_saldo}")
                
                # Verificar si hay tasas de cambio
                cursor.execute("SELECT COUNT(*) FROM tasas_cambio WHERE activa = 1;")
                tasas_activas = cursor.fetchone()[0]
                print(f"   📊 Tasas de cambio activas: {tasas_activas}")
                
                conn.close()
                
            except Exception as e:
                print(f"   ⚠️  Error verificando BD: {str(e)}")
        else:
            print("   ❌ Base de datos no encontrada")
        
        print("\n4. Verificando vistas de compra...")
        
        # Verificar que existen las vistas
        vistas_requeridas = [
            'views/divisas/comprar.html',
            'views/divisas/index.html'
        ]
        
        vistas_encontradas = 0
        for vista in vistas_requeridas:
            if os.path.exists(vista):
                vistas_encontradas += 1
                print(f"   ✅ {vista}")
            else:
                print(f"   ❌ {vista}")
        
        print(f"\n   📊 Vistas encontradas: {vistas_encontradas}/{len(vistas_requeridas)}")
        
        print("\n5. Resumen del diagnóstico...")
        
        problemas_detectados = []
        
        if funciones_encontradas < len(funciones_clave):
            problemas_detectados.append("Faltan funciones clave en el controlador")
        
        if correcciones_aplicadas < len(correcciones):
            problemas_detectados.append("Las funciones de compra no están corregidas")
        
        if vistas_encontradas < len(vistas_requeridas):
            problemas_detectados.append("Faltan vistas del módulo de divisas")
        
        if problemas_detectados:
            print("   ⚠️  Problemas detectados:")
            for i, problema in enumerate(problemas_detectados, 1):
                print(f"      {i}. {problema}")
        else:
            print("   ✅ No se detectaron problemas obvios")
        
        print("\n6. Instrucciones para probar las compras:")
        print("   1. Reiniciar web2py si está ejecutándose")
        print("   2. Iniciar sesión como administrador o cliente")
        print("   3. Ir a: http://127.0.0.1:8000/divisas2os/divisas/comprar")
        print("   4. Llenar el formulario de compra")
        print("   5. Verificar que se registre la transacción en la BD")
        print("   6. Revisar logs de web2py para mensajes de debug")
        
        print("\n7. Si las compras siguen fallando, verificar:")
        print("   - Que el usuario tenga una cuenta con saldo VES suficiente")
        print("   - Que existan tasas de cambio activas en la BD")
        print("   - Los logs de web2py para errores específicos")
        print("   - Permisos de la base de datos")
        
        return correcciones_aplicadas == len(correcciones) and funciones_encontradas == len(funciones_clave)
        
    except Exception as e:
        print(f"❌ Error durante el diagnóstico: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = diagnosticar_compras()
    print(f"\n{'='*60}")
    if resultado:
        print("🎉 DIAGNÓSTICO EXITOSO - Las compras deberían funcionar ahora")
    else:
        print("🔧 DIAGNÓSTICO INCOMPLETO - Revisar problemas detectados")
    print(f"{'='*60}")