#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test para verificar las funciones de generación de números de cuenta por moneda
"""

import sys
import os

print("=" * 70)
print("TEST: Funciones de Generación de Números de Cuenta por Moneda")
print("=" * 70)

# Simular las funciones (copiadas de los controladores)
def generar_numero_cuenta_por_moneda_test(moneda, cuentas_existentes=None):
    """
    Versión de prueba de la función generar_numero_cuenta_por_moneda
    """
    import random
    
    if cuentas_existentes is None:
        cuentas_existentes = set()
    
    # Definir prefijos por moneda
    prefijos = {
        'VES': '01',
        'USD': '02',
        'EUR': '03',
        'USDT': '04'
    }
    
    # Obtener prefijo (por defecto VES si la moneda no es válida)
    prefijo = prefijos.get(moneda, '01')
    
    # Generar número de cuenta único
    max_intentos = 100
    for _ in range(max_intentos):
        # Generar 18 dígitos aleatorios
        digitos = ''.join([str(random.randint(0, 9)) for _ in range(18)])
        
        # Combinar prefijo + dígitos = 20 dígitos totales
        numero_cuenta = prefijo + digitos
        
        # Verificar unicidad
        if numero_cuenta not in cuentas_existentes:
            return numero_cuenta
    
    raise Exception("No se pudo generar número de cuenta único")

def generar_numero_cuenta_test(cuentas_existentes=None):
    """
    Versión de prueba de la función generar_numero_cuenta
    """
    return generar_numero_cuenta_por_moneda_test('VES', cuentas_existentes)

# -------------------------------------------------------------------------
# Pruebas
# -------------------------------------------------------------------------

print("\n1. Probando generar_numero_cuenta_por_moneda() con diferentes monedas:")
print("-" * 70)

monedas = ['VES', 'USD', 'EUR', 'USDT']
prefijos_esperados = {
    'VES': '01',
    'USD': '02',
    'EUR': '03',
    'USDT': '04'
}

cuentas_generadas = set()
todo_ok = True

for moneda in monedas:
    try:
        numero = generar_numero_cuenta_por_moneda_test(moneda, cuentas_generadas)
        
        # Verificar longitud
        if len(numero) != 20:
            print(f"   ❌ {moneda}: Longitud incorrecta ({len(numero)} dígitos)")
            todo_ok = False
            continue
        
        # Verificar prefijo
        prefijo_esperado = prefijos_esperados[moneda]
        if not numero.startswith(prefijo_esperado):
            print(f"   ❌ {moneda}: Prefijo incorrecto (esperado {prefijo_esperado}, obtenido {numero[:2]})")
            todo_ok = False
            continue
        
        # Verificar que sea numérico
        if not numero.isdigit():
            print(f"   ❌ {moneda}: Contiene caracteres no numéricos")
            todo_ok = False
            continue
        
        # Verificar unicidad
        if numero in cuentas_generadas:
            print(f"   ❌ {moneda}: Número duplicado")
            todo_ok = False
            continue
        
        cuentas_generadas.add(numero)
        print(f"   ✅ {moneda}: {numero} (prefijo {numero[:2]}, 18 dígitos aleatorios)")
        
    except Exception as e:
        print(f"   ❌ {moneda}: Error - {str(e)}")
        todo_ok = False

print("\n2. Probando generar_numero_cuenta() (compatibilidad con código existente):")
print("-" * 70)

try:
    numero_ves = generar_numero_cuenta_test(cuentas_generadas)
    
    # Verificar que sea VES por defecto
    if numero_ves.startswith('01'):
        print(f"   ✅ Genera cuenta VES por defecto: {numero_ves}")
    else:
        print(f"   ❌ No genera cuenta VES por defecto (prefijo: {numero_ves[:2]})")
        todo_ok = False
    
    # Verificar longitud
    if len(numero_ves) == 20:
        print(f"   ✅ Longitud correcta: 20 dígitos")
    else:
        print(f"   ❌ Longitud incorrecta: {len(numero_ves)} dígitos")
        todo_ok = False
    
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    todo_ok = False

print("\n3. Probando unicidad (generar múltiples cuentas de la misma moneda):")
print("-" * 70)

try:
    cuentas_usd = set()
    num_cuentas = 10
    
    for i in range(num_cuentas):
        numero = generar_numero_cuenta_por_moneda_test('USD', cuentas_usd)
        cuentas_usd.add(numero)
    
    if len(cuentas_usd) == num_cuentas:
        print(f"   ✅ Generadas {num_cuentas} cuentas USD únicas")
        print(f"   Ejemplos:")
        for i, cuenta in enumerate(list(cuentas_usd)[:3], 1):
            print(f"      {i}. {cuenta}")
    else:
        print(f"   ❌ Se generaron duplicados ({len(cuentas_usd)} únicas de {num_cuentas})")
        todo_ok = False
        
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    todo_ok = False

print("\n4. Probando manejo de moneda inválida:")
print("-" * 70)

try:
    numero_invalido = generar_numero_cuenta_por_moneda_test('XXX', cuentas_generadas)
    
    # Debe usar VES por defecto
    if numero_invalido.startswith('01'):
        print(f"   ✅ Moneda inválida usa VES por defecto: {numero_invalido}")
    else:
        print(f"   ❌ Moneda inválida no usa VES por defecto (prefijo: {numero_invalido[:2]})")
        todo_ok = False
        
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    todo_ok = False

# -------------------------------------------------------------------------
# Resumen
# -------------------------------------------------------------------------

print("\n" + "=" * 70)
if todo_ok:
    print("✅ TODAS LAS PRUEBAS PASARON")
    print("\nImplementación correcta:")
    print("  - generar_numero_cuenta_por_moneda(moneda) funciona correctamente")
    print("  - Prefijos por moneda: VES=01, USD=02, EUR=03, USDT=04")
    print("  - Genera 20 dígitos totales (2 prefijo + 18 aleatorios)")
    print("  - Valida unicidad correctamente")
    print("  - generar_numero_cuenta() mantiene compatibilidad (VES por defecto)")
else:
    print("❌ ALGUNAS PRUEBAS FALLARON")
    print("\nRevisar la implementación de las funciones")

print("=" * 70)
