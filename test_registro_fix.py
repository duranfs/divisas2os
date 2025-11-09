#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar que el error del formulario de registro está corregido
"""

def verificar_correccion():
    """
    Verifica que la corrección del controlador está aplicada
    """
    print("=== VERIFICACIÓN DE CORRECCIÓN DEL FORMULARIO ===")
    
    try:
        # Leer el controlador
        with open('controllers/clientes.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        print("1. Verificando corrección en el controlador...")
        
        # Buscar los return statements corregidos
        returns_correctos = [
            'return dict(form=form, registro_exitoso=True, numero_cuenta=numero_cuenta)',
            'return dict(form=form, registro_exitoso=False)'
        ]
        
        returns_encontrados = 0
        for return_stmt in returns_correctos:
            if return_stmt in controller_content:
                returns_encontrados += 1
                print(f"   ✅ Encontrado: {return_stmt}")
            else:
                print(f"   ❌ Faltante: {return_stmt}")
        
        print(f"\n   📊 Returns corregidos: {returns_encontrados}/{len(returns_correctos)}")
        
        # Verificar que no hay returns sin registro_exitoso
        returns_incorrectos = [
            'return dict(form=form)\n',
            'return dict(form=form) '
        ]
        
        returns_incorrectos_encontrados = 0
        for return_incorrecto in returns_incorrectos:
            if return_incorrecto in controller_content:
                returns_incorrectos_encontrados += 1
                print(f"   ⚠️  Encontrado return incorrecto: {return_incorrecto.strip()}")
        
        if returns_incorrectos_encontrados == 0:
            print("   ✅ No se encontraron returns incorrectos")
        
        print("\n2. Verificando vista registrar.html...")
        
        # Leer la vista
        with open('views/clientes/registrar.html', 'r', encoding='utf-8') as f:
            vista_content = f.read()
        
        # Verificar que la vista usa registro_exitoso correctamente
        if '{{if registro_exitoso:}}' in vista_content:
            print("   ✅ Vista usa registro_exitoso correctamente")
        else:
            print("   ❌ Vista no usa registro_exitoso")
        
        # Verificar que hay un else para cuando no es exitoso
        if '{{else:}}' in vista_content:
            print("   ✅ Vista tiene bloque else para formulario")
        else:
            print("   ❌ Vista no tiene bloque else")
        
        print("\n3. Resumen de la corrección:")
        
        if returns_encontrados == len(returns_correctos) and returns_incorrectos_encontrados == 0:
            print("   ✅ CORRECCIÓN APLICADA EXITOSAMENTE")
            print("   📝 El error 'registro_exitoso is not defined' debería estar resuelto")
            print("   🎯 El formulario ahora debería funcionar correctamente")
        else:
            print("   ❌ CORRECCIÓN INCOMPLETA")
            print("   🔧 Revisar los return statements en el controlador")
        
        print("\n4. Instrucciones para probar:")
        print("   1. Reiniciar web2py si está ejecutándose")
        print("   2. Ir a: http://127.0.0.1:8000/divisas2os/clientes/registrar")
        print("   3. Llenar el formulario con datos de prueba")
        print("   4. Verificar que no aparece el error NameError")
        
        return returns_encontrados == len(returns_correctos) and returns_incorrectos_encontrados == 0
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = verificar_correccion()
    print(f"\n{'='*60}")
    if resultado:
        print("🎉 CORRECCIÓN EXITOSA - El formulario debería funcionar ahora")
    else:
        print("🔧 CORRECCIÓN INCOMPLETA - Revisar manualmente")
    print(f"{'='*60}")