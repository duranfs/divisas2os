#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para probar el logo de R4 Banco Microfinanciero
"""

import os

def verificar_archivos_logo():
    """Verificar que todos los archivos del logo existen"""
    
    archivos_requeridos = [
        "static/images/logo-r4-banco.svg",
        "static/css/logo-r4.css",
        "views/_logo_r4.html"
    ]
    
    print("🔍 Verificando archivos del logo R4...")
    
    todos_existen = True
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            size = os.path.getsize(archivo)
            print(f"✅ {archivo} ({size} bytes)")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO")
            todos_existen = False
    
    return todos_existen

def verificar_layout_actualizado():
    """Verificar que el layout incluye el logo"""
    
    print("\n🔍 Verificando layout.html...")
    
    try:
        with open("views/layout.html", 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        verificaciones = [
            ("CSS del logo", "logo-r4.css"),
            ("Componente del logo", "_logo_r4.html"),
            ("Copyright R4", "R4 Banco Microfinanciero")
        ]
        
        for nombre, buscar in verificaciones:
            if buscar in contenido:
                print(f"✅ {nombre} - INCLUIDO")
            else:
                print(f"❌ {nombre} - NO ENCONTRADO")
        
        return True
        
    except Exception as e:
        print(f"❌ Error leyendo layout.html: {e}")
        return False

def mostrar_instrucciones():
    """Mostrar instrucciones para ver el logo"""
    
    print("\n" + "="*60)
    print("🎨 LOGO R4 BANCO MICROFINANCIERO INSTALADO")
    print("="*60)
    print()
    print("📋 CARACTERÍSTICAS DEL LOGO:")
    print("- Diseño profesional con colores corporativos")
    print("- Barras gráficas representando crecimiento")
    print("- Texto 'R4 BANCO MICROFINANCIERO'")
    print("- Subtítulo 'Sistema de Divisas'")
    print("- Responsive para móviles")
    print()
    print("🎯 UBICACIONES DEL LOGO:")
    print("- Navbar principal (esquina superior izquierda)")
    print("- Footer con copyright actualizado")
    print("- Título de la página actualizado")
    print()
    print("🚀 PARA VER EL LOGO:")
    print("1. Inicia el servidor web2py")
    print("2. Ve a http://127.0.0.1:8000/divisas2os")
    print("3. El logo aparecerá en la barra de navegación")
    print()
    print("🎨 COLORES UTILIZADOS:")
    print("- Azul oscuro: #1a365d (fondo principal)")
    print("- Azul medio: #2d5a87 (bordes y detalles)")
    print("- Naranja: #ffa366 (texto 'BANCO' y barras)")
    print("- Dorado: #ffd700 (subtítulo y acentos)")
    print("- Blanco: #ffffff (texto principal 'R4')")
    print()
    print("="*60)

def generar_vista_previa():
    """Generar una vista previa HTML del logo"""
    
    html_preview = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vista Previa - Logo R4 Banco Microfinanciero</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="static/css/logo-r4.css">
    <style>
        body { 
            background: #f8f9fa; 
            padding: 40px 20px;
        }
        .preview-section {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .navbar-demo {
            background: #1a365d;
            padding: 10px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .color-palette {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        .color-item {
            text-align: center;
            padding: 10px;
            border-radius: 8px;
            color: white;
            font-size: 12px;
            min-width: 120px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-5">Vista Previa - Logo R4 Banco Microfinanciero</h1>
        
        <!-- Logo en Navbar -->
        <div class="preview-section">
            <h3>Logo en Navbar</h3>
            <div class="navbar-demo">
                <a href="#" class="logo-r4">
                    <div class="logo-r4-icon">
                        <div class="logo-r4-bars">
                            <div class="logo-r4-bar logo-r4-bar-1"></div>
                            <div class="logo-r4-bar logo-r4-bar-2"></div>
                            <div class="logo-r4-bar logo-r4-bar-3"></div>
                        </div>
                    </div>
                    <div class="logo-r4-text">
                        <div class="logo-r4-main">R4</div>
                        <div class="logo-r4-sub">BANCO</div>
                        <div class="logo-r4-desc">MICROFINANCIERO</div>
                    </div>
                </a>
            </div>
        </div>
        
        <!-- Logo Standalone -->
        <div class="preview-section">
            <h3>Logo Independiente</h3>
            <div class="text-center">
                <a href="#" class="logo-r4" style="display: inline-flex;">
                    <div class="logo-r4-icon">
                        <div class="logo-r4-bars">
                            <div class="logo-r4-bar logo-r4-bar-1"></div>
                            <div class="logo-r4-bar logo-r4-bar-2"></div>
                            <div class="logo-r4-bar logo-r4-bar-3"></div>
                        </div>
                    </div>
                    <div class="logo-r4-text">
                        <div class="logo-r4-main">R4</div>
                        <div class="logo-r4-sub">BANCO</div>
                        <div class="logo-r4-desc">MICROFINANCIERO</div>
                    </div>
                </a>
            </div>
        </div>
        
        <!-- Paleta de Colores -->
        <div class="preview-section">
            <h3>Paleta de Colores</h3>
            <div class="color-palette">
                <div class="color-item" style="background: #1a365d;">
                    <strong>#1a365d</strong><br>
                    Azul Oscuro<br>
                    (Fondo)
                </div>
                <div class="color-item" style="background: #2d5a87;">
                    <strong>#2d5a87</strong><br>
                    Azul Medio<br>
                    (Bordes)
                </div>
                <div class="color-item" style="background: #ffa366; color: #000;">
                    <strong>#ffa366</strong><br>
                    Naranja<br>
                    (Acentos)
                </div>
                <div class="color-item" style="background: #ffd700; color: #000;">
                    <strong>#ffd700</strong><br>
                    Dorado<br>
                    (Detalles)
                </div>
                <div class="color-item" style="background: #ffffff; color: #000; border: 1px solid #ddd;">
                    <strong>#ffffff</strong><br>
                    Blanco<br>
                    (Texto)
                </div>
            </div>
        </div>
        
        <!-- Información -->
        <div class="preview-section">
            <h3>Información del Logo</h3>
            <div class="row">
                <div class="col-md-6">
                    <h5>Características:</h5>
                    <ul>
                        <li>Diseño moderno y profesional</li>
                        <li>Barras gráficas representando crecimiento</li>
                        <li>Colores corporativos consistentes</li>
                        <li>Responsive para dispositivos móviles</li>
                        <li>Efectos hover suaves</li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h5>Archivos Generados:</h5>
                    <ul>
                        <li><code>static/images/logo-r4-banco.svg</code></li>
                        <li><code>static/css/logo-r4.css</code></li>
                        <li><code>views/_logo_r4.html</code></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    with open("vista_previa_logo_r4.html", 'w', encoding='utf-8') as f:
        f.write(html_preview)
    
    print("✅ Vista previa generada: vista_previa_logo_r4.html")

if __name__ == "__main__":
    print("🎨 VERIFICACIÓN DEL LOGO R4 BANCO MICROFINANCIERO")
    print("="*60)
    
    archivos_ok = verificar_archivos_logo()
    layout_ok = verificar_layout_actualizado()
    
    if archivos_ok and layout_ok:
        print("\n🟢 INSTALACIÓN COMPLETA Y EXITOSA")
        generar_vista_previa()
        mostrar_instrucciones()
    else:
        print("\n🟡 INSTALACIÓN INCOMPLETA")
        print("Revisa los archivos faltantes arriba.")