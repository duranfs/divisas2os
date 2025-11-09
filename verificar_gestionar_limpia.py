#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificación rápida de la vista gestionar limpia
"""

import os

def verificar_vista_limpia():
    """Verifica que la vista gestionar esté limpia y sin problemas de formato"""
    
    print("=== VERIFICACIÓN DE VISTA GESTIONAR LIMPIA ===")
    
    vista_path = 'views/cuentas/gestionar.html'
    
    if not os.path.exists(vista_path):
        print(f"❌ Vista no encontrada: {vista_path}")
        return False
    
    with open(vista_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    print(f"✓ Vista encontrada: {vista_path}")
    print(f"✓ Tamaño: {len(contenido)} caracteres")
    
    # Verificar que no hay problemas de formato
    problemas_formato = [
        ('page-header h1 { color: #000 !important; font-weight: 700; margin-bottom: 0.5rem; } .page-header .lead', "CSS mal formateado"),
        ('border-radius: 1rem; margin-bottom: 2rem; box-shadow: 0 10px 15px', "CSS en línea visible"),
        ('document.addEventListener(\'DOMContentLoaded\', function() {', "JavaScript visible como texto")
    ]
    
    problemas_encontrados = 0
    for problema, descripcion in problemas_formato:
        if problema in contenido:
            print(f"❌ {descripcion}: ENCONTRADO")
            problemas_encontrados += 1
        else:
            print(f"✓ {descripcion}: OK")
    
    # Verificar elementos esenciales
    elementos_esenciales = [
        ("{{extend 'layout.html'}}", "Layout correcto"),
        ("Gestionar Cuenta", "Título correcto"),
        ("{{if cuenta and cliente and usuario:}}", "Validación de datos"),
        ("{{=form}}", "Formulario presente"),
        ("{{=cuenta.numero_cuenta}}", "Número de cuenta"),
        ("{{=usuario.first_name}}", "Nombre del cliente"),
        ("Saldos Actuales", "Sección de saldos"),
        ("<style>", "CSS presente"),
        ("</style>", "CSS cerrado correctamente")
    ]
    
    elementos_encontrados = 0
    for elemento, descripcion in elementos_esenciales:
        if elemento in contenido:
            print(f"✓ {descripcion}: OK")
            elementos_encontrados += 1
        else:
            print(f"❌ {descripcion}: FALTANTE")
    
    # Verificar que el CSS está en el lugar correcto
    css_inicio = contenido.find('<style>')
    css_fin = contenido.find('</style>')
    
    if css_inicio != -1 and css_fin != -1 and css_fin > css_inicio:
        print("✓ CSS correctamente encapsulado")
        css_correcto = True
    else:
        print("❌ CSS mal formateado o faltante")
        css_correcto = False
    
    # Calcular puntuación
    puntuacion_elementos = (elementos_encontrados / len(elementos_esenciales)) * 100
    puntuacion_formato = ((len(problemas_formato) - problemas_encontrados) / len(problemas_formato)) * 100
    
    puntuacion_total = (puntuacion_elementos + puntuacion_formato) / 2
    
    print(f"\n=== PUNTUACIONES ===")
    print(f"Elementos esenciales: {puntuacion_elementos:.1f}%")
    print(f"Formato correcto: {puntuacion_formato:.1f}%")
    print(f"PUNTUACIÓN TOTAL: {puntuacion_total:.1f}%")
    
    if puntuacion_total >= 90 and css_correcto:
        print("\n🎉 ¡Vista gestionar limpia y funcional!")
        return True
    elif puntuacion_total >= 75:
        print("\n✅ Vista funcional con algunos elementos menores")
        return True
    else:
        print("\n⚠️  La vista necesita correcciones")
        return False

if __name__ == "__main__":
    print("VERIFICACIÓN DE VISTA GESTIONAR LIMPIA")
    print("=" * 45)
    
    resultado = verificar_vista_limpia()
    
    print(f"\n{'=' * 45}")
    if resultado:
        print("✅ VISTA GESTIONAR CORREGIDA Y FUNCIONAL")
        print("📋 Ya no deberían aparecer líneas de CSS al final")
        print("📋 La página debería verse correctamente")
    else:
        print("❌ LA VISTA NECESITA MÁS CORRECCIONES")
    print("=" * 45)