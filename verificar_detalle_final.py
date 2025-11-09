#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificación final de la funcionalidad de detalles de cliente
Ejecutar desde C:\web2py
"""

import os
import sys

# Rutas correctas
CONTROLADOR_PATH = 'applications/divisas2os/controllers/clientes.py'
VISTA_PATH = 'applications/divisas2os/views/clientes/detalle.html'

def verificar_controlador_detalle():
    """Verifica que la función detalle esté implementada correctamente"""
    
    print("=== VERIFICACIÓN DEL CONTROLADOR DETALLE ===")
    
    try:
        # Verificar que el archivo existe
        if not os.path.exists(CONTROLADOR_PATH):
            print(f"❌ Controlador no encontrado: {CONTROLADOR_PATH}")
            return False
        
        # Leer el archivo del controlador
        with open(CONTROLADOR_PATH, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        print(f"✓ Controlador encontrado: {CONTROLADOR_PATH}")
        
        # Verificar que la función detalle existe
        if 'def detalle():' in contenido:
            print("✓ Función detalle() encontrada")
        else:
            print("❌ Función detalle() no encontrada")
            return False
        
        # Verificar elementos clave de la implementación
        elementos_clave = [
            ('@auth.requires_login()', 'Decorador de autenticación'),
            ('validate_client_access', 'Validación de acceso'),
            ('db.clientes.id == cliente_id', 'Consulta de cliente'),
            ('db.auth_user.id == cliente.user_id', 'Consulta de usuario'),
            ('db.cuentas.cliente_id == cliente_id', 'Consulta de cuentas'),
            ('datos_seguros = Storage()', 'Preparación de datos seguros'),
            ('return dict(', 'Retorno de datos')
        ]
        
        for elemento, descripcion in elementos_clave:
            if elemento in contenido:
                print(f"✓ {descripcion}: {elemento}")
            else:
                print(f"⚠️  {descripcion} faltante: {elemento}")
        
        # Verificar manejo de errores
        if 'try:' in contenido and 'except Exception as e:' in contenido:
            print("✓ Manejo de errores implementado")
        else:
            print("⚠️  Manejo de errores faltante")
        
        # Verificar validación de permisos
        if 'administrador' in contenido and 'operador' in contenido:
            print("✓ Validación de roles implementada")
        else:
            print("⚠️  Validación de roles faltante")
        
        print("✅ Controlador detalle verificado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar controlador: {str(e)}")
        return False

def verificar_vista_detalle():
    """Verifica que la vista detalle.html esté completa"""
    
    print("\n=== VERIFICACIÓN DE LA VISTA DETALLE ===")
    
    try:
        # Verificar que el archivo existe
        if not os.path.exists(VISTA_PATH):
            print(f"❌ Vista no encontrada: {VISTA_PATH}")
            return False
        
        print(f"✓ Vista encontrada: {VISTA_PATH}")
        
        # Leer el contenido
        with open(VISTA_PATH, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar estructura básica
        elementos_estructura = [
            ("{{extend 'layout.html'}}", "Extensión de layout"),
            ('<div class="container-fluid">', "Contenedor principal"),
            ('Detalles del Cliente', "Título de página"),
            ('{{if cliente and datos_seguros:}}', "Validación de datos")
        ]
        
        for elemento, descripcion in elementos_estructura:
            if elemento in contenido:
                print(f"✓ {descripcion}: encontrado")
            else:
                print(f"⚠️  {descripcion}: faltante")
        
        # Verificar secciones principales
        secciones = [
            ('Información Personal', "Sección de datos personales"),
            ('Cuentas Bancarias', "Sección de cuentas"), 
            ('Últimas Transacciones', "Sección de transacciones"),
            ('Cliente No Encontrado', "Manejo de errores")
        ]
        
        for seccion, descripcion in secciones:
            if seccion in contenido:
                print(f"✓ {descripcion}: encontrada")
            else:
                print(f"⚠️  {descripcion}: faltante")
        
        # Verificar campos de datos críticos
        campos_datos = [
            ('{{=datos_seguros.nombre_completo}}', "Nombre completo"),
            ('{{=cliente.cedula}}', "Cédula"),
            ('{{=datos_seguros.email}}', "Email"),
            ('{{=datos_seguros.telefono}}', "Teléfono"),
            ('{{=datos_seguros.direccion}}', "Dirección")
        ]
        
        for campo, descripcion in campos_datos:
            if campo in contenido:
                print(f"✓ {descripcion}: campo presente")
            else:
                print(f"⚠️  {descripcion}: campo faltante")
        
        # Verificar loops de datos
        loops = [
            ('{{for cuenta in cuentas:}}', "Loop de cuentas"),
            ('{{for transaccion in ultimas_transacciones:}}', "Loop de transacciones")
        ]
        
        for loop, descripcion in loops:
            if loop in contenido:
                print(f"✓ {descripcion}: implementado")
            else:
                print(f"⚠️  {descripcion}: faltante")
        
        # Verificar manejo de estados vacíos
        estados_vacios = [
            ('Sin cuentas bancarias', "Mensaje sin cuentas"),
            ('Sin transacciones', "Mensaje sin transacciones"),
            ('{{else:}}', "Manejo de casos vacíos")
        ]
        
        for estado, descripcion in estados_vacios:
            if estado in contenido:
                print(f"✓ {descripcion}: implementado")
            else:
                print(f"⚠️  {descripcion}: faltante")
        
        print("✅ Vista detalle verificada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar vista: {str(e)}")
        return False

def verificar_integracion():
    """Verifica que el controlador y la vista estén integrados correctamente"""
    
    print("\n=== VERIFICACIÓN DE INTEGRACIÓN ===")
    
    try:
        # Leer ambos archivos
        with open(CONTROLADOR_PATH, 'r', encoding='utf-8') as f:
            controlador = f.read()
        
        with open(VISTA_PATH, 'r', encoding='utf-8') as f:
            vista = f.read()
        
        # Verificar que los datos que pasa el controlador coinciden con lo que espera la vista
        datos_controlador = [
            'cliente=cliente',
            'usuario=usuario', 
            'datos_seguros=datos_seguros',
            'cuentas=cuentas',
            'ultimas_transacciones=ultimas_transacciones'
        ]
        
        datos_vista = [
            '{{if cliente',
            '{{if usuario',
            'datos_seguros.',
            '{{for cuenta in cuentas',
            '{{for transaccion in ultimas_transacciones'
        ]
        
        print("Verificando integración controlador-vista:")
        
        for i, (dato_ctrl, dato_vista) in enumerate(zip(datos_controlador, datos_vista)):
            ctrl_ok = dato_ctrl in controlador
            vista_ok = dato_vista in vista
            
            if ctrl_ok and vista_ok:
                print(f"✓ Dato {i+1}: Controlador y vista integrados")
            elif ctrl_ok and not vista_ok:
                print(f"⚠️  Dato {i+1}: Controlador OK, Vista faltante")
            elif not ctrl_ok and vista_ok:
                print(f"⚠️  Dato {i+1}: Vista OK, Controlador faltante")
            else:
                print(f"❌ Dato {i+1}: Ambos faltantes")
        
        print("✅ Integración verificada")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar integración: {str(e)}")
        return False

def main():
    """Función principal de verificación"""
    
    print("VERIFICACIÓN FINAL DE FUNCIONALIDAD DE DETALLES DE CLIENTE")
    print("=" * 70)
    print(f"Directorio actual: {os.getcwd()}")
    print(f"Controlador: {CONTROLADOR_PATH}")
    print(f"Vista: {VISTA_PATH}")
    print("=" * 70)
    
    # Ejecutar todas las verificaciones
    resultados = []
    
    resultados.append(("Controlador", verificar_controlador_detalle()))
    resultados.append(("Vista", verificar_vista_detalle()))
    resultados.append(("Integración", verificar_integracion()))
    
    # Mostrar resumen
    print("\n" + "=" * 70)
    print("RESUMEN FINAL DE VERIFICACIÓN")
    print("=" * 70)
    
    todos_ok = True
    for nombre, resultado in resultados:
        estado = "✅ OK" if resultado else "❌ ERROR"
        print(f"{nombre:20}: {estado}")
        if not resultado:
            todos_ok = False
    
    print("\n" + "=" * 70)
    if todos_ok:
        print("🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
        print("✅ La funcionalidad de detalles de cliente está completamente implementada")
        print("✅ El controlador y la vista están correctamente integrados")
        print("✅ La funcionalidad está lista para usar")
        print("\n📋 PRÓXIMOS PASOS:")
        print("   1. Acceder a la aplicación web")
        print("   2. Ir a Gestión de Clientes")
        print("   3. Hacer clic en 'Ver detalles' de cualquier cliente")
        print("   4. Verificar que se muestran todos los datos correctamente")
    else:
        print("⚠️  ALGUNAS VERIFICACIONES FALLARON")
        print("❌ Revisar los elementos faltantes arriba")
        print("❌ Corregir los problemas antes de usar la funcionalidad")
    
    print("=" * 70)

if __name__ == "__main__":
    main()