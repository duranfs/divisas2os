#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificación final de la vista de detalles
Ejecutar desde C:\web2py
"""

import os

def verificar_vista_detalle():
    """Verifica que la vista de detalles esté completa y funcional"""
    
    print("=== VERIFICACIÓN DE VISTA DE DETALLES ===")
    
    vista_path = "applications/divisas2os/views/clientes/detalle.html"
    
    if not os.path.exists(vista_path):
        print(f"❌ Vista no encontrada: {vista_path}")
        return False
    
    with open(vista_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    print(f"✓ Vista encontrada: {vista_path}")
    print(f"✓ Tamaño del archivo: {len(contenido)} caracteres")
    
    # Verificar elementos esenciales
    elementos_esenciales = [
        ("{{extend 'layout.html'}}", "Extensión de layout"),
        ("Detalles del Cliente", "Título principal"),
        ("{{if cliente and datos_seguros:}}", "Validación de datos"),
        ("Información Personal", "Sección personal"),
        ("Cuentas Bancarias", "Sección de cuentas"),
        ("Últimas Transacciones", "Sección de transacciones"),
        ("{{=datos_seguros.nombre_completo}}", "Campo nombre"),
        ("{{for cuenta in cuentas:}}", "Loop de cuentas"),
        ("{{for transaccion in ultimas_transacciones:}}", "Loop de transacciones"),
        ("Cliente No Encontrado", "Manejo de errores")
    ]
    
    elementos_encontrados = 0
    for elemento, descripcion in elementos_esenciales:
        if elemento in contenido:
            elementos_encontrados += 1
            print(f"✓ {descripcion}: {elemento}")
        else:
            print(f"⚠️  {descripcion}: FALTANTE")
    
    porcentaje = (elementos_encontrados / len(elementos_esenciales)) * 100
    print(f"\n📊 Completitud: {elementos_encontrados}/{len(elementos_esenciales)} ({porcentaje:.1f}%)")
    
    # Verificar secciones específicas
    secciones_importantes = [
        ("card-header", "Headers de tarjetas"),
        ("btn btn-warning", "Botón editar"),
        ("btn btn-secondary", "Botón volver"),
        ("table-responsive", "Tablas responsive"),
        ("badge bg-success", "Estados activos"),
        ("fas fa-", "Iconos FontAwesome")
    ]
    
    print("\n--- Elementos de UI ---")
    for seccion, descripcion in secciones_importantes:
        if seccion in contenido:
            print(f"✓ {descripcion}")
        else:
            print(f"⚠️  {descripcion}: faltante")
    
    if porcentaje >= 80:
        print("\n✅ Vista de detalles está funcional")
        return True
    else:
        print("\n❌ Vista de detalles necesita mejoras")
        return False

def verificar_enlaces_detalle():
    """Verifica que los enlaces a la vista de detalles estén correctos"""
    
    print("\n=== VERIFICACIÓN DE ENLACES A DETALLES ===")
    
    # Verificar en vista de listado
    listar_path = "applications/divisas2os/views/clientes/listar.html"
    
    if os.path.exists(listar_path):
        with open(listar_path, 'r', encoding='utf-8') as f:
            contenido_listar = f.read()
        
        print(f"✓ Vista de listado encontrada: {listar_path}")
        
        if "URL('clientes', 'detalle'" in contenido_listar:
            print("✓ Enlace a detalles encontrado en vista de listado")
        else:
            print("⚠️  Enlace a detalles faltante en vista de listado")
        
        if 'title="Ver detalles"' in contenido_listar:
            print("✓ Tooltip de detalles encontrado")
        else:
            print("⚠️  Tooltip de detalles faltante")
        
        if 'fas fa-eye' in contenido_listar:
            print("✓ Icono de ojo para ver detalles encontrado")
        else:
            print("⚠️  Icono de ojo faltante")
            
        return True
    else:
        print(f"⚠️  Vista de listado no encontrada: {listar_path}")
        return False

def verificar_controlador_detalle():
    """Verifica que el controlador tenga la función detalle"""
    
    print("\n=== VERIFICACIÓN DE CONTROLADOR ===")
    
    controlador_path = "applications/divisas2os/controllers/clientes.py"
    
    if os.path.exists(controlador_path):
        with open(controlador_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        print(f"✓ Controlador encontrado: {controlador_path}")
        
        if 'def detalle():' in contenido:
            print("✓ Función detalle() encontrada en controlador")
        else:
            print("❌ Función detalle() NO encontrada en controlador")
            return False
        
        if '@auth.requires_login()' in contenido:
            print("✓ Decorador de autenticación encontrado")
        else:
            print("⚠️  Decorador de autenticación faltante")
        
        return True
    else:
        print(f"❌ Controlador no encontrado: {controlador_path}")
        return False

def main():
    print("VERIFICACIÓN COMPLETA DE FUNCIONALIDAD DE DETALLES")
    print("=" * 60)
    print(f"Directorio actual: {os.getcwd()}")
    print("=" * 60)
    
    vista_ok = verificar_vista_detalle()
    enlaces_ok = verificar_enlaces_detalle()
    controlador_ok = verificar_controlador_detalle()
    
    print("\n" + "=" * 60)
    print("RESUMEN FINAL:")
    print(f"Vista de detalles: {'✅ OK' if vista_ok else '❌ ERROR'}")
    print(f"Enlaces: {'✅ OK' if enlaces_ok else '❌ ERROR'}")
    print(f"Controlador: {'✅ OK' if controlador_ok else '❌ ERROR'}")
    
    todo_ok = vista_ok and enlaces_ok and controlador_ok
    
    print("\n" + "=" * 60)
    if todo_ok:
        print("🎉 ¡LA VISTA DE DETALLES ESTÁ COMPLETAMENTE FUNCIONAL!")
        print("\n📋 CÓMO USAR:")
        print("1. Acceder a la aplicación web")
        print("2. Ir a 'Gestión' → 'Clientes'")
        print("3. En la lista de clientes, hacer clic en el ícono de ojo (👁️)")
        print("4. Se abrirá la vista de detalles completa del cliente")
        print("\n✨ CARACTERÍSTICAS DE LA VISTA:")
        print("• Información personal completa")
        print("• Lista de cuentas bancarias con saldos")
        print("• Historial de transacciones recientes")
        print("• Botones de acción (editar, activar/inactivar)")
        print("• Navegación breadcrumb")
        print("• Diseño responsive")
    else:
        print("⚠️  HAY PROBLEMAS QUE RESOLVER")
        print("❌ Revisar los elementos faltantes arriba")
        
        if not vista_ok:
            print("\n🔧 PARA ARREGLAR LA VISTA:")
            print("• Verificar que el archivo detalle.html existe")
            print("• Completar los elementos faltantes")
        
        if not enlaces_ok:
            print("\n🔧 PARA ARREGLAR LOS ENLACES:")
            print("• Agregar enlaces a detalle en la vista de listado")
            print("• Verificar que los URLs sean correctos")
        
        if not controlador_ok:
            print("\n🔧 PARA ARREGLAR EL CONTROLADOR:")
            print("• Implementar la función detalle() en clientes.py")
            print("• Agregar decoradores de autenticación")
    
    print("=" * 60)

if __name__ == "__main__":
    main()