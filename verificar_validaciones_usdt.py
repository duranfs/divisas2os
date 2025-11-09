#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar que todas las validaciones incluyan USDT
"""

def verificar_validaciones():
    """
    Verifica que todas las validaciones de moneda incluyan USDT
    """
    print("=== VERIFICACIÓN DE VALIDACIONES USDT ===")
    
    try:
        # Leer el controlador
        with open('controllers/divisas.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        print("\n1. Verificando validaciones corregidas...")
        
        # Validaciones que deben incluir USDT
        validaciones_correctas = [
            ("Validación venta origen", "moneda_origen not in ['USD', 'EUR', 'USDT']"),
            ("Validación compra destino", "moneda_destino not in ['USD', 'EUR', 'USDT']"),
            ("Mensaje error venta", "Moneda origen debe ser USD, EUR o USDT"),
            ("Mensaje error compra API", "destino USD, EUR o USDT"),
            ("Mensaje error venta API", "origen debe ser USD, EUR o USDT")
        ]
        
        validaciones_encontradas = 0
        for nombre, validacion in validaciones_correctas:
            if validacion in controller_content:
                validaciones_encontradas += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Validaciones corregidas: {validaciones_encontradas}/{len(validaciones_correctas)}")
        
        print("\n2. Verificando validaciones obsoletas...")
        
        # Validaciones obsoletas que NO deben existir
        validaciones_obsoletas = [
            ("Validación venta solo USD/EUR", "moneda_origen not in ['USD', 'EUR']:"),
            ("Validación compra solo USD/EUR", "moneda_destino not in ['USD', 'EUR']:"),
            ("Mensaje error solo USD/EUR", "Moneda origen debe ser USD o EUR"),
            ("Mensaje API solo USD/EUR compra", "destino USD o EUR"),
            ("Mensaje API solo USD/EUR venta", "origen debe ser USD o EUR")
        ]
        
        validaciones_obsoletas_encontradas = 0
        for nombre, validacion in validaciones_obsoletas:
            if validacion in controller_content:
                validaciones_obsoletas_encontradas += 1
                print(f"   ❌ {nombre} (OBSOLETA - debe corregirse)")
            else:
                print(f"   ✅ {nombre} (correctamente eliminada)")
        
        print(f"\n   📊 Validaciones obsoletas encontradas: {validaciones_obsoletas_encontradas}/{len(validaciones_obsoletas)}")
        
        print("\n3. Verificando soporte completo USDT...")
        
        # Elementos de soporte USDT
        soporte_usdt = [
            ("Procesamiento compra USDT", "elif moneda_destino == 'USDT':"),
            ("Procesamiento venta USDT", "elif moneda_origen == 'USDT':"),
            ("Tasa USDT en obtener_tasas_actuales", "'usdt_ves': float(tasa_activa.usdt_ves)"),
            ("Tasa USDT en obtener_tasas_para_transacciones", "usdt_base = tasas_base['usdt_ves']"),
            ("Saldo USDT manejo NULL compra", "saldo_usdt_actual = cuenta.saldo_usdt if cuenta.saldo_usdt is not None"),
            ("Saldo USDT manejo NULL venta", "saldo_disponible = cuenta.saldo_usdt if cuenta.saldo_usdt is not None"),
            ("Actualización saldo USDT compra", "nuevo_saldo_usdt = saldo_usdt_actual + monto_destino"),
            ("Actualización saldo USDT venta", "nuevo_saldo_usdt = saldo_usdt_actual - monto_origen")
        ]
        
        soporte_encontrado = 0
        for nombre, elemento in soporte_usdt:
            if elemento in controller_content:
                soporte_encontrado += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Soporte USDT completo: {soporte_encontrado}/{len(soporte_usdt)}")
        
        print("\n4. Resumen de correcciones:")
        
        if validaciones_encontradas == len(validaciones_correctas):
            print("   ✅ Todas las validaciones incluyen USDT correctamente")
        else:
            print("   ❌ Faltan validaciones por corregir")
        
        if validaciones_obsoletas_encontradas == 0:
            print("   ✅ No hay validaciones obsoletas")
        else:
            print("   ❌ Hay validaciones obsoletas que deben corregirse")
        
        if soporte_encontrado == len(soporte_usdt):
            print("   ✅ Soporte completo para USDT implementado")
        else:
            print("   ❌ Soporte USDT incompleto")
        
        print("\n5. Instrucciones para probar:")
        print("   1. Reiniciar web2py")
        print("   2. Ir a: http://127.0.0.1:8000/divisas2os/divisas/vender")
        print("   3. Seleccionar USDT como moneda a vender")
        print("   4. Ingresar cantidad y confirmar")
        print("   5. Verificar que no aparezca el error de validación")
        
        return (validaciones_encontradas == len(validaciones_correctas) and 
                validaciones_obsoletas_encontradas == 0 and 
                soporte_encontrado == len(soporte_usdt))
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = verificar_validaciones()
    print(f"\n{'='*60}")
    if resultado:
        print("🎉 TODAS LAS VALIDACIONES CORREGIDAS - USDT debería funcionar")
    else:
        print("🔧 VALIDACIONES INCOMPLETAS - Revisar correcciones")
    print(f"{'='*60}")