#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para verificar y corregir el controlador de remesas
"""

import os

def verificar_controlador():
    """Verificar que el controlador tenga todas las funciones necesarias"""
    
    print("🔍 Verificando controlador de remesas...")
    
    if not os.path.exists('controllers/remesas.py'):
        print("❌ Controlador no encontrado")
        return False
    
    with open('controllers/remesas.py', 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    funciones_requeridas = [
        'obtener_disponibilidad_moneda',
        'registrar_movimiento_remesa',
        'calcular_estadisticas_mes',
        'def index',
        'def registrar_remesa',
        'def configurar_limites',
        'def historial_movimientos',
        'def ajustar_remesa'
    ]
    
    print("\n📋 Verificando funciones:")
    todas_presentes = True
    for funcion in funciones_requeridas:
        if funcion in contenido:
            print(f"   ✅ {funcion}")
        else:
            print(f"   ❌ {funcion} - FALTA")
            todas_presentes = False
    
    return todas_presentes

def verificar_tablas_bd():
    """Verificar que las tablas existan en la BD"""
    
    print("\n🗄️  Verificando tablas en base de datos...")
    
    try:
        import sqlite3
        
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        # Obtener lista de tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = [row[0] for row in cursor.fetchall()]
        
        tablas_requeridas = [
            'remesas_diarias',
            'limites_venta',
            'movimientos_remesas',
            'alertas_limites'
        ]
        
        todas_presentes = True
        for tabla in tablas_requeridas:
            if tabla in tablas:
                print(f"   ✅ {tabla}")
            else:
                print(f"   ❌ {tabla} - FALTA")
                todas_presentes = False
        
        conn.close()
        return todas_presentes
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def probar_acceso():
    """Generar URL de prueba"""
    
    print("\n🌐 URL de acceso al módulo:")
    print("   http://127.0.0.1:8000/divisas2os/remesas")
    print("\n📝 Requisitos:")
    print("   - Usuario con rol 'administrador'")
    print("   - Servidor web2py en ejecución")

def mostrar_solucion():
    """Mostrar solución si hay problemas"""
    
    print("\n" + "="*60)
    print("🔧 SOLUCIÓN DE PROBLEMAS")
    print("="*60)
    print()
    print("Si el error persiste:")
    print()
    print("1. Verifica que el servidor web2py esté reiniciado")
    print("2. Limpia el cache de web2py:")
    print("   - Elimina archivos en applications/divisas2os/errors/")
    print("   - Elimina archivos en applications/divisas2os/sessions/")
    print()
    print("3. Verifica que las tablas existan:")
    print("   python instalar_modulo_remesas_completo.py")
    print()
    print("4. Verifica que el usuario tenga rol 'administrador'")
    print()
    print("="*60)

if __name__ == "__main__":
    print("🔧 VERIFICACIÓN DEL MÓDULO DE REMESAS")
    print("="*60)
    
    controlador_ok = verificar_controlador()
    tablas_ok = verificar_tablas_bd()
    
    probar_acceso()
    
    if controlador_ok and tablas_ok:
        print("\n✅ MÓDULO VERIFICADO CORRECTAMENTE")
        print("\n🚀 El módulo debería funcionar ahora")
        print("   Reinicia el servidor web2py si es necesario")
    else:
        print("\n⚠️  HAY PROBLEMAS EN EL MÓDULO")
        mostrar_solucion()
