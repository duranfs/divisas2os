#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para ayudar a subir el logo de R4 Banco Microfinanciero
"""

import os
import shutil

def mostrar_instrucciones():
    """Mostrar instrucciones claras para subir el logo"""
    
    print("🎨 INTEGRACIÓN DEL LOGO R4 BANCO MICROFINANCIERO")
    print("="*60)
    print()
    print("📋 PASOS PARA INTEGRAR TU LOGO:")
    print()
    print("1. 📁 UBICACIÓN DEL LOGO:")
    print("   - Guarda tu imagen del logo en:")
    print("   - 📂 static/images/logo-r4-real.png")
    print()
    print("2. 📐 ESPECIFICACIONES RECOMENDADAS:")
    print("   - Formato: PNG (preferido) o JPG")
    print("   - Tamaño: 200x60 píxeles aproximadamente")
    print("   - Fondo: Transparente (si es PNG)")
    print("   - Calidad: Alta resolución")
    print()
    print("3. 🚀 APLICAR CAMBIOS:")
    print("   - Ejecuta: python aplicar_logo_real.py")
    print()
    print("4. ✅ VERIFICAR:")
    print("   - Inicia web2py")
    print("   - Ve a tu aplicación")
    print("   - El logo aparecerá en la barra superior")
    print()
    print("="*60)

def verificar_directorio():
    """Verificar que el directorio de imágenes existe"""
    
    directorio = "static/images"
    
    if not os.path.exists(directorio):
        print(f"📁 Creando directorio: {directorio}")
        os.makedirs(directorio, exist_ok=True)
        print("✅ Directorio creado exitosamente")
    else:
        print(f"✅ Directorio existe: {directorio}")
    
    return True

def verificar_logo_existente():
    """Verificar si ya existe un logo"""
    
    logo_path = "static/images/logo-r4-real.png"
    
    if os.path.exists(logo_path):
        size = os.path.getsize(logo_path)
        print(f"✅ Logo encontrado: {logo_path} ({size} bytes)")
        return True
    else:
        print(f"❌ Logo no encontrado: {logo_path}")
        return False

def mostrar_estado_archivos():
    """Mostrar el estado de todos los archivos necesarios"""
    
    print("\n🔍 ESTADO DE ARCHIVOS:")
    print("-" * 40)
    
    archivos = {
        "Logo principal": "static/images/logo-r4-real.png",
        "CSS del logo": "static/css/logo-r4-real.css",
        "Componente HTML": "views/_logo_r4_real.html",
        "Script aplicación": "aplicar_logo_real.py",
        "Instrucciones": "INSTRUCCIONES_LOGO_R4.md"
    }
    
    todos_listos = True
    
    for nombre, archivo in archivos.items():
        if os.path.exists(archivo):
            print(f"✅ {nombre}: {archivo}")
        else:
            print(f"❌ {nombre}: {archivo}")
            if archivo == "static/images/logo-r4-real.png":
                todos_listos = False
    
    print("-" * 40)
    
    if todos_listos:
        print("🟢 TODOS LOS ARCHIVOS LISTOS")
        print("🚀 Ejecuta: python aplicar_logo_real.py")
    else:
        print("🟡 FALTA SUBIR EL LOGO")
        print("📋 Guarda tu logo como: static/images/logo-r4-real.png")
    
    return todos_listos

def crear_ejemplo_html():
    """Crear un ejemplo HTML para probar el logo"""
    
    html_ejemplo = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prueba Logo R4</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="static/css/logo-r4-real.css">
    <style>
        body { background: #f8f9fa; padding: 40px; }
        .test-navbar { background: #1a365d; padding: 15px; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Prueba del Logo R4 Banco Microfinanciero</h1>
        
        <div class="test-navbar mb-4">
            <a href="#" class="navbar-brand d-flex align-items-center">
                <img src="static/images/logo-r4-real.png" 
                     alt="R4 Banco Microfinanciero" 
                     class="logo-r4-real me-2"
                     style="height: 40px; width: auto;">
                <div class="logo-text">
                    <div class="logo-title">Sistema de Divisas</div>
                    <div class="logo-subtitle">R4 Banco Microfinanciero</div>
                </div>
            </a>
        </div>
        
        <div class="alert alert-info">
            <h5>Instrucciones:</h5>
            <ol>
                <li>Guarda tu logo como: <code>static/images/logo-r4-real.png</code></li>
                <li>Recarga esta página para ver el resultado</li>
                <li>Si se ve bien, ejecuta: <code>python aplicar_logo_real.py</code></li>
            </ol>
        </div>
    </div>
</body>
</html>
"""
    
    with open("prueba_logo_r4.html", 'w', encoding='utf-8') as f:
        f.write(html_ejemplo)
    
    print("✅ Archivo de prueba creado: prueba_logo_r4.html")
    print("🌐 Abre este archivo en tu navegador para probar el logo")

if __name__ == "__main__":
    mostrar_instrucciones()
    verificar_directorio()
    
    if verificar_logo_existente():
        print("\n🎉 ¡Logo encontrado! Listo para aplicar.")
        print("🚀 Ejecuta: python aplicar_logo_real.py")
    else:
        print("\n📋 Sube tu logo y luego ejecuta este script nuevamente.")
    
    mostrar_estado_archivos()
    crear_ejemplo_html()
    
    print("\n" + "="*60)
    print("💡 CONSEJOS:")
    print("- Usa formato PNG para mejor calidad")
    print("- Mantén proporciones del logo original")
    print("- Prueba primero con prueba_logo_r4.html")
    print("="*60)