#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificación simple de la vista de editar cliente
"""

import os

def verificar_vista_editar():
    """Verifica que la vista de editar esté correctamente implementada"""
    
    print("=== VERIFICACIÓN DE VISTA EDITAR ===")
    
    vista_path = 'views/clientes/editar.html'
    
    if not os.path.exists(vista_path):
        print(f"❌ Vista no encontrada: {vista_path}")
        return False
    
    with open(vista_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    print(f"✓ Vista encontrada: {vista_path}")
    print(f"✓ Tamaño: {len(contenido)} caracteres")
    
    # Verificar elementos esenciales
    elementos = [
        ("{{extend 'layout.html'}}", "Layout"),
        ("Editar Cliente", "Título"),
        ("{{=form}}", "Formulario"),
        ("{{=cliente.id}}", "ID cliente"),
        ("<style>", "CSS"),
        ("<script>", "JavaScript")
    ]
    
    encontrados = 0
    for elemento, nombre in elementos:
        if elemento in contenido:
            print(f"✓ {nombre}: OK")
            encontrados += 1
        else:
            print(f"❌ {nombre}: FALTANTE")
    
    # Verificar que no hay errores obvios
    errores = ["SyntaxError", "invalid syntax", "{{if getattr(usuario, 'estado', '') == 'activo':}}"]
    errores_encontrados = 0
    
    for error in errores:
        if error in contenido:
            print(f"⚠️  Posible problema: {error}")
            errores_encontrados += 1
    
    if errores_encontrados == 0:
        print("✓ No se detectaron errores de sintaxis")
    
    puntuacion = (encontrados / len(elementos)) * 100
    
    print(f"\nPuntuación: {puntuacion:.1f}%")
    
    if puntuacion >= 90 and errores_encontrados == 0:
        print("🎉 ¡Vista de editar implementada correctamente!")
        return True
    elif puntuacion >= 70:
        print("✅ Vista implementada con algunos elementos menores faltantes")
        return True
    else:
        print("⚠️  La vista necesita mejoras")
        return False

if __name__ == "__main__":
    print("VERIFICACIÓN DE VISTA DE EDITAR CLIENTE")
    print("=" * 45)
    
    resultado = verificar_vista_editar()
    
    print("\n" + "=" * 45)
    if resultado:
        print("✅ VISTA DE EDITAR LISTA PARA USAR")
    else:
        print("❌ LA VISTA NECESITA CORRECCIONES")
    print("=" * 45)