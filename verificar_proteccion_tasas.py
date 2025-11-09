#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificar que todas las funciones de actualización de tasas
estén protegidas con @auth.requires_membership('administrador')
"""

import os
import re

def verificar_proteccion():
    """Verificar protección en controladores"""
    
    print("🔒 VERIFICANDO PROTECCIÓN DE FUNCIONES DE ACTUALIZACIÓN DE TASAS")
    print("="*70)
    
    controladores = [
        'controllers/default.py',
        'controllers/api.py',
        'controllers/crypto_api.py'
    ]
    
    funciones_encontradas = []
    funciones_sin_proteccion = []
    
    for controlador in controladores:
        if not os.path.exists(controlador):
            continue
            
        print(f"\n📄 Verificando: {controlador}")
        
        with open(controlador, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        for i, linea in enumerate(lineas):
            # Buscar funciones de actualización de tasas
            if re.match(r'^def (actualizar.*tasa|verificar.*tasa)', linea):
                nombre_funcion = linea.strip()
                funciones_encontradas.append((controlador, i+1, nombre_funcion))
                
                # Verificar si tiene el decorador en las líneas anteriores
                tiene_proteccion = False
                for j in range(max(0, i-5), i):
                    if "@auth.requires_membership('administrador')" in lineas[j]:
                        tiene_proteccion = True
                        break
                
                if tiene_proteccion:
                    print(f"   ✅ Línea {i+1}: {nombre_funcion.strip()} - PROTEGIDA")
                else:
                    print(f"   ❌ Línea {i+1}: {nombre_funcion.strip()} - SIN PROTECCIÓN")
                    funciones_sin_proteccion.append((controlador, i+1, nombre_funcion))
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN:")
    print("="*70)
    print(f"   Total de funciones encontradas: {len(funciones_encontradas)}")
    print(f"   Funciones protegidas: {len(funciones_encontradas) - len(funciones_sin_proteccion)}")
    print(f"   Funciones SIN protección: {len(funciones_sin_proteccion)}")
    
    if funciones_sin_proteccion:
        print("\n⚠️  FUNCIONES SIN PROTECCIÓN:")
        for controlador, linea, funcion in funciones_sin_proteccion:
            print(f"   {controlador}:{linea} - {funcion.strip()}")
        print("\n❌ ACCIÓN REQUERIDA: Agregar @auth.requires_membership('administrador')")
    else:
        print("\n✅ TODAS LAS FUNCIONES ESTÁN PROTEGIDAS")
    
    print("\n" + "="*70)
    print("🔒 SEGURIDAD:")
    print("="*70)
    print("Solo los usuarios con rol 'administrador' pueden:")
    print("   - Actualizar tasas del BCV")
    print("   - Actualizar tasas de desarrollo")
    print("   - Actualizar tasa USDT")
    print("   - Verificar tasas en BD")
    print()
    print("Los clientes y operadores NO pueden actualizar tasas.")
    print("="*70)
    
    return len(funciones_sin_proteccion) == 0

if __name__ == "__main__":
    resultado = verificar_proteccion()
    exit(0 if resultado else 1)
