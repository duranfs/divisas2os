#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def aplicar_logo_real():
    print("🎨 Aplicando logo real de R4 Banco Microfinanciero...")
    
    # Verificar que el logo existe
    if not os.path.exists("static/images/logo-r4-real.png"):
        print("❌ ERROR: No se encontró static/images/logo-r4-real.png")
        print("📋 Por favor:")
        print("1. Guarda tu logo como: static/images/logo-r4-real.png")
        print("2. Ejecuta este script nuevamente")
        return False
    
    # Leer layout actual
    try:
        with open("views/layout.html", 'r', encoding='utf-8') as f:
            layout_content = f.read()
    except Exception as e:
        print(f"❌ Error leyendo layout.html: {e}")
        return False
    
    # Actualizar CSS en layout
    if "logo-r4-real.css" not in layout_content:
        layout_content = layout_content.replace(
            'logo-r4.css',
            'logo-r4-real.css'
        )
        print("✅ CSS actualizado en layout.html")
    
    # Actualizar componente del logo
    if "_logo_r4.html" in layout_content:
        layout_content = layout_content.replace(
            "_logo_r4.html",
            "_logo_r4_real.html"
        )
        print("✅ Componente del logo actualizado")
    
    # Escribir layout actualizado
    try:
        with open("views/layout.html", 'w', encoding='utf-8') as f:
            f.write(layout_content)
        print("✅ Layout.html actualizado exitosamente")
    except Exception as e:
        print(f"❌ Error escribiendo layout.html: {e}")
        return False
    
    return True

def verificar_integracion():
    archivos_necesarios = [
        "static/images/logo-r4-real.png",
        "static/css/logo-r4-real.css", 
        "views/_logo_r4_real.html"
    ]
    
    print("\n🔍 Verificando integración...")
    
    todos_ok = True
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - FALTANTE")
            todos_ok = False
    
    if todos_ok:
        print("\n🟢 INTEGRACIÓN COMPLETA")
        print("🚀 Inicia web2py para ver tu logo de R4!")
    else:
        print("\n🟡 INTEGRACIÓN INCOMPLETA")
        print("Revisa los archivos faltantes.")
    
    return todos_ok

if __name__ == "__main__":
    print("="*60)
    print("🎨 APLICANDO LOGO REAL R4 BANCO MICROFINANCIERO")
    print("="*60)
    
    if aplicar_logo_real():
        verificar_integracion()
    else:
        print("\n❌ No se pudo completar la aplicación del logo")
