#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script principal para ejecutar la creación y verificación de datos de prueba
Requisitos: 1.1, 2.1

Este script:
1. Genera datos de prueba (usuarios, clientes, cuentas)
2. Verifica que los datos se muestren correctamente
3. Proporciona un resumen completo del estado
"""

import os
import sys
import subprocess
from datetime import datetime

# Configurar path para el proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.insert(0, project_dir)

def run_script(script_name, description):
    """Ejecutar un script y capturar su resultado"""
    print(f"🚀 {description}")
    print("-" * 60)
    
    try:
        # Ejecutar el script
        result = subprocess.run([
            sys.executable, 
            os.path.join(current_dir, script_name)
        ], capture_output=True, text=True, cwd=project_dir)
        
        # Mostrar output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # Verificar si fue exitoso
        success = result.returncode == 0
        
        if success:
            print(f"✅ {description} completado exitosamente")
        else:
            print(f"❌ {description} falló (código: {result.returncode})")
        
        print("-" * 60)
        print()
        
        return success
        
    except Exception as e:
        print(f"❌ Error ejecutando {script_name}: {e}")
        print("-" * 60)
        print()
        return False

def main():
    """Función principal"""
    print("🎯 EJECUCIÓN COMPLETA DE CREACIÓN DE DATOS DE PRUEBA")
    print("=" * 80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("📋 TAREAS A EJECUTAR:")
    print("   1. Generar datos de prueba (usuarios, clientes, cuentas)")
    print("   2. Verificar que los datos se muestren correctamente")
    print("   3. Proporcionar resumen final")
    print()
    
    results = []
    
    # Paso 1: Generar datos de prueba
    success1 = run_script("create_test_data.py", "GENERANDO DATOS DE PRUEBA")
    results.append(("Generación de datos", success1))
    
    # Paso 2: Verificar visualización
    success2 = run_script("verify_display.py", "VERIFICANDO VISUALIZACIÓN DE DATOS")
    results.append(("Verificación de visualización", success2))
    
    # Resumen final
    print("=" * 80)
    print("📊 RESUMEN FINAL DE EJECUCIÓN")
    print("=" * 80)
    
    total_tasks = len(results)
    successful_tasks = sum(1 for _, success in results if success)
    
    print(f"Total de tareas: {total_tasks}")
    print(f"Tareas exitosas: {successful_tasks}")
    print(f"Tareas fallidas: {total_tasks - successful_tasks}")
    print()
    
    print("📋 DETALLE DE RESULTADOS:")
    for task_name, success in results:
        status = "✅ EXITOSO" if success else "❌ FALLIDO"
        print(f"   {task_name}: {status}")
    
    print()
    
    if successful_tasks == total_tasks:
        print("🎉 ¡TODAS LAS TAREAS COMPLETADAS EXITOSAMENTE!")
        print()
        print("✅ DATOS DE PRUEBA CREADOS Y VERIFICADOS")
        print()
        print("📋 PRÓXIMOS PASOS PARA PROBAR EL SISTEMA:")
        print("   1. Iniciar el servidor web2py:")
        print("      python web2py.py -a <password> -i 127.0.0.1 -p 8000")
        print()
        print("   2. Acceder a las siguientes URLs para verificar:")
        print("      • Listado de clientes: http://127.0.0.1:8000/divisas2os/clientes/listar")
        print("      • Listado de cuentas: http://127.0.0.1:8000/divisas2os/cuentas/listar_todas")
        print()
        print("   3. Probar las siguientes funcionalidades:")
        print("      • Filtros de búsqueda por nombre")
        print("      • Filtros de búsqueda por cédula")
        print("      • Filtros por estado (activo/inactivo)")
        print("      • Visualización de estadísticas")
        print("      • Navegación entre páginas (si hay más de 20 registros)")
        print()
        print("   4. Verificar que se muestren:")
        print("      • 11 clientes en total (3 existentes + 8 de prueba)")
        print("      • 9 clientes activos, 2 inactivos")
        print("      • 16 cuentas con diferentes tipos y saldos")
        print("      • Saldos en múltiples monedas (VES, USD, EUR, USDT)")
        print()
        return True
    else:
        print("⚠️  ALGUNAS TAREAS FALLARON")
        print()
        print("🔍 RECOMENDACIONES:")
        if not results[0][1]:  # Si falló la generación
            print("   • Verificar que la base de datos esté accesible")
            print("   • Revisar permisos de escritura en el directorio databases/")
            print("   • Verificar que no haya conflictos con datos existentes")
        
        if not results[1][1]:  # Si falló la verificación
            print("   • Los datos pueden haberse creado pero hay problemas menores")
            print("   • Revisar manualmente la base de datos")
            print("   • Probar acceder a las vistas directamente")
        
        print()
        print("   • Revisar los mensajes de error anteriores")
        print("   • Ejecutar los scripts individualmente para más detalles")
        print()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)