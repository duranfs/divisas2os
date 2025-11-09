#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para verificar la integración completa del módulo de Remesas
"""

import os
import sqlite3

def verificar_menu():
    """Verificar que el menú incluye Remesas"""
    
    print("🔍 Verificando integración en el menú...")
    
    try:
        with open("views/layout.html", 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        verificaciones = [
            ("Menú navbar Remesas", "fas fa-money-bill-wave"),
            ("Enlace Dashboard Remesas", "URL('remesas','index')"),
            ("Enlace Registrar Remesa", "URL('remesas','registrar_remesa')"),
            ("Enlace Configurar Límites", "URL('remesas','configurar_limites')"),
            ("Enlace Historial", "URL('remesas','historial_movimientos')"),
            ("Sidebar Remesas", "Dashboard Remesas")
        ]
        
        todos_ok = True
        for nombre, buscar in verificaciones:
            if buscar in contenido:
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre} - NO ENCONTRADO")
                todos_ok = False
        
        return todos_ok
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def verificar_tablas():
    """Verificar que las tablas existen en la BD"""
    
    print("\n🗄️  Verificando tablas en base de datos...")
    
    try:
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
        
        todos_ok = True
        for tabla in tablas_requeridas:
            if tabla in tablas:
                # Contar registros
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {tabla} ({count} registros)")
            else:
                print(f"   ❌ {tabla} - NO EXISTE")
                todos_ok = False
        
        conn.close()
        return todos_ok
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def verificar_archivos():
    """Verificar que todos los archivos existen"""
    
    print("\n📁 Verificando archivos del módulo...")
    
    archivos = [
        ("Controlador", "controllers/remesas.py"),
        ("Vista Dashboard", "views/remesas/index.html"),
        ("Vista Registrar", "views/remesas/registrar_remesa.html"),
        ("Vista Configurar", "views/remesas/configurar_limites.html"),
        ("Vista Historial", "views/remesas/historial_movimientos.html"),
        ("Vista Ajustar", "views/remesas/ajustar_remesa.html")
    ]
    
    todos_ok = True
    for nombre, archivo in archivos:
        if os.path.exists(archivo):
            size = os.path.getsize(archivo) / 1024
            print(f"   ✅ {nombre} ({size:.1f} KB)")
        else:
            print(f"   ❌ {nombre} - NO EXISTE")
            todos_ok = False
    
    return todos_ok

def verificar_datos_ejemplo():
    """Verificar que hay datos de ejemplo"""
    
    print("\n📊 Verificando datos de ejemplo...")
    
    try:
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        # Verificar remesas
        cursor.execute("SELECT COUNT(*) FROM remesas_diarias WHERE activa = 1")
        remesas_activas = cursor.fetchone()[0]
        
        # Verificar límites
        cursor.execute("SELECT COUNT(*) FROM limites_venta WHERE activo = 1")
        limites_activos = cursor.fetchone()[0]
        
        print(f"   📦 Remesas activas: {remesas_activas}")
        print(f"   📦 Límites activos: {limites_activos}")
        
        if remesas_activas > 0 and limites_activos > 0:
            # Mostrar detalle
            cursor.execute("""
                SELECT moneda, monto_recibido, monto_disponible 
                FROM remesas_diarias 
                WHERE activa = 1
            """)
            
            print("\n   💰 Remesas disponibles:")
            for row in cursor.fetchall():
                moneda, recibido, disponible = row
                print(f"      {moneda}: {disponible:,.2f} de {recibido:,.2f}")
            
            cursor.execute("""
                SELECT moneda, limite_diario, monto_disponible 
                FROM limites_venta 
                WHERE activo = 1
            """)
            
            print("\n   📊 Límites configurados:")
            for row in cursor.fetchall():
                moneda, limite, disponible = row
                print(f"      {moneda}: {disponible:,.2f} de {limite:,.2f}")
        
        conn.close()
        return remesas_activas > 0 and limites_activos > 0
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def mostrar_resumen():
    """Mostrar resumen de la verificación"""
    
    print("\n" + "="*60)
    print("📋 RESUMEN DE INTEGRACIÓN")
    print("="*60)
    print()
    print("✅ MÓDULO DE REMESAS Y LÍMITES INTEGRADO")
    print()
    print("📍 UBICACIÓN EN EL MENÚ:")
    print("- Navbar superior: Menú 'Remesas' (dropdown)")
    print("- Sidebar izquierdo: Sección 'Remesas y Límites'")
    print("- Solo visible para Administradores")
    print()
    print("🔗 ENLACES DISPONIBLES:")
    print("1. Dashboard Remesas - Vista general de disponibilidad")
    print("2. Registrar Remesa - Formulario de registro")
    print("3. Configurar Límites - Establecer límites diarios")
    print("4. Historial - Auditoría de movimientos")
    print()
    print("🚀 PARA ACCEDER:")
    print("1. Inicia sesión como Administrador")
    print("2. Busca el menú 'Remesas' en la barra superior")
    print("3. O usa el sidebar 'Remesas y Límites'")
    print("4. URL directa: /remesas/index")
    print()
    print("="*60)

if __name__ == "__main__":
    print("🔍 VERIFICACIÓN DE INTEGRACIÓN DEL MÓDULO DE REMESAS")
    print("="*60)
    
    # Ejecutar verificaciones
    menu_ok = verificar_menu()
    tablas_ok = verificar_tablas()
    archivos_ok = verificar_archivos()
    datos_ok = verificar_datos_ejemplo()
    
    # Mostrar resumen
    mostrar_resumen()
    
    # Resultado final
    if menu_ok and tablas_ok and archivos_ok and datos_ok:
        print("\n🎉 ¡INTEGRACIÓN COMPLETA Y EXITOSA!")
        print("\n💡 El módulo está listo para usar.")
        print("   Inicia sesión como administrador para verlo en el menú.")
    else:
        print("\n⚠️  Hay algunos problemas en la integración")
        print("   Revisa los errores mostrados arriba.")