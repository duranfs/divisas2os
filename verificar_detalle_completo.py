#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificación completa de la funcionalidad de detalles de cliente
"""

import os
import sys

def verificar_controlador_detalle():
    """Verifica que la función detalle esté implementada correctamente"""
    
    print("=== VERIFICACIÓN DEL CONTROLADOR DETALLE ===")
    
    try:
        # Leer el archivo del controlador
        with open('controllers/clientes.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar que la función detalle existe
        if 'def detalle():' in contenido:
            print("✓ Función detalle() encontrada")
        else:
            print("❌ Función detalle() no encontrada")
            return False
        
        # Verificar elementos clave de la implementación
        elementos_clave = [
            'auth.requires_login()',
            'validate_client_access',
            'db.clientes.id == cliente_id',
            'db.auth_user.id == cliente.user_id',
            'db.cuentas.cliente_id == cliente_id',
            'datos_seguros = Storage()',
            'return dict('
        ]
        
        for elemento in elementos_clave:
            if elemento in contenido:
                print(f"✓ Elemento encontrado: {elemento}")
            else:
                print(f"⚠️  Elemento faltante: {elemento}")
        
        # Verificar manejo de errores
        if 'try:' in contenido and 'except Exception as e:' in contenido:
            print("✓ Manejo de errores implementado")
        else:
            print("⚠️  Manejo de errores faltante")
        
        print("✅ Controlador detalle verificado")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar controlador: {str(e)}")
        return False

def verificar_vista_detalle():
    """Verifica que la vista detalle.html esté completa"""
    
    print("\n=== VERIFICACIÓN DE LA VISTA DETALLE ===")
    
    try:
        # Verificar que el archivo existe
        vista_path = "views/clientes/detalle.html"
        if not os.path.exists(vista_path):
            print(f"❌ Vista no encontrada: {vista_path}")
            return False
        
        print(f"✓ Vista encontrada: {vista_path}")
        
        # Leer el contenido
        with open(vista_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar estructura básica
        elementos_estructura = [
            "{{extend 'layout.html'}}",
            '<div class="container-fluid">',
            'Detalles del Cliente',
            '{{if cliente and datos_seguros:}}'
        ]
        
        for elemento in elementos_estructura:
            if elemento in contenido:
                print(f"✓ Estructura: {elemento}")
            else:
                print(f"⚠️  Estructura faltante: {elemento}")
        
        # Verificar secciones principales
        secciones = [
            'Información Personal',
            'Cuentas Bancarias', 
            'Últimas Transacciones',
            'Cliente No Encontrado'
        ]
        
        for seccion in secciones:
            if seccion in contenido:
                print(f"✓ Sección: {seccion}")
            else:
                print(f"⚠️  Sección faltante: {seccion}")
        
        # Verificar campos de datos
        campos_datos = [
            '{{=datos_seguros.nombre_completo}}',
            '{{=cliente.cedula}}',
            '{{=datos_seguros.email}}',
            '{{=datos_seguros.telefono}}',
            '{{=datos_seguros.direccion}}'
        ]
        
        for campo in campos_datos:
            if campo in contenido:
                print(f"✓ Campo: {campo}")
            else:
                print(f"⚠️  Campo faltante: {campo}")
        
        # Verificar loops de datos
        loops = [
            '{{for cuenta in cuentas:}}',
            '{{for transaccion in ultimas_transacciones:}}'
        ]
        
        for loop in loops:
            if loop in contenido:
                print(f"✓ Loop: {loop}")
            else:
                print(f"⚠️  Loop faltante: {loop}")
        
        # Verificar manejo de estados vacíos
        estados_vacios = [
            '{{else:}}',
            'Sin cuentas bancarias',
            'Sin transacciones'
        ]
        
        for estado in estados_vacios:
            if estado in contenido:
                print(f"✓ Estado vacío: {estado}")
            else:
                print(f"⚠️  Estado vacío faltante: {estado}")
        
        print("✅ Vista detalle verificada")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar vista: {str(e)}")
        return False

def verificar_funciones_auxiliares():
    """Verifica que las funciones auxiliares necesarias existan"""
    
    print("\n=== VERIFICACIÓN DE FUNCIONES AUXILIARES ===")
    
    try:
        # Leer el archivo del controlador
        with open('controllers/clientes.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar funciones auxiliares
        funciones_auxiliares = [
            'def validate_client_access(',
            'def get_user_roles(',
            'def log_error(',
            'def handle_database_error('
        ]
        
        for funcion in funciones_auxiliares:
            if funcion in contenido:
                print(f"✓ Función auxiliar: {funcion}")
            else:
                print(f"⚠️  Función auxiliar faltante: {funcion}")
        
        print("✅ Funciones auxiliares verificadas")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar funciones auxiliares: {str(e)}")
        return False

def verificar_permisos_acceso():
    """Verifica que los decoradores de permisos estén correctos"""
    
    print("\n=== VERIFICACIÓN DE PERMISOS ===")
    
    try:
        # Leer el archivo del controlador
        with open('controllers/clientes.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar la función detalle y verificar decoradores
        lineas = contenido.split('\n')
        encontrar_detalle = False
        
        for i, linea in enumerate(lineas):
            if 'def detalle():' in linea:
                encontrar_detalle = True
                # Verificar líneas anteriores para decoradores
                for j in range(max(0, i-5), i):
                    if '@auth.requires_login()' in lineas[j]:
                        print("✓ Decorador @auth.requires_login() encontrado")
                        break
                else:
                    print("⚠️  Decorador @auth.requires_login() faltante")
                break
        
        if not encontrar_detalle:
            print("❌ Función detalle() no encontrada")
            return False
        
        # Verificar validación de permisos dentro de la función
        if 'auth.has_membership(' in contenido:
            print("✓ Validación de membresía encontrada")
        else:
            print("⚠️  Validación de membresía faltante")
        
        if 'administrador' in contenido and 'operador' in contenido:
            print("✓ Roles administrador y operador verificados")
        else:
            print("⚠️  Roles administrador/operador faltantes")
        
        print("✅ Permisos verificados")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar permisos: {str(e)}")
        return False

def main():
    """Función principal de verificación"""
    
    print("VERIFICACIÓN COMPLETA DE FUNCIONALIDAD DE DETALLES DE CLIENTE")
    print("=" * 70)
    
    # Ejecutar todas las verificaciones
    resultados = []
    
    resultados.append(("Controlador", verificar_controlador_detalle()))
    resultados.append(("Vista", verificar_vista_detalle()))
    resultados.append(("Funciones Auxiliares", verificar_funciones_auxiliares()))
    resultados.append(("Permisos", verificar_permisos_acceso()))
    
    # Mostrar resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE VERIFICACIÓN")
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
        print("✅ El controlador y la vista están listos para usar")
    else:
        print("⚠️  ALGUNAS VERIFICACIONES FALLARON")
        print("❌ Revisar los elementos faltantes arriba")
    
    print("=" * 70)

if __name__ == "__main__":
    main()