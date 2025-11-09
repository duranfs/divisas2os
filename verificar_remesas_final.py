#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script final de verificación del módulo de remesas
"""

import os
import sqlite3

def verificar_todo():
    """Verificación completa del módulo"""
    
    print("🔍 VERIFICACIÓN FINAL DEL MÓDULO DE REMESAS")
    print("="*60)
    
    # 1. Verificar archivos
    print("\n📁 Verificando archivos...")
    archivos = {
        'Controlador': 'controllers/remesas.py',
        'Modelo': 'models/db.py',
        'Vista Index': 'views/remesas/index.html',
        'Vista Registrar': 'views/remesas/registrar_remesa.html',
        'Vista Límites': 'views/remesas/configurar_limites.html',
        'Vista Historial': 'views/remesas/historial_movimientos.html',
        'Vista Ajustar': 'views/remesas/ajustar_remesa.html'
    }
    
    archivos_ok = True
    for nombre, ruta in archivos.items():
        if os.path.exists(ruta):
            print(f"   ✅ {nombre}")
        else:
            print(f"   ❌ {nombre} - FALTA")
            archivos_ok = False
    
    # 2. Verificar tablas
    print("\n🗄️  Verificando tablas...")
    try:
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = [row[0] for row in cursor.fetchall()]
        
        tablas_requeridas = ['remesas_diarias', 'limites_venta', 'movimientos_remesas', 'alertas_limites']
        tablas_ok = True
        
        for tabla in tablas_requeridas:
            if tabla in tablas:
                # Contar registros
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {tabla} ({count} registros)")
            else:
                print(f"   ❌ {tabla} - FALTA")
                tablas_ok = False
        
        conn.close()
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        tablas_ok = False
    
    # 3. Verificar modelo en db.py
    print("\n📝 Verificando modelo en db.py...")
    try:
        with open('models/db.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        if 'remesas_diarias' in contenido:
            print("   ✅ Modelo de remesas agregado a db.py")
            modelo_ok = True
        else:
            print("   ❌ Modelo NO encontrado en db.py")
            modelo_ok = False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        modelo_ok = False
    
    # 4. Verificar datos de ejemplo
    print("\n📊 Verificando datos de ejemplo...")
    try:
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM remesas_diarias WHERE activa = 1")
        remesas_activas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM limites_venta WHERE activo = 1")
        limites_activos = cursor.fetchone()[0]
        
        print(f"   📦 Remesas activas: {remesas_activas}")
        print(f"   📦 Límites activos: {limites_activos}")
        
        if remesas_activas > 0 and limites_activos > 0:
            print("   ✅ Datos de ejemplo presentes")
            datos_ok = True
        else:
            print("   ⚠️  Sin datos de ejemplo (ejecuta instalar_modulo_remesas_completo.py)")
            datos_ok = False
        
        conn.close()
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        datos_ok = False
    
    # Resumen
    print("\n" + "="*60)
    print("📋 RESUMEN DE VERIFICACIÓN")
    print("="*60)
    print(f"Archivos: {'✅ OK' if archivos_ok else '❌ FALTAN ARCHIVOS'}")
    print(f"Tablas: {'✅ OK' if tablas_ok else '❌ FALTAN TABLAS'}")
    print(f"Modelo: {'✅ OK' if modelo_ok else '❌ FALTA MODELO'}")
    print(f"Datos: {'✅ OK' if datos_ok else '⚠️  SIN DATOS'}")
    
    if archivos_ok and tablas_ok and modelo_ok:
        print("\n🎉 ¡MÓDULO COMPLETAMENTE INSTALADO!")
        print("\n🚀 PRÓXIMOS PASOS:")
        print("1. Reinicia el servidor web2py")
        print("2. Accede a: http://127.0.0.1:8000/divisas2os/remesas")
        print("3. Usuario debe tener rol 'administrador'")
        return True
    else:
        print("\n⚠️  HAY PROBLEMAS EN LA INSTALACIÓN")
        print("\n🔧 SOLUCIONES:")
        if not tablas_ok:
            print("- Ejecuta: python instalar_modulo_remesas_completo.py")
        if not modelo_ok:
            print("- El modelo ya fue agregado a db.py, reinicia web2py")
        if not archivos_ok:
            print("- Ejecuta: python agregar_modulo_remesas.py")
        return False

if __name__ == "__main__":
    verificar_todo()
